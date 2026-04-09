import json
import random
import re
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"
SAFE_FALLBACK_PRESET = "Balanced"
BUST_KEYS = ("flat", "small", "medium", "large", "xlarge")
CATEGORY_FILES = {
    "hairStyle": "hair_styles.json",
    "hairColor": "hair_colors.json",
    "eyeColor": "eye_colors.json",
    "accessory": "accessories.json",
    "bustSize": "bust_sizes.json",
}


def clamp_probability(value, fallback=0.0):
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = float(fallback)

    return min(1.0, max(0.0, numeric))


def slugify(value):
    text = re.sub(r"[^a-zA-Z0-9 ]+", "", str(value or ""))
    text = re.sub(r"\s+", "_", text.strip().lower())
    return text


def to_name(parts):
    slug = slugify(" ".join(part for part in parts if part))
    return slug or "oc_prompt"


class DataCatalog:
    def __init__(self, data_dir=None):
        self.data_dir = Path(data_dir or DATA_DIR)
        self._base_prompt_data = self._load_json("base_prompt.json")
        self._presets = self._load_json("presets.json")
        self._categories = {
            key: self._normalize_category(self._load_json(filename))
            for key, filename in CATEGORY_FILES.items()
        }

    def _load_json(self, filename):
        with (self.data_dir / filename).open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def _normalize_option(self, option):
        if isinstance(option, str):
            return {
                "key": option,
                "prompt": option,
                "label": option,
                "name": option,
                "developmentOnly": False,
            }

        key = (
            option.get("key")
            or option.get("id")
            or option.get("name")
            or option.get("label")
            or option.get("value")
            or option.get("prompt")
            or ""
        )
        prompt = option.get("prompt") or option.get("value") or option.get("label") or ""
        label = option.get("label") or prompt
        name = option.get("name") or prompt

        return {
            "key": str(key),
            "prompt": str(prompt),
            "label": str(label),
            "name": str(name),
            "developmentOnly": bool(option.get("developmentOnly", False)),
        }

    def _normalize_category(self, category):
        return {
            "key": str(category.get("key", "")),
            "label": str(category.get("label", "")),
            "tagType": str(category.get("tagType", "default")),
            "description": str(category.get("description", "")),
            "optional": bool(category.get("optional", False)),
            "includeChance": clamp_probability(category.get("includeChance", 1.0), 1.0),
            "emptyLabel": str(category.get("emptyLabel", "none")),
            "includeInName": category.get("includeInName", True) is not False,
            "developmentOnly": bool(category.get("developmentOnly", False)),
            "values": [self._normalize_option(value) for value in category.get("values", [])],
        }

    @property
    def default_base_prompt(self):
        return str(self._base_prompt_data.get("default", "")).strip()

    @property
    def preset_names(self):
        return tuple(self._presets.keys())

    def get_preset(self, preset_name):
        return self._presets.get(preset_name, self._presets[SAFE_FALLBACK_PRESET])

    def get_category(self, category_key, production_mode=True):
        category = self._categories[category_key]
        if not production_mode:
            return category

        if category["developmentOnly"]:
            return dict(category, values=[])

        return dict(
            category,
            values=[value for value in category["values"] if not value["developmentOnly"]],
        )

    def get_fixed_choices(self, category_key):
        category = self._categories[category_key]
        return tuple(["none"] + [value["label"] for value in category["values"]])

    def get_bust_choices(self):
        return tuple(["none"] + [value["label"] for value in self._categories["bustSize"]["values"]])


