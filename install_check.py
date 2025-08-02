#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
インストールと依存関係チェックスクリプト
Installation and dependency check script
"""

import sys
import subprocess
import importlib.util
import os


def check_python_version():
    """Python バージョンをチェック"""
    if sys.version_info < (3, 7):
        print("エラー: Python 3.7以上が必要です")
        print(f"現在のバージョン: {sys.version}")
        return False
    print(f"✓ Python バージョン OK: {sys.version.split()[0]}")
    return True


def check_module(module_name):
    """モジュールの存在確認"""
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def install_pillow():
    """Pillow のインストール"""
    print("Pillowをインストールしています...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow>=10.0.0"])
        print("✓ Pillow のインストールが完了しました")
        return True
    except subprocess.CalledProcessError:
        print("✗ Pillow のインストールに失敗しました")
        return False


def check_tkinter():
    """tkinter の確認"""
    try:
        import tkinter
        print("✓ tkinter が利用可能です")
        return True
    except ImportError:
        print("✗ tkinter が見つかりません")
        print("  Windows: 通常はPythonに含まれています")
        print("  Linux: sudo apt install python3-tk")
        print("  macOS: brew install python-tk")
        return False


def test_image_conversion():
    """画像変換のテスト"""
    try:
        from PIL import Image
        print("✓ 画像変換機能のテスト中...")
        
        # テスト画像を作成
        test_img = Image.new('RGB', (100, 100), color='red')
        test_img.save('test_install.png')
        
        # 変換テスト
        test_img.save('test_install.jpg', quality=90)
        
        # クリーンアップ
        os.remove('test_install.png')
        os.remove('test_install.jpg')
        
        print("✓ 画像変換機能が正常に動作します")
        return True
    except Exception as e:
        print(f"✗ 画像変換テストに失敗: {e}")
        return False


def main():
    """メイン関数"""
    print("=== 画像ファイル変換ソフト インストールチェック ===")
    print()
    
    all_ok = True
    
    # Python バージョンチェック
    if not check_python_version():
        all_ok = False
    
    # Pillow チェック・インストール
    if not check_module("PIL"):
        print("Pillow が見つかりません。インストールを試みます...")
        if not install_pillow():
            all_ok = False
    else:
        try:
            import PIL
            print(f"✓ Pillow が利用可能です (バージョン: {PIL.__version__})")
        except:
            print("✓ Pillow がインストールされています")
    
    # tkinter チェック
    if not check_tkinter():
        print("  注意: GUI版は動作しませんが、CLI版は利用可能です")
    
    # 機能テスト
    if not test_image_conversion():
        all_ok = False
    
    print()
    if all_ok:
        print("🎉 すべての依存関係が満たされています！")
        print()
        print("使用方法:")
        print("  CLI版: python image_converter.py --help")
        if check_module("tkinter"):
            print("  GUI版: python image_converter_gui.py")
            print("         または run_gui.bat をダブルクリック")
    else:
        print("❌ いくつかの問題があります。上記のエラーを確認してください。")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())