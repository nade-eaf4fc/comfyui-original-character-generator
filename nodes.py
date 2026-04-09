from .generator import DataCatalog, OriginalCharacterGenerator


CATALOG = DataCatalog()
GENERATOR = OriginalCharacterGenerator(CATALOG)
SETTINGS_TYPE = "OC_CHARACTER_SETTINGS"


def settings_input_spec():
    balanced = CATALOG.get_preset("Balanced")
    return {
        "base_prompt": ("STRING", {"default": CATALOG.default_base_prompt, "multiline": True}),
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
    CATEGORY = "OC"
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
    CATEGORY = "OC"
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
    CATEGORY = "OC"
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
    CATEGORY = "OC"
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


NODE_CLASS_MAPPINGS = {
    "Original Character Settings": OriginalCharacterSettings,
    "Generate Original Character": GenerateOriginalCharacter,
    "Generate Original Character List": GenerateOriginalCharacterList,
    "Generate Original Character Simple": GenerateOriginalCharacterSimple,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Original Character Settings": "Original Character Settings",
    "Generate Original Character": "Generate Original Character",
    "Generate Original Character List": "Generate Original Character List",
    "Generate Original Character Simple": "Generate Original Character Simple",
}
