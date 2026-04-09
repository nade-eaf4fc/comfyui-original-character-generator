import json
import re
from pathlib import Path

from .generator import PACKAGE_DIR, SAFE_FALLBACK_PRESET, clamp_probability


USER_PRESETS_DIR = PACKAGE_DIR / "user_presets"
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1F]+')
FIXED_CATEGORY_KEYS = (
    "hair_style",
    "hair_color",
    "eye_color",
    "accessory",
    "bust_size",
)
BUST_KEYS = ("flat", "small", "medium", "large", "xlarge")
FORCED_NONE_ACCESSORY = "__none__"


def ensure_user_presets_dir():
    USER_PRESETS_DIR.mkdir(parents=True, exist_ok=True)
    return USER_PRESETS_DIR


def sanitize_preset_name(name):
    text = str(name or "").strip()
    text = INVALID_FILENAME_CHARS.sub("", text)
    text = re.sub(r"\s+", " ", text).strip().strip(".")
    return text or "oc_settings"


def normalize_settings_payload(candidate):
    candidate = dict(candidate or {})
    fixed = dict(candidate.get("fixed", {}))
    weights = dict(candidate.get("weights", {}))

    normalized = {
        "base_prompt": str(candidate.get("base_prompt", "") or "").strip(),
        "include_base_prompt": False,
        "preset": str(candidate.get("preset", SAFE_FALLBACK_PRESET) or SAFE_FALLBACK_PRESET),
        "fixed": {},
        "weights": {},
        "accessory_probability": clamp_probability(candidate.get("accessory_probability", 0.0), 0.0),
        "production_mode": bool(candidate.get("production_mode", True)),
    }

    if "include_base_prompt" in candidate:
        normalized["include_base_prompt"] = bool(candidate.get("include_base_prompt", False))
    else:
        normalized["include_base_prompt"] = bool(normalized["base_prompt"])

    for key in FIXED_CATEGORY_KEYS:
        value = fixed.get(key, "none")
        normalized["fixed"][key] = str(value if value not in (None, "") else "none")

    if normalized["fixed"]["accessory"] == FORCED_NONE_ACCESSORY:
        pass
    elif normalized["fixed"]["accessory"] in ("", "none", "null", "random"):
        normalized["fixed"]["accessory"] = "none"

    for key in BUST_KEYS:
        normalized["weights"][key] = clamp_probability(weights.get(key, 0.0), 0.0)

    return normalized


class SettingsPresetStore:
    def __init__(self, presets_dir=None):
        self.presets_dir = Path(presets_dir or USER_PRESETS_DIR)

    def ensure_dir(self):
        self.presets_dir.mkdir(parents=True, exist_ok=True)
        return self.presets_dir

    def list_presets(self):
        directory = self.ensure_dir()
        return sorted(path.stem for path in directory.glob("*.json"))

    def get_path(self, preset_name):
        safe_name = sanitize_preset_name(preset_name)
        return self.ensure_dir() / f"{safe_name}.json"

    def load(self, preset_name):
        path = self.get_path(preset_name)
        with path.open("r", encoding="utf-8") as handle:
            return normalize_settings_payload(json.load(handle))

    def save(self, preset_name, settings):
        path = self.get_path(preset_name)
        payload = normalize_settings_payload(settings)
        with path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        return {
            "name": path.stem,
            "path": str(path),
            "settings": payload,
        }

    def parse_settings_json(self, settings_json):
        try:
            payload = json.loads(str(settings_json or "{}"))
        except json.JSONDecodeError as error:
            raise ValueError(f"settings_json is not valid JSON: {error.msg}") from error

        if not isinstance(payload, dict):
            raise ValueError("settings_json must be a JSON object.")

        return normalize_settings_payload(payload)
