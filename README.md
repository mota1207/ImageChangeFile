# 画像ファイル変換ソフト - Image File Converter

Windows用Python画像変換ツール

## 概要

様々な画像形式を相互変換できるPython製のソフトウェアです。コマンドライン版とGUI版の両方を提供しています。

## 主な機能

- **多形式対応**: JPEG, PNG, BMP, GIF, TIFF, WebP
- **単一ファイル変換**: 1つのファイルを指定形式に変換
- **バッチ変換**: フォルダ内の全画像を一括変換
- **ドラッグ&ドロップ**: 画像ファイルを直接ドラッグ&ドロップで変換
- **リサイズ機能**: 変換時に画像サイズを変更
- **品質調整**: JPEG/WebP形式の圧縮品質を調整
- **EXIF対応**: 回転情報に基づく自動補正
- **GUI版**: 使いやすいグラフィカルインターフェース

## システム要件

- Windows 7/8/10/11
- Python 3.7以上
- Pillow ライブラリ
- tkinterdnd2 ライブラリ（ドラッグ&ドロップ機能用）

## インストール

### 1. Pythonのインストール
[Python公式サイト](https://www.python.org/downloads/)からPython 3.7以上をダウンロードしてインストール

### 2. 必要ライブラリのインストール
```bash
pip install -r requirements.txt
```

または
```bash
pip install Pillow tkinterdnd2
```

## 使用方法

### GUI版（推奨）

1. `run_gui.bat` をダブルクリック
2. または、コマンドプロンプトで以下を実行：
```bash
python image_converter_gui.py
```

#### GUI版の使い方
1. **変換モード**を選択（単一ファイル／バッチ変換）
2. **入力**欄で変換元ファイル/フォルダを指定
   - **ファイル選択**: 「参照」ボタンをクリックして選択
   - **ドラッグ&ドロップ**: ドロップエリアに画像ファイルを直接ドラッグ&ドロップ
3. **出力**欄で保存先を指定
4. **変換オプション**を設定：
   - 出力形式: JPEG, PNG, BMP, GIF, TIFF, WebP
   - 品質: 1-100（JPEG/WebP用）
   - リサイズ: 幅×高さ（オプション）
5. **変換開始**ボタンをクリック

### コマンドライン版

#### 基本的な使用法
```bash
# 単一ファイル変換
python image_converter.py input.jpg output.png

# バッチ変換（フォルダ内全ファイル）
python image_converter.py --batch input_folder output_folder --format PNG

# リサイズ付き変換
python image_converter.py input.jpg output.jpg --resize 800 600

# 品質指定変換
python image_converter.py input.png output.jpg --quality 85
```

#### コマンドラインオプション
```
python image_converter.py [入力] [出力] [オプション]

位置引数:
  input                 入力ファイルまたはディレクトリ
  output                出力ファイルまたはディレクトリ

オプション:
  --batch               バッチ変換モード
  --format FORMAT       出力形式 (JPEG/PNG/BMP/GIF/TIFF/WEBP)
  --quality QUALITY     JPEG品質 (1-100、デフォルト: 95)
  --resize WIDTH HEIGHT リサイズサイズ (幅 高さ)
  -h, --help           ヘルプを表示
```

## 使用例

### 単一ファイル変換
```bash
# JPEGをPNGに変換
python image_converter.py photo.jpg photo.png

# 高品質JPEG変換
python image_converter.py image.png image.jpg --quality 95

# リサイズ付き変換
python image_converter.py large.jpg small.jpg --resize 400 300
```

### バッチ変換
```bash
# フォルダ内全ファイルをPNGに変換
python image_converter.py photos/ converted/ --batch --format PNG

# WebP形式で一括変換（品質80）
python image_converter.py input/ output/ --batch --format WEBP --quality 80

# リサイズ付きバッチ変換
python image_converter.py photos/ thumbnails/ --batch --format JPEG --resize 200 200
```

## 対応形式

| 形式 | 拡張子 | 読み込み | 書き込み | 備考 |
|------|--------|----------|----------|------|
| JPEG | .jpg, .jpeg | ✓ | ✓ | 品質調整可能 |
| PNG | .png | ✓ | ✓ | 透明度対応 |
| BMP | .bmp | ✓ | ✓ | Windows標準 |
| GIF | .gif | ✓ | ✓ | アニメーション非対応 |
| TIFF | .tiff, .tif | ✓ | ✓ | 高品質保存 |
| WebP | .webp | ✓ | ✓ | 品質調整可能 |

## 特徴

### ドラッグ&ドロップ機能
- **直感的な操作**: 画像ファイルを直接ドロップエリアにドラッグ&ドロップ
- **視覚的フィードバック**: ドラッグ中に色とボーダーが変化
- **自動ファイル検証**: サポートされている画像形式のみ受け入れ
- **モード対応**: 単一ファイル・バッチ変換の両方で利用可能

### 画像処理機能
- **EXIF自動回転**: 撮影時の向き情報に基づく自動回転
- **透明度処理**: PNG → JPEG変換時の白背景合成
- **高品質リサイズ**: Lanczosアルゴリズム使用

### エラーハンドリング
- 入力ファイルの存在確認
- 出力ディレクトリの自動作成
- 詳細なエラーメッセージ表示
- 変換統計情報の表示

## トラブルシューティング

### よくある問題

1. **「Pythonが見つかりません」エラー**
   - Pythonが正しくインストールされているか確認
   - PATHが設定されているか確認

2. **「Pillowがインストールされていません」エラー**
   ```bash
   pip install Pillow tkinterdnd2
   ```

3. **「ドラッグ&ドロップ機能は利用できません」メッセージ**
   ```bash
   pip install tkinterdnd2
   ```

4. **「ファイルが開けません」エラー**
   - ファイルパスが正しいか確認
   - ファイルが使用中でないか確認
   - 対応形式かどうか確認

5. **GUI版が起動しない**
   - tkinterがインストールされているか確認（通常はPythonに同梱）
   - コマンドライン版を試してみる

## ライセンス

このソフトウェアはMITライセンスのもとで公開されています。

## 作者

画像ファイル変換ソフト開発チーム

## 更新履歴

- v1.0.0 (2024) - 初回リリース
  - GUI版とCLI版を同梱
  - 主要画像形式に対応
  - バッチ変換機能
  - リサイズ機能
- v1.1.0 (2024) - ドラッグ&ドロップ機能追加
  - 画像ファイルのドラッグ&ドロップ変換
  - 視覚的フィードバック
  - 自動ファイル形式検証
