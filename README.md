# Generate Original Character

ComfyUI custom nodes for generating original character base prompts from external data.

外部データから OC 素体向けプロンプトを生成する ComfyUI カスタムノード群です。

## Overview / 概要

This package provides four nodes:

- `Original Character Settings`
- `Generate Original Character`
- `Generate Original Character List`
- `Generate Original Character Simple`

このパッケージには次の4ノードが含まれます。

- `Original Character Settings`
- `Generate Original Character`
- `Generate Original Character List`
- `Generate Original Character Simple`

Recommended workflow / 推奨ワークフロー:

1. Build shared settings with `Original Character Settings`
2. Send them to `Generate Original Character` for single output
3. Or send them to `Generate Original Character List` for list output

1. `Original Character Settings` で共通設定を作る
2. 単発生成は `Generate Original Character` に渡す
3. リスト生成は `Generate Original Character List` に渡す

For onboarding, `Generate Original Character Simple` is also included as a one-node version.

導入用に、1ノード完結の `Generate Original Character Simple` も同梱しています。

## Features / 特徴

- Deterministic generation with `seed`
- Separate single and list generation nodes
- Shared settings node
- One-node simple variant
- Reproducible list generation with `seed + index`
- Fixed attribute support
- Weighted bust-size selection
- Accessory probability control
- External data files for easier extension
- `production_mode` support for filtering development-only entries

- `seed` による再現可能な生成
- 単発生成ノードと list 生成ノードの分離
- 共通設定ノード
- 1ノード完結の simple ノード
- `seed + index` による list 各要素の再現性
- 属性固定対応
- 胸サイズの重み付き選択
- アクセサリー出現率の調整
- データ定義を外部ファイル化
- `production_mode` による開発用候補の除外

## Installation / インストール

1. Copy this folder into `ComfyUI/custom_nodes/`.
2. Restart ComfyUI.
3. Reload the browser UI if needed.
4. Search for the node names above.

1. このフォルダを `ComfyUI/custom_nodes/` に入れます。
2. ComfyUI を再起動します。
3. 必要ならブラウザ UI を再読込します。
4. 上記ノード名で検索して使用します。

Recommended folder name / 推奨フォルダ名:

- `comfyui_generate_original_character`

## Included Files / 同梱ファイル

- `__init__.py`
- `nodes.py`
- `generator.py`
- `web/preset_sync.js`
- `data/base_prompt.json`
- `data/presets.json`
- `data/hair_styles.json`
- `data/hair_colors.json`
- `data/eye_colors.json`
- `data/accessories.json`
- `data/bust_sizes.json`
- `LICENSE`

## Node List / ノード一覧

### 1. `Original Character Settings`

Builds a reusable settings object for the generation nodes.

生成ノードに渡せる共通設定オブジェクトを作ります。

Inputs / 入力:

- `base_prompt`
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

Outputs / 出力:

- `settings`
- `settings_json`

### 2. `Generate Original Character`

Single-output generator that receives `settings`.

`settings` を受け取る単発生成ノードです。

Inputs / 入力:

- `seed`
- `settings`

Outputs / 出力:

- `prompt`
- `formatted_prompt`
- `name`
- `hair_style`
- `hair_color`
- `eye_color`
- `accessory`
- `bust_size`
- `metadata_json`

### 3. `Generate Original Character List`

List-output generator that receives `settings`.

`settings` を受け取る list 生成ノードです。

Inputs / 入力:

- `seed`
- `list_count`
- `settings`

Outputs / 出力:

- `prompt_list`
- `formatted_prompt_list`
- `name_list`
- `hair_style_list`
- `hair_color_list`
- `eye_color_list`
- `accessory_list`
- `bust_size_list`
- `metadata_list`

### 4. `Generate Original Character Simple`

One-node version for quick use.

手早く使うための 1 ノード完結版です。

Inputs / 入力:

- `seed`
- `output_mode`
- `list_count`
- all settings inputs from `Original Character Settings`

Outputs / 出力:

- single outputs
- list outputs
- `metadata_json`
- `metadata_list`

## Seed Reproducibility / seed 再現性

- The same `seed`, settings, and data files produce the same result.
- `Generate Original Character List` uses `seed + index`.
- `Generate Original Character Simple` also uses `seed + index` when `output_mode = list`.

