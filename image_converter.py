#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像ファイル変換ソフト (Image File Converter)
Windows用Python画像変換ツール

対応フォーマット: JPEG, PNG, BMP, GIF, TIFF, WebP
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image, ImageOps
import argparse


class ImageConverter:
    """画像変換クラス"""
    
    SUPPORTED_FORMATS = {
        'JPEG': ['.jpg', '.jpeg'],
        'PNG': ['.png'],
        'BMP': ['.bmp'],
        'GIF': ['.gif'],
        'TIFF': ['.tiff', '.tif'],
        'WEBP': ['.webp']
    }
    
    def __init__(self):
        self.processed_files = 0
        self.failed_files = 0
        
    def get_supported_extensions(self) -> List[str]:
        """サポートされている拡張子のリストを取得"""
        extensions = []
        for format_exts in self.SUPPORTED_FORMATS.values():
            extensions.extend(format_exts)
        return extensions
    
    def is_supported_format(self, file_path: str) -> bool:
        """ファイルがサポートされている形式かチェック"""
        ext = Path(file_path).suffix.lower()
        return ext in self.get_supported_extensions()
    
    def convert_image(self, input_path: str, output_path: str, 
                     quality: int = 95, resize: Optional[Tuple[int, int]] = None) -> bool:
        """
        画像を変換する
        
        Args:
            input_path: 入力ファイルパス
            output_path: 出力ファイルパス
            quality: JPEG品質 (1-100)
            resize: リサイズサイズ (width, height) またはNone
            
        Returns:
            bool: 変換成功時True、失敗時False
        """
        try:
            # 入力ファイルの存在確認
            if not os.path.exists(input_path):
                print(f"エラー: 入力ファイルが見つかりません: {input_path}")
                return False
            
            # 出力ディレクトリの作成
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 画像を開く
            with Image.open(input_path) as img:
                # EXIF情報に基づく自動回転
                img = ImageOps.exif_transpose(img)
                
                # リサイズ処理
                if resize:
                    img = img.resize(resize, Image.Resampling.LANCZOS)
                
                # 出力形式の決定
                output_ext = Path(output_path).suffix.lower()
                
                # PNG以外の場合、透明度を処理
                if output_ext in ['.jpg', '.jpeg', '.bmp']:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # 白背景で透明度を合成
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                
                # 保存設定
                save_kwargs = {}
                if output_ext in ['.jpg', '.jpeg']:
                    save_kwargs['quality'] = quality
                    save_kwargs['optimize'] = True
                elif output_ext == '.png':
                    save_kwargs['optimize'] = True
                elif output_ext == '.webp':
                    save_kwargs['quality'] = quality
                    save_kwargs['method'] = 6  # 最高品質の圧縮
                
                # 画像を保存
                img.save(output_path, **save_kwargs)
                
            print(f"変換完了: {input_path} -> {output_path}")
            self.processed_files += 1
            return True
            
        except Exception as e:
            print(f"変換エラー ({input_path}): {str(e)}")
            self.failed_files += 1
            return False
    
    def batch_convert(self, input_dir: str, output_dir: str, 
                     output_format: str, quality: int = 95,
                     resize: Optional[Tuple[int, int]] = None) -> None:
        """
        バッチ変換
        
        Args:
            input_dir: 入力ディレクトリ
            output_dir: 出力ディレクトリ
            output_format: 出力形式 (例: 'PNG', 'JPEG')
            quality: JPEG品質
            resize: リサイズサイズ
        """
        if not os.path.exists(input_dir):
            print(f"エラー: 入力ディレクトリが見つかりません: {input_dir}")
            return
        
        # 出力拡張子を決定
        format_extensions = {
            'JPEG': '.jpg',
            'PNG': '.png',
            'BMP': '.bmp',
            'GIF': '.gif',
            'TIFF': '.tiff',
            'WEBP': '.webp'
        }
        
        output_ext = format_extensions.get(output_format.upper(), '.png')
        
        # 入力ディレクトリ内の画像ファイルを取得
        input_files = []
        for ext in self.get_supported_extensions():
            pattern = f"*{ext}"
            input_files.extend(Path(input_dir).glob(pattern))
            input_files.extend(Path(input_dir).glob(pattern.upper()))
        
        if not input_files:
            print(f"変換対象の画像ファイルが見つかりません: {input_dir}")
            return
        
        print(f"バッチ変換開始: {len(input_files)}ファイル")
        print(f"出力形式: {output_format.upper()}")
        if resize:
            print(f"リサイズ: {resize[0]}x{resize[1]}")
        
        # 各ファイルを変換
        for input_file in input_files:
            output_filename = input_file.stem + output_ext
            output_path = os.path.join(output_dir, output_filename)
            self.convert_image(str(input_file), output_path, quality, resize)
        
        print(f"\nバッチ変換完了!")
        print(f"成功: {self.processed_files}ファイル")
        if self.failed_files > 0:
            print(f"失敗: {self.failed_files}ファイル")


def main():
    """コマンドライン実行用メイン関数"""
    parser = argparse.ArgumentParser(
        description='画像ファイル変換ソフト - Image File Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 単一ファイル変換
  python image_converter.py input.jpg output.png
  
  # バッチ変換
  python image_converter.py --batch input_dir output_dir --format PNG
  
  # リサイズ付き変換
  python image_converter.py input.jpg output.jpg --resize 800 600
  
  # 品質指定変換
  python image_converter.py input.png output.jpg --quality 85
        """
    )
    
    parser.add_argument('input', help='入力ファイルまたはディレクトリ')
    parser.add_argument('output', help='出力ファイルまたはディレクトリ')
    parser.add_argument('--batch', action='store_true', 
                       help='バッチ変換モード')
    parser.add_argument('--format', default='PNG',
                       choices=['JPEG', 'PNG', 'BMP', 'GIF', 'TIFF', 'WEBP'],
                       help='出力形式 (バッチモード時)')
    parser.add_argument('--quality', type=int, default=95, 
                       help='JPEG品質 (1-100)')
    parser.add_argument('--resize', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                       help='リサイズサイズ (幅 高さ)')
    
    args = parser.parse_args()
    
    # 引数の検証
    if args.quality < 1 or args.quality > 100:
        print("エラー: 品質は1-100の間で指定してください")
        return 1
    
    converter = ImageConverter()
    
    try:
        if args.batch:
            # バッチ変換
            resize = tuple(args.resize) if args.resize else None
            converter.batch_convert(args.input, args.output, args.format, 
                                  args.quality, resize)
        else:
            # 単一ファイル変換
            if not converter.is_supported_format(args.input):
                print(f"エラー: サポートされていない形式です: {args.input}")
                print(f"サポート形式: {', '.join(converter.get_supported_extensions())}")
                return 1
            
            resize = tuple(args.resize) if args.resize else None
            success = converter.convert_image(args.input, args.output, 
                                            args.quality, resize)
            return 0 if success else 1
            
    except KeyboardInterrupt:
        print("\n変換が中断されました")
        return 1
    except Exception as e:
        print(f"予期しないエラー: {str(e)}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())