# comfyui-original-character-generator

![Platform](https://img.shields.io/badge/Platform-ComfyUI%20Node-1f2937?style=flat-square)
![Category](https://img.shields.io/badge/Category-OC%20Generator-2563eb?style=flat-square)
![Nodes](https://img.shields.io/badge/Nodes-7%20Included-0f766e?style=flat-square)
![Settings](https://img.shields.io/badge/Settings-JSON%20Ready-f59e0b?style=flat-square)
![Presets](https://img.shields.io/badge/Presets-user__presets-7c3aed?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-374151?style=flat-square)

オリジナルキャラクター向けのプロンプト生成と、再利用できる設定管理のための ComfyUI カスタムノードです。

**Languages:** [English](README.md) | [日本語](README_ja.md) | [한국어](README_ko.md) | [简体中文](README_zh-CN.md)

## スクリーンショット

### ワークフロー全体

![Workflow overview](docs/images/workflow-overview.png)

### 保存済み Settings Preset

![Saved preset](docs/images/settings-preset.png)

## 作例

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

### ワークフローからの出力例

<p align="center">
  <img src="examples/ComfyUI_00001_.png" alt="Workflow render sample 01" width="30%" />
  <img src="examples/ComfyUI_00002_.png" alt="Workflow render sample 02" width="30%" />
  <img src="examples/ComfyUI_00003_.png" alt="Workflow render sample 03" width="30%" />
</p>
<p align="center">
  <img src="examples/ComfyUI_00004_.png" alt="Workflow render sample 04" width="30%" />
  <img src="examples/ComfyUI_00005_.png" alt="Workflow render sample 05" width="30%" />
</p>

その他の作例は [`examples/`](examples) にあります。

## まず Web 版で試す

ブラウザで先に試したい場合は、こちらの Web 版を使えます。

- [original-character-generator-web](https://nade-eaf4fc.github.io/original-character-generator-web/)

Web 版では、この ComfyUI ノードと互換性のある `settings_json` を書き出せます。

## 既存ユーザーへのお知らせ

最近の更新により、既存の workflow がそのままでは動かず、ノードの再接続や更新が必要になる場合があります。

ご不便をおかけして申し訳ありません。早い段階で clone して試してくださった方々、本当にありがとうございます。

## 特徴

- 再利用可能な設定オブジェクトからオリジナルキャラクターのプロンプトを生成
- 髪型、髪色、瞳色、アクセサリー、胸サイズを固定可能
- 胸サイズの重みとアクセサリー出現率を調整可能
- `user_presets` で `settings_json` の保存と読み込みが可能
- 専用の `Show Settings` ノードで設定内容を確認可能
- サンプル workflow とサンプル preset を同梱

## 導入方法

### 方法 1: フォルダを直接入れる

1. このリポジトリのフォルダを `ComfyUI/custom_nodes/` に置きます。
2. ComfyUI を再起動します。
3. ノードメニューで `OC Generator` を検索します。

### 方法 2: git clone

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/nade-eaf4fc/comfyui-original-character-generator.git
```

clone 後に ComfyUI を再起動してください。

## 含まれるノード

現在のノード構成は以下のとおりです。

- `OC Generator / Settings`
- `OC Generator / Show Settings`
- `OC Generator / Save Settings JSON`
- `OC Generator / Load Settings Preset`
- `OC Generator / Generate Character`
- `OC Generator / Generate Character List`
- `OC Generator / Generate Character Simple`

### `OC Generator / Settings`

再利用可能な設定オブジェクトを作成し、同時に `settings_json` も出力します。

入力:

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

出力:

- `settings`
- `settings_json`

### `OC Generator / Show Settings`

設定内容を読みやすいサマリーとして表示します。

出力:

- `settings_summary`

### `OC Generator / Save Settings JSON`

`settings_json` を解析し、必要に応じて `user_presets` に保存したうえで、再利用可能な `settings` オブジェクトを出力します。

入力:

- `settings_json`
- `file_name`
- `save_enabled`

出力:

- `settings`
- `settings_json`
- `saved_name`
- `saved_path`

### `OC Generator / Load Settings Preset`

`user_presets` ディレクトリから保存済み preset を読み込みます。

出力:

- `settings`
- `settings_json`

### `OC Generator / Generate Character`

`settings` オブジェクトから 1 件の結果を生成します。

出力:

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

`settings` オブジェクトから複数件の結果を生成します。

出力:

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

すぐ使いたい方向けの 1 ノード版です。設定入力をまとめて持ち、単体結果またはリスト結果を出力できます。

## Preset と保存設定

組み込み preset:

- `Balanced`
- `Petite`
- `Curvy`
- `Statement`

保存済み preset ファイルの保存先:

- `user_presets/*.json`

サンプル preset:

- [`user_presets/example_soft_violet.json`](user_presets/example_soft_violet.json)

付属の Web UI から出力した互換 `settings_json` も、このノードセットに読み込めます。

## サンプルファイル

Workflow サンプル:

- [`workflows/oc-generator-basic-workflow_simple_and_list.json`](workflows/oc-generator-basic-workflow_simple_and_list.json)
- [`workflows/oc-generator-soft-violet-preset-workflow.json`](workflows/oc-generator-soft-violet-preset-workflow.json)

画像サンプル:

- [`examples`](examples)

## 動作メモ

- 同じ `seed`、同じ settings、同じ data ファイルであれば、同じ結果になります。
- リスト生成では `seed + index` を使います。
- 胸サイズの重みは `0.00` から `1.00` の値をそのまま入れられ、内部で正規化されます。
- `include_base_prompt = false` の場合、生成結果からベースプロンプトを除外します。
- `include_base_prompt = true` かつ `base_prompt` が空の場合、既定のベースプロンプトを使います。
- 胸サイズの重みがすべて `0` の場合、`Balanced` preset の分布にフォールバックします。
- `fixed_bust_size` を指定すると、重みによる胸サイズ選択よりそちらが優先されます。
- `fixed_accessory` に具体的なアクセサリーを指定すると、アクセサリー出現率よりそちらが優先されます。
- ノード UI 上での `fixed_accessory = none` は「固定なし」を意味します。
- Web 連携で保存された `settings_json` では、「アクセサリーを必ずなしにする」専用状態も扱えます。
- `production_mode = true` にすると、`developmentOnly: true` の項目は候補から除外されます。

## データ拡張

`data/` 配下の JSON ファイルを編集してください。

- `data/base_prompt.json`
- `data/presets.json`
- `data/hair_styles.json`
- `data/hair_colors.json`
- `data/eye_colors.json`
- `data/accessories.json`
- `data/bust_sizes.json`

サポートされている項目:

- `key`
- `prompt`
- `label`
- `name`
- `developmentOnly`

カテゴリファイルでは、単純な文字列配列も使えます。

## Acknowledgements

Built with development assistance from OpenAI Codex, powered by GPT-5.4.

## License

This package is released under the MIT License.