- 同じ `seed`、同じ設定、同じデータであれば同じ結果を返します。
- `Generate Original Character List` は `seed + index` で各要素を生成します。
- `Generate Original Character Simple` でも `output_mode = list` 時は同様です。

## Presets / プリセット

Available presets / 利用可能プリセット:

- `Balanced`
- `Petite`
- `Curvy`
- `Statement`

Each preset defines:

- bust weights
- accessory probability

各プリセットは次を定義します。

- 胸サイズ重み
- アクセサリー出現率

`web/preset_sync.js` copies preset values into the numeric widgets for:

- `Original Character Settings`
- `Generate Original Character Simple`

`web/preset_sync.js` は次のノードで preset を数値欄へ反映します。

- `Original Character Settings`
- `Generate Original Character Simple`

## Priority Rules / 優先順位

Priority is shared across all generator surfaces.

優先順位はすべての生成ノードで共通です。

1. Fixed inputs have the highest priority.
2. `fixed_bust_size` overrides all bust weights.
3. `fixed_accessory` overrides `accessory_probability`.
4. `fixed_accessory = none` forces no accessory prompt.
5. Preset selection provides the baseline values.
6. Manual weight and probability edits after preset selection are the actual values used.

1. 固定入力が最優先です。
2. `fixed_bust_size` は胸サイズ重みより優先されます。
3. `fixed_accessory` は `accessory_probability` より優先されます。
4. `fixed_accessory = none` の場合はアクセサリー語を追加しません。
5. preset は基準値です。
6. preset 適用後に手動変更した weight / probability が最終的に使われる値です。

## Bust Size Behavior / 胸サイズ仕様

- Supported values: `flat`, `small`, `medium`, `large`, `xlarge`
- Weights are expected in the `0.00` to `1.00` range
- The total does not need to equal `1.00`
- Weights are normalized internally
- If the total is `0`, the node falls back to `Balanced`
- Fallback information is included in metadata

- 対応値: `flat`, `small`, `medium`, `large`, `xlarge`
- weight は `0.00` から `1.00` を想定します
- 合計が `1.00` である必要はありません
- ノード内部で正規化して使用します
- 合計が `0` の場合は `Balanced` にフォールバックします
- フォールバック情報は metadata に含まれます

## Accessory Behavior / アクセサリー仕様

- `accessory_probability` is the probability of generating an accessory
- `none` is always treated as `1 - p`
- On failure, no accessory prompt is added
- On success, one accessory is selected from the accessory pool

- `accessory_probability` は「アクセサリーあり」の確率です
- `none` は常に `1 - p` として扱われます
- 失敗時はアクセサリー語を追加しません
- 成功時のみ候補から1件選択します

## Base Prompt / ベースプロンプト

- `base_prompt` is a direct setting input
- If `base_prompt` is empty, the packaged default from `data/base_prompt.json` is used

- `base_prompt` は設定入力です
- 空の場合は `data/base_prompt.json` の既定値を使います

## Formatted Prompt Format / formatted_prompt 形式

```text
name: ...
positive: ...
negative:

----------
```

## Data Extension / データ拡張

Edit or add JSON files under `data/`.

`data/` 以下の JSON を編集または追加してください。

Supported option fields / 対応フィールド:

- `key`
- `prompt`
- `label`
- `name`
- `developmentOnly`

Plain strings are also supported for simple entries.

単純な候補なら文字列だけでも定義できます。

## production_mode and developmentOnly / production_mode と developmentOnly

- `production_mode = true` excludes entries marked with `developmentOnly: true`
- `production_mode = false` includes them
- If a fixed value targets a filtered entry, the node falls back to normal selection

- `production_mode = true` では `developmentOnly: true` の候補を除外します
- `production_mode = false` ではそれらも含めます
- 固定値が除外対象を指していた場合は通常選択へフォールバックします

## Known Limitations / 既知の制約

- If the frontend extension does not load, preset selection alone will not rewrite current numeric widget values.
- `metadata_list` is returned as a list of JSON strings.
- v1 does not include separate data-validator or preview nodes.

- フロントエンド拡張が読み込まれない場合、preset 変更だけでは数値ウィジェットへ反映されません。
- `metadata_list` は JSON 文字列のリストとして返します。
- v1 にはデータ検証専用ノードやプレビュー専用ノードは含まれていません。

## License / ライセンス

This package is released under the MIT License.

このパッケージは MIT License で公開しています。
