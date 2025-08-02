@echo off
chcp 65001 > nul
echo 画像ファイル変換ソフト - Image File Converter
echo.

REM インストールチェックを実行
echo 依存関係をチェックしています...
python install_check.py
if errorlevel 1 (
    echo.
    echo インストールに問題があります。install_check.py の出力を確認してください。
    pause
    exit /b 1
)

echo.
echo GUI版を起動しています...
python image_converter_gui.py

if errorlevel 1 (
    echo.
    echo GUI版の起動に失敗しました。コマンドライン版を試してください。
    echo 使用方法: python image_converter.py [入力ファイル] [出力ファイル]
    pause
)