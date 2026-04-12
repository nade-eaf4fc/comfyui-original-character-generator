# comfyui-original-character-generator

![Platform](https://img.shields.io/badge/Platform-ComfyUI%20Node-1f2937?style=flat-square)
![Category](https://img.shields.io/badge/Category-OC%20Generator-2563eb?style=flat-square)
![Nodes](https://img.shields.io/badge/Nodes-7%20Included-0f766e?style=flat-square)
![Settings](https://img.shields.io/badge/Settings-JSON%20Ready-f59e0b?style=flat-square)
![Presets](https://img.shields.io/badge/Presets-user__presets-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-374151?style=flat-square)

这是一个用于生成原创角色提示词并管理可复用设置的 ComfyUI 自定义节点包。

**Languages:** [English](README.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [简体中文](README_zh-CN.md)

## 截图

### 工作流总览

![Workflow overview](docs/images/workflow-overview.png)

### 已保存的 Settings Preset

![Saved preset](docs/images/settings-preset.png)

## 示例输出

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

### 工作流渲染示例

<p align="center">
  <img src="examples/ComfyUI_00001_.png" alt="Workflow render sample 01" width="30%" />
  <img src="examples/ComfyUI_00002_.png" alt="Workflow render sample 02" width="30%" />
  <img src="examples/ComfyUI_00003_.png" alt="Workflow render sample 03" width="30%" />
</p>
<p align="center">
  <img src="examples/ComfyUI_00004_.png" alt="Workflow render sample 04" width="30%" />
  <img src="examples/ComfyUI_00005_.png" alt="Workflow render sample 05" width="30%" />
</p>

更多示例请查看 [`examples/`](examples)。

## 先试用 Web 版本

如果你想先在浏览器里试用生成器，可以使用这里的 Web 版本：

- [original-character-generator-web](https://nade-eaf4fc.github.io/original-character-generator-web/)

该 Web 应用可以导出与此 ComfyUI 节点集兼容的 `settings_json` 文件。

## 给现有用户的说明

最近的一些更新可能会导致现有工作流无法直接运行，或者需要重新连接节点。

很抱歉带来不便，也感谢所有已经 clone 并尝试过这个项目的朋友。

## 功能

- 通过可复用的 settings 对象生成原创角色提示词
- 可固定发型、发色、瞳色、配饰和胸围尺寸
- 可调整胸围尺寸权重分布和配饰出现概率
- 可在 `user_presets` 中保存和加载 `settings_json`
- 可使用专用的 `Show Settings` 节点查看设置摘要
- 附带示例工作流和示例 preset 数据

## 安装

### 方法 1：直接复制文件夹

1. 将此仓库文件夹放入 `ComfyUI/custom_nodes/`。
2. 重启 ComfyUI。
3. 在节点菜单中搜索 `OC Generator`。

### 方法 2：git clone

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/nade-eaf4fc/comfyui-original-character-generator.git
```

clone 之后请重启 ComfyUI。

## 包含的节点

当前节点集如下：

- `OC Generator / Settings`
- `OC Generator / Show Settings`
- `OC Generator / Save Settings JSON`
- `OC Generator / Load Settings Preset`
- `OC Generator / Generate Character`
- `OC Generator / Generate Character List`
- `OC Generator / Generate Character Simple`

### `OC Generator / Settings`

构建一个可复用的 settings 对象，同时输出 `settings_json`。

输入：

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

输出：

- `settings`
- `settings_json`

### `OC Generator / Show Settings`

以易读的摘要形式显示当前设置。

输出：

- `settings_summary`

### `OC Generator / Save Settings JSON`

解析 `settings_json` 字符串，可选择将其保存到 `user_presets`，并输出一个可复用的 `settings` 对象。

输入：

- `settings_json`
- `file_name`
- `save_enabled`

输出：

- `settings`
- `settings_json`
- `saved_name`
- `saved_path`

### `OC Generator / Load Settings Preset`

从 `user_presets` 目录加载已保存的 preset。

输出：

- `settings`
- `settings_json`

### `OC Generator / Generate Character`

根据一个 `settings` 对象生成单个结果。

输出：

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

根据一个 `settings` 对象生成多个结果。

输出：

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

适合快速使用的单节点版本。它包含相同的设置输入，并可输出单个结果或列表结果。

## Preset 与已保存设置

内置 preset：

- `Balanced`
- `Petite`
- `Curvy`
- `Statement`

保存的 preset 文件位置：

- `user_presets/*.json`

示例 preset：

- [`user_presets/example_soft_violet.json`](user_presets/example_soft_violet.json)

配套的 Web UI 也可以导出兼容的 `settings_json`，并导入到这组节点中使用。

## 示例文件

工作流示例：

- [`workflows/oc-generator-basic-workflow_simple_and_list.json`](workflows/oc-generator-basic-workflow_simple_and_list.json)
- [`workflows/oc-generator-soft-violet-preset-workflow.json`](workflows/oc-generator-soft-violet-preset-workflow.json)

图像示例：

- [`examples`](examples)

## 行为说明

- 相同的 `seed`、settings 和 data 文件会生成相同的结果。
- 列表生成使用 `seed + index`。
- 胸围尺寸权重可直接输入 `0.00` 到 `1.00` 范围内的值，内部会自动归一化。
- `include_base_prompt = false` 时，生成结果中不会包含基础提示词。
- 如果 `include_base_prompt = true` 且 `base_prompt` 为空，则会使用默认基础提示词。
- 如果所有胸围尺寸权重都为 `0`，则会回退到 `Balanced` preset 分布。
- `fixed_bust_size` 的优先级高于基于权重的胸围尺寸选择。
- 当 `fixed_accessory` 指定了具体配饰时，它的优先级高于配饰概率设置。
- 在节点 UI 中，`fixed_accessory = none` 表示不固定配饰。
- 通过 Web 集成保存的 `settings_json` 还支持“强制无配饰”的特殊状态。
- `production_mode = true` 会隐藏标记为 `developmentOnly: true` 的条目。

## 扩展数据

请编辑 `data/` 下的 JSON 文件：

- `data/base_prompt.json`
- `data/presets.json`
- `data/hair_styles.json`
- `data/hair_colors.json`
- `data/eye_colors.json`
- `data/accessories.json`
- `data/bust_sizes.json`

支持的字段：

- `key`
- `prompt`
- `label`
- `name`
- `developmentOnly`

分类文件中也支持简单的字符串条目。

## Acknowledgements

Built with development assistance from OpenAI Codex, powered by GPT-5.4.

## License

This package is released under the MIT License.
