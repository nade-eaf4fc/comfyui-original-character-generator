# comfyui-original-character-generator

![Platform](https://img.shields.io/badge/Platform-ComfyUI%20Node-1f2937?style=flat-square)
![Category](https://img.shields.io/badge/Category-OC%20Generator-2563eb?style=flat-square)
![Nodes](https://img.shields.io/badge/Nodes-7%20Included-0f766e?style=flat-square)
![Settings](https://img.shields.io/badge/Settings-JSON%20Ready-f59e0b?style=flat-square)
![Presets](https://img.shields.io/badge/Presets-user__presets-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-374151?style=flat-square)

ComfyUI custom nodes for generating original character prompts and reusable settings.

## Screenshots

### Workflow Overview

![Workflow overview](docs/images/workflow-overview.png)

### Saved Settings Preset

![Saved preset](docs/images/settings-preset.png)

## Sample Outputs

<p align="center">
  <img src="examples/original-character-example-01.png" alt="Original character example 01" width="30%" />
  <img src="examples/original-character-example-02.png" alt="Original character example 02" width="30%" />
  <img src="examples/original-character-example-03.png" alt="Original character example 03" width="30%" />
</p>
<p align="center">
  <img src="examples/original-character-example-04.png" alt="Original character example 04" width="30%" />
  <img src="examples/original-character-example-05.png" alt="Original character example 05" width="30%" />
  <img src="examples/original-character-example-06.png" alt="Original character example 06" width="30%" />
</p>

More examples are available in [`examples/`](examples).

## Try the Web Version

If you want to try the generator in your browser first, use the web version here:

- [original-character-generator-web](https://nade-eaf4fc.github.io/original-character-generator-web/)

The web app can export compatible `settings_json` files for this ComfyUI node set.

## Features

- Generate original character prompts from reusable settings objects
- Use fixed attributes for hair style, hair color, eye color, accessory, and bust size
- Adjust weighted bust-size distribution and accessory probability
- Save and load `settings_json` presets from `user_presets`
- Inspect settings with a dedicated `Show Settings` node
- Use included sample workflows and sample preset data

## Installation

### Option 1: Download or copy the folder

1. Place this repository folder inside `ComfyUI/custom_nodes/`.
2. Restart ComfyUI.
3. Search for `OC Generator` in the node menu.

### Option 2: git clone

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/nade-eaf4fc/comfyui-original-character-generator.git
```

After cloning, restart ComfyUI.

## Included Nodes

The current node set is:

- `OC Generator / Settings`
- `OC Generator / Show Settings`
- `OC Generator / Save Settings JSON`
- `OC Generator / Load Settings Preset`
- `OC Generator / Generate Character`
- `OC Generator / Generate Character List`
- `OC Generator / Generate Character Simple`

### `OC Generator / Settings`

Builds a reusable settings object and also outputs `settings_json`.

Inputs:

- `base_prompt`
- `include_base_prompt`
- `preset`
- `fixed_hair_style`
- `fixed_hair_color`
- `fixed_eye_color`
- `fixed_accessory`
- `fixed_bust_size`
- `weight_flat`
- `weight_small`
- `weight_medium`
- `weight_large`
- `weight_xlarge`
- `accessory_probability`
- `production_mode`

Outputs:

- `settings`
- `settings_json`

### `OC Generator / Show Settings`

Displays a settings object as raw `settings_json` and a readable text summary.

Outputs:

- `settings_json`
- `settings_summary`

### `OC Generator / Save Settings JSON`

Parses a `settings_json` string, optionally saves it into `user_presets`, and outputs a reusable `settings` object.

Inputs:

- `settings_json`
- `file_name`
- `save_enabled`

Outputs:

- `settings`
- `settings_json`
- `saved_name`
- `saved_path`

### `OC Generator / Load Settings Preset`

Loads a saved preset from the `user_presets` directory.

Outputs:

- `settings`
- `settings_json`

### `OC Generator / Generate Character`

Generates one result from a `settings` object.

Outputs:

- `prompt`
- `formatted_prompt`
- `name`
- `hair_style`
- `hair_color`
- `eye_color`
- `accessory`
- `bust_size`
- `metadata_json`

### `OC Generator / Generate Character List`

Generates multiple results from a `settings` object.

Outputs:

- `prompt_list`
- `formatted_prompt_list`
- `name_list`
- `hair_style_list`
- `hair_color_list`
- `eye_color_list`
- `accessory_list`
- `bust_size_list`
- `metadata_list`

### `OC Generator / Generate Character Simple`

One-node version for quick use. It includes the same setting inputs and can output either a single result or a list.

## Presets and Saved Settings

Built-in presets:

- `Balanced`
- `Petite`
- `Curvy`
- `Statement`

Saved preset files are stored in:

- `user_presets/*.json`

Sample preset:

- [`user_presets/example_soft_violet.json`](user_presets/example_soft_violet.json)

The companion web UI can export compatible `settings_json` files that can be imported into this node set.

## Example Files

Workflow examples:

- [`workflows/oc-generator-basic-workflow.json`](workflows/oc-generator-basic-workflow.json)
- [`workflows/oc-generator-soft-violet-preset-workflow.json`](workflows/oc-generator-soft-violet-preset-workflow.json)

Image examples:

- [`examples`](examples)

## Behavior Notes

- The same `seed`, settings, and data files will produce the same result.
- List generation uses `seed + index`.
- Bust weights accept raw values in the `0.00` to `1.00` range and are normalized internally.
- `include_base_prompt = false` omits the base prompt from generated output.
- If `include_base_prompt = true` and `base_prompt` is empty, the default base prompt is used.
- If all bust weights are `0`, generation falls back to the `Balanced` preset distribution.
- `fixed_bust_size` overrides weighted bust selection.
- `fixed_accessory` overrides accessory probability when a concrete accessory is selected.
- `fixed_accessory = none` means no fixed accessory in the node UI.
- The special forced-no-accessory state is supported through saved `settings_json` data from the web integration.
- `production_mode = true` hides entries marked with `developmentOnly: true`.

## Extending Data

Edit the JSON files under `data/`:

- `data/base_prompt.json`
- `data/presets.json`
- `data/hair_styles.json`
- `data/hair_colors.json`
- `data/eye_colors.json`
- `data/accessories.json`
- `data/bust_sizes.json`

Supported option fields:

- `key`
- `prompt`
- `label`
- `name`
- `developmentOnly`

Simple string entries are also supported in category files.

## Acknowledgements

Built with development assistance from OpenAI Codex, powered by GPT-5.4.

## License

This package is released under the MIT License.
