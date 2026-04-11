from .generator import DataCatalog, OriginalCharacterGenerator
from .preset_store import SettingsPresetStore


CATALOG = DataCatalog()
GENERATOR = OriginalCharacterGenerator(CATALOG)
PRESET_STORE = SettingsPresetStore()
SETTINGS_TYPE = "OC_GENERATOR_SETTINGS"
NODE_CATEGORY = "OC Generator"
NODE_KEY_SETTINGS = "OC Generator Settings"
NODE_KEY_SHOW_SETTINGS = "OC Generator Show Settings"
NODE_KEY_SAVE_SETTINGS_JSON = "OC Generator Save Settings JSON"
NODE_KEY_LOAD_PRESET = "OC Generator Load Settings Preset"
NODE_KEY_GENERATE = "OC Generator Generate Character"
NODE_KEY_GENERATE_LIST = "OC Generator Generate Character List"
NODE_KEY_GENERATE_SIMPLE = "OC Generator Generate Character Simple"


def settings_input_spec():
    balanced = CATALOG.get_preset("Balanced")
    return {
        "base_prompt": ("STRING", {"default": CATALOG.default_base_prompt, "multiline": True}),
        "include_base_prompt": ("BOOLEAN", {"default": False}),
        "preset": (list(CATALOG.preset_names), {"default": "Balanced"}),
        "fixed_hair_style": (list(CATALOG.get_fixed_choices("hairStyle")), {"default": "none"}),
        "fixed_hair_color": (list(CATALOG.get_fixed_choices("hairColor")), {"default": "none"}),
        "fixed_eye_color": (list(CATALOG.get_fixed_choices("eyeColor")), {"default": "none"}),
        "fixed_accessory": (list(CATALOG.get_fixed_choices("accessory")), {"default": "none"}),
        "fixed_bust_size": (list(CATALOG.get_bust_choices()), {"default": "none"}),
        "weight_flat": ("FLOAT", {"default": balanced["bust_weights"]["flat"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "weight_small": ("FLOAT", {"default": balanced["bust_weights"]["small"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "weight_medium": ("FLOAT", {"default": balanced["bust_weights"]["medium"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "weight_large": ("FLOAT", {"default": balanced["bust_weights"]["large"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "weight_xlarge": ("FLOAT", {"default": balanced["bust_weights"]["xlarge"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "accessory_probability": ("FLOAT", {"default": balanced["accessory_probability"], "min": 0.0, "max": 1.0, "step": 0.01}),
        "production_mode": ("BOOLEAN", {"default": True}),
    }


def build_settings_payload(kwargs):
    return GENERATOR.build_settings(**kwargs)


def single_result_tuple(result):
    return (
        result["prompt"],
        result["formatted_prompt"],
        result["name"],
        result["hair_style"],
        result["hair_color"],
        result["eye_color"],
        result["accessory"],
        result["bust_size"],
        result["metadata_json"],
    )


def list_result_tuple(results):
    return (
        [result["prompt"] for result in results],
        [result["formatted_prompt"] for result in results],
        [result["name"] for result in results],
        [result["hair_style"] for result in results],
        [result["hair_color"] for result in results],
        [result["eye_color"] for result in results],
        [result["accessory"] for result in results],
        [result["bust_size"] for result in results],
        [result["metadata_json"] for result in results],
    )


class OriginalCharacterSettings:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "build"
    RETURN_TYPES = (SETTINGS_TYPE, "STRING")
    RETURN_NAMES = ("settings", "settings_json")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": settings_input_spec(),
        }

    def build(self, **kwargs):
        settings = build_settings_payload(kwargs)
        return (settings, GENERATOR.settings_to_json(settings))


class GenerateOriginalCharacter:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "generate"
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "prompt",
        "formatted_prompt",
        "name",
        "hair_style",
        "hair_color",
        "eye_color",
        "accessory",
        "bust_size",
        "metadata_json",
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "settings": (SETTINGS_TYPE,),
            }
        }

    def generate(self, seed, settings):
        return single_result_tuple(GENERATOR.generate_from_settings(seed, settings))


class GenerateOriginalCharacterList:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "generate"
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "prompt_list",
        "formatted_prompt_list",
        "name_list",
        "hair_style_list",
        "hair_color_list",
        "eye_color_list",
        "accessory_list",
        "bust_size_list",
        "metadata_list",
    )
    OUTPUT_IS_LIST = (
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    )

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
                "list_count": ("INT", {"default": 4, "min": 1, "max": 256}),
                "settings": (SETTINGS_TYPE,),
            }
        }

    def generate(self, seed, list_count, settings):
        return list_result_tuple(GENERATOR.generate_list_from_settings(seed, list_count, settings))


class GenerateOriginalCharacterSimple:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "generate"
    RETURN_TYPES = (
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "prompt",
        "formatted_prompt",
        "name",
        "hair_style",
        "hair_color",
        "eye_color",
        "accessory",
        "bust_size",
        "prompt_list",
        "formatted_prompt_list",
        "name_list",
        "hair_style_list",
        "hair_color_list",
        "eye_color_list",
        "accessory_list",
        "bust_size_list",
        "metadata_json",
        "metadata_list",
    )
    OUTPUT_IS_LIST = (
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
        True,
    )

    @classmethod
    def INPUT_TYPES(cls):
        required = {
            "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            "output_mode": (["single", "list"], {"default": "single"}),
            "list_count": ("INT", {"default": 1, "min": 1, "max": 256}),
        }
        required.update(settings_input_spec())
        return {"required": required}

    def generate(self, seed, output_mode, list_count, **kwargs):
        settings = build_settings_payload(kwargs)
        results = GENERATOR.generate_list_from_settings(
            seed=seed,
            list_count=list_count if output_mode == "list" else 1,
            settings=settings,
        )
        first = results[0]
        return (
            first["prompt"],
            first["formatted_prompt"],
            first["name"],
            first["hair_style"],
            first["hair_color"],
            first["eye_color"],
            first["accessory"],
            first["bust_size"],
            [result["prompt"] for result in results],
            [result["formatted_prompt"] for result in results],
            [result["name"] for result in results],
            [result["hair_style"] for result in results],
            [result["hair_color"] for result in results],
            [result["eye_color"] for result in results],
            [result["accessory"] for result in results],
            [result["bust_size"] for result in results],
            first["metadata_json"],
            [result["metadata_json"] for result in results],
        )


class LoadOriginalCharacterSettingsPreset:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "load"
    RETURN_TYPES = (SETTINGS_TYPE, "STRING")
    RETURN_NAMES = ("settings", "settings_json")

    @classmethod
    def INPUT_TYPES(cls):
        preset_names = PRESET_STORE.list_presets()
        if not preset_names:
            preset_names = ["(no presets found)"]

        return {
            "required": {
                "preset_name": (preset_names, {"default": preset_names[0]}),
            }
        }

    def load(self, preset_name):
        if preset_name == "(no presets found)":
            raise ValueError("No saved OC settings presets were found in user_presets.")

        settings = PRESET_STORE.load(preset_name)
        return (settings, GENERATOR.settings_to_json(settings))


class ShowOriginalCharacterSettings:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "show"
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("settings_json", "settings_summary")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "settings": (SETTINGS_TYPE,),
            }
        }

    def show(self, settings):
        payload = dict(settings or {})
        fixed = dict(payload.get("fixed", {}))
        weights = dict(payload.get("weights", {}))
        summary = "\n".join(
            [
                f"base_prompt: {payload.get('base_prompt', '')}",
                f"include_base_prompt: {bool(payload.get('include_base_prompt', False))}",
                f"preset: {payload.get('preset', 'Balanced')}",
                f"production_mode: {bool(payload.get('production_mode', True))}",
                "fixed:",
                f"  hair_style: {fixed.get('hair_style', 'none')}",
                f"  hair_color: {fixed.get('hair_color', 'none')}",
                f"  eye_color: {fixed.get('eye_color', 'none')}",
                f"  accessory: {fixed.get('accessory', 'none')}",
                f"  bust_size: {fixed.get('bust_size', 'none')}",
                "weights:",
                f"  flat: {weights.get('flat', 0.0):.2f}",
                f"  small: {weights.get('small', 0.0):.2f}",
                f"  medium: {weights.get('medium', 0.0):.2f}",
                f"  large: {weights.get('large', 0.0):.2f}",
                f"  xlarge: {weights.get('xlarge', 0.0):.2f}",
                f"accessory_probability: {float(payload.get('accessory_probability', 0.0)):.2f}",
            ]
        )
        return (GENERATOR.settings_to_json(payload), summary)


class SaveOriginalCharacterSettingsJson:
    CATEGORY = NODE_CATEGORY
    FUNCTION = "save"
    OUTPUT_NODE = True
    RETURN_TYPES = (SETTINGS_TYPE, "STRING", "STRING", "STRING")
    RETURN_NAMES = ("settings", "settings_json", "saved_name", "saved_path")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "settings_json": ("STRING", {"multiline": True, "default": "{}"}),
                "file_name": ("STRING", {"default": "oc_settings"}),
                "save_enabled": ("BOOLEAN", {"default": True}),
            }
        }

    def save(self, settings_json, file_name, save_enabled):
        settings = PRESET_STORE.parse_settings_json(settings_json)
        normalized_json = GENERATOR.settings_to_json(settings)
        saved_name = ""
        saved_path = ""

        if save_enabled:
            saved = PRESET_STORE.save(file_name, settings)
            saved_name = saved["name"]
            saved_path = saved["path"]

        return (settings, normalized_json, saved_name, saved_path)


NODE_CLASS_MAPPINGS = {
    NODE_KEY_SETTINGS: OriginalCharacterSettings,
    NODE_KEY_SHOW_SETTINGS: ShowOriginalCharacterSettings,
    NODE_KEY_SAVE_SETTINGS_JSON: SaveOriginalCharacterSettingsJson,
    NODE_KEY_LOAD_PRESET: LoadOriginalCharacterSettingsPreset,
    NODE_KEY_GENERATE: GenerateOriginalCharacter,
    NODE_KEY_GENERATE_LIST: GenerateOriginalCharacterList,
    NODE_KEY_GENERATE_SIMPLE: GenerateOriginalCharacterSimple,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_KEY_SETTINGS: "OC Generator / Settings",
    NODE_KEY_SHOW_SETTINGS: "OC Generator / Show Settings",
    NODE_KEY_SAVE_SETTINGS_JSON: "OC Generator / Save Settings JSON",
    NODE_KEY_LOAD_PRESET: "OC Generator / Load Settings Preset",
    NODE_KEY_GENERATE: "OC Generator / Generate Character",
    NODE_KEY_GENERATE_LIST: "OC Generator / Generate Character List",
    NODE_KEY_GENERATE_SIMPLE: "OC Generator / Generate Character Simple",
}