class OriginalCharacterGenerator:
    def __init__(self, catalog=None):
        self.catalog = catalog or DataCatalog()

    def build_settings(
        self,
        *,
        base_prompt,
        include_base_prompt,
        preset,
        fixed_hair_style,
        fixed_hair_color,
        fixed_eye_color,
        fixed_accessory,
        fixed_bust_size,
        weight_flat,
        weight_small,
        weight_medium,
        weight_large,
        weight_xlarge,
        accessory_probability,
        production_mode,
    ):
        preset_name = preset if preset in self.catalog.preset_names else SAFE_FALLBACK_PRESET
        return {
            "base_prompt": str(base_prompt or "").strip(),
            "include_base_prompt": bool(include_base_prompt),
            "preset": preset_name,
            "fixed": {
                "hair_style": fixed_hair_style or "none",
                "hair_color": fixed_hair_color or "none",
                "eye_color": fixed_eye_color or "none",
                "accessory": fixed_accessory or "none",
                "bust_size": fixed_bust_size or "none",
            },
            "weights": {
                "flat": clamp_probability(weight_flat, 0.0),
                "small": clamp_probability(weight_small, 0.0),
                "medium": clamp_probability(weight_medium, 0.0),
                "large": clamp_probability(weight_large, 0.0),
                "xlarge": clamp_probability(weight_xlarge, 0.0),
            },
            "accessory_probability": clamp_probability(accessory_probability, 0.0),
            "production_mode": bool(production_mode),
        }

    def settings_to_json(self, settings):
        return json.dumps(settings, ensure_ascii=False, sort_keys=True)

    def resolve_option(self, category, raw_value):
        if raw_value in (None, "", "none"):
            return None

        candidate = str(raw_value).strip().lower()
        for option in category["values"]:
            if candidate in {
                option["label"].lower(),
                option["key"].lower(),
                option["prompt"].lower(),
                option["name"].lower(),
            }:
                return option

        return None

    def choose_random_option(self, rng, category):
        if not category["values"]:
            return None

        if category["optional"] and rng.random() >= category["includeChance"]:
            return None

        return rng.choice(category["values"])

    def resolve_bust_weights(self, preset_name, weights):
        raw_weights = {key: clamp_probability(weights.get(key, 0.0), 0.0) for key in BUST_KEYS}
        raw_total = sum(raw_weights.values())

        if raw_total <= 0:
            fallback_preset = self.catalog.get_preset(SAFE_FALLBACK_PRESET)
            fallback_weights = dict(fallback_preset["bust_weights"])
            fallback_total = sum(fallback_weights.values())
            normalized = {key: fallback_weights[key] / fallback_total for key in BUST_KEYS}
            return {
                "raw": raw_weights,
                "normalized": normalized,
                "raw_total": 0.0,
                "fallback_used": True,
                "fallback_preset": SAFE_FALLBACK_PRESET,
                "selected_preset": preset_name,
            }

        normalized = {key: raw_weights[key] / raw_total for key in BUST_KEYS}
        return {
            "raw": raw_weights,
            "normalized": normalized,
            "raw_total": raw_total,
            "fallback_used": False,
            "fallback_preset": SAFE_FALLBACK_PRESET,
            "selected_preset": preset_name,
        }

    def choose_weighted_bust(self, rng, category, distribution):
        roll = rng.random()
        cumulative = 0.0
        fallback_option = category["values"][0] if category["values"] else None
        option_map = {option["key"]: option for option in category["values"]}

        for key in BUST_KEYS:
            option = option_map.get(key)
            if option is None:
                continue

            cumulative += distribution["normalized"][key]
            fallback_option = option
            if roll <= cumulative:
                return option

        return fallback_option

    def choose_accessory(self, rng, category, fixed_accessory, accessory_probability):
        if fixed_accessory == "__none__":
            return None

        resolved_fixed = self.resolve_option(category, fixed_accessory)
        if resolved_fixed is not None:
            return resolved_fixed

        if rng.random() >= clamp_probability(accessory_probability, 0.0):
            return None

        return rng.choice(category["values"]) if category["values"] else None

    def choose_generic(self, rng, category, fixed_value):
        resolved_fixed = self.resolve_option(category, fixed_value)
        if resolved_fixed is not None:
            return resolved_fixed

        return self.choose_random_option(rng, category)

    def format_prompt(self, base_prompt, selected_entries):
        parts = [base_prompt] + [
            entry["option"]["prompt"]
            for entry in selected_entries
            if entry["option"] is not None
        ]
        return ", ".join(part for part in parts if part)

    def build_name(self, selected_entries):
        parts = [
            entry["option"]["name"]
            for entry in selected_entries
            if entry["option"] is not None and entry["category"]["includeInName"]
        ]
        return to_name(parts)

    def build_formatted_prompt(self, name, prompt):
        return f"name: {name}\npositive: {prompt}\nnegative: \n\n----------"

    def generate_from_settings(self, seed, settings):
        rng = random.Random(int(seed))
        settings = dict(settings or {})
        fixed = dict(settings.get("fixed", {}))
        weights = dict(settings.get("weights", {}))
        categories = {
            key: self.catalog.get_category(
                key,
                production_mode=bool(settings.get("production_mode", True)),
            )
            for key in CATEGORY_FILES
        }
        distribution = self.resolve_bust_weights(
            settings.get("preset", SAFE_FALLBACK_PRESET),
            weights,
        )

        hair_style = self.choose_generic(rng, categories["hairStyle"], fixed.get("hair_style"))
        hair_color = self.choose_generic(rng, categories["hairColor"], fixed.get("hair_color"))
        eye_color = self.choose_generic(rng, categories["eyeColor"], fixed.get("eye_color"))
        accessory = self.choose_accessory(
            rng,
            categories["accessory"],
            fixed.get("accessory"),
            settings.get("accessory_probability", 0.0),
        )

        fixed_bust_option = None
        fixed_bust_size = fixed.get("bust_size")
        if fixed_bust_size not in (None, "", "none"):
            fixed_bust_option = self.resolve_option(categories["bustSize"], fixed_bust_size)

        if fixed_bust_option is not None:
            bust_size = fixed_bust_option
        else:
            bust_size = self.choose_weighted_bust(rng, categories["bustSize"], distribution)

        selected_entries = [
            {"category": categories["hairStyle"], "option": hair_style},
            {"category": categories["hairColor"], "option": hair_color},
            {"category": categories["eyeColor"], "option": eye_color},
            {"category": categories["accessory"], "option": accessory},
            {"category": categories["bustSize"], "option": bust_size},
        ]

        raw_base_prompt = str(settings.get("base_prompt", "") or "").strip()
        include_base_prompt = settings.get("include_base_prompt")
        if include_base_prompt is None:
            include_base_prompt = bool(raw_base_prompt)

        effective_base_prompt = ""
        if bool(include_base_prompt):
            effective_base_prompt = raw_base_prompt or self.catalog.default_base_prompt

        prompt = self.format_prompt(effective_base_prompt, selected_entries)
        name = self.build_name(selected_entries)
        formatted_prompt = self.build_formatted_prompt(name, prompt)

        metadata = {
            "seed": int(seed),
            "base_prompt": effective_base_prompt,
            "include_base_prompt": bool(include_base_prompt),
            "preset": settings.get("preset", SAFE_FALLBACK_PRESET),
            "production_mode": bool(settings.get("production_mode", True)),
            "fixed": fixed,
            "bust_weights": distribution,
            "accessory_probability": clamp_probability(settings.get("accessory_probability", 0.0), 0.0),
            "result": {
                "prompt": prompt,
                "formatted_prompt": formatted_prompt,
                "name": name,
                "hair_style": hair_style["label"] if hair_style else "",
                "hair_color": hair_color["label"] if hair_color else "",
                "eye_color": eye_color["label"] if eye_color else "",
                "accessory": accessory["label"] if accessory else categories["accessory"]["emptyLabel"],
                "bust_size": bust_size["label"] if bust_size else "",
            },
        }

        return {
            "prompt": prompt,
            "formatted_prompt": formatted_prompt,
            "name": name,
            "hair_style": hair_style["label"] if hair_style else "",
            "hair_color": hair_color["label"] if hair_color else "",
            "eye_color": eye_color["label"] if eye_color else "",
            "accessory": accessory["label"] if accessory else categories["accessory"]["emptyLabel"],
            "bust_size": bust_size["label"] if bust_size else "",
            "metadata_json": json.dumps(metadata, ensure_ascii=False, sort_keys=True),
        }

    def generate_list_from_settings(self, seed, list_count, settings):
        count = max(1, int(list_count))
        return [
            self.generate_from_settings(int(seed) + index, settings)
            for index in range(count)
        ]

    def generate_one(
        self,
        *,
        seed,
        base_prompt,
        include_base_prompt,
        preset,
        fixed_hair_style,
        fixed_hair_color,
        fixed_eye_color,
        fixed_accessory,
        fixed_bust_size,
        weight_flat,
        weight_small,
        weight_medium,
        weight_large,
        weight_xlarge,
        accessory_probability,
        production_mode,
    ):
        settings = self.build_settings(
            base_prompt=base_prompt,
            include_base_prompt=include_base_prompt,
            preset=preset,
            fixed_hair_style=fixed_hair_style,
            fixed_hair_color=fixed_hair_color,
            fixed_eye_color=fixed_eye_color,
            fixed_accessory=fixed_accessory,
            fixed_bust_size=fixed_bust_size,
            weight_flat=weight_flat,
            weight_small=weight_small,
            weight_medium=weight_medium,
            weight_large=weight_large,
            weight_xlarge=weight_xlarge,
            accessory_probability=accessory_probability,
            production_mode=production_mode,
        )
        return self.generate_from_settings(seed, settings)
