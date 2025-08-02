#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
画像ファイル変換ソフト GUI版 (Image File Converter GUI)
Windows用Python画像変換ツール - グラフィカルユーザーインターフェース
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from pathlib import Path
from image_converter import ImageConverter


class ImageConverterGUI:
    """画像変換GUI クラス"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("画像ファイル変換ソフト - Image File Converter")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # アイコン設定（オプション）
        try:
            # Windows用
            self.root.iconbitmap(default="icon.ico")
        except:
            pass
        
        self.converter = ImageConverter()
        self.setup_ui()
        
    def setup_ui(self):
        """UIセットアップ"""
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # ルートのグリッド設定
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # タイトル
        title_label = ttk.Label(main_frame, text="画像ファイル変換ソフト", 
                               font=("", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # モード選択
        mode_frame = ttk.LabelFrame(main_frame, text="変換モード", padding="10")
        mode_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        mode_frame.columnconfigure(1, weight=1)
        
        self.mode_var = tk.StringVar(value="single")
        ttk.Radiobutton(mode_frame, text="単一ファイル変換", variable=self.mode_var, 
                       value="single", command=self.on_mode_change).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="バッチ変換", variable=self.mode_var, 
                       value="batch", command=self.on_mode_change).grid(row=0, column=1, sticky=tk.W)
        
        # 入力設定
        input_frame = ttk.LabelFrame(main_frame, text="入力設定", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="入力:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_button = ttk.Button(input_frame, text="参照", command=self.browse_input)
        self.input_button.grid(row=0, column=2)
        
        # 出力設定
        output_frame = ttk.LabelFrame(main_frame, text="出力設定", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="出力:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_var = tk.StringVar()
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_var)
        self.output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.output_button = ttk.Button(output_frame, text="参照", command=self.browse_output)
        self.output_button.grid(row=0, column=2)
        
        # 変換オプション
        options_frame = ttk.LabelFrame(main_frame, text="変換オプション", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        
        # 出力形式
        ttk.Label(options_frame, text="出力形式:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                   values=["JPEG", "PNG", "BMP", "GIF", "TIFF", "WEBP"], 
                                   state="readonly", width=10)
        format_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        
        # 品質設定
        ttk.Label(options_frame, text="品質:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.quality_var = tk.IntVar(value=95)
        quality_spin = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.quality_var, width=10)
        quality_spin.grid(row=0, column=3, sticky=tk.W)
        
        # リサイズオプション
        resize_frame = ttk.Frame(options_frame)
        resize_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.resize_var = tk.BooleanVar()
        resize_check = ttk.Checkbutton(resize_frame, text="リサイズ", variable=self.resize_var,
                                      command=self.on_resize_toggle)
        resize_check.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        
        ttk.Label(resize_frame, text="幅:").grid(row=0, column=1, sticky=tk.W, padx=(0, 5))
        self.width_var = tk.IntVar(value=800)
        self.width_spin = ttk.Spinbox(resize_frame, from_=1, to=10000, textvariable=self.width_var, 
                                     width=8, state="disabled")
        self.width_spin.grid(row=0, column=2, padx=(0, 10))
        
        ttk.Label(resize_frame, text="高さ:").grid(row=0, column=3, sticky=tk.W, padx=(0, 5))
        self.height_var = tk.IntVar(value=600)
        self.height_spin = ttk.Spinbox(resize_frame, from_=1, to=10000, textvariable=self.height_var, 
                                      width=8, state="disabled")
        self.height_spin.grid(row=0, column=4)
        
        # 実行ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        self.convert_button = ttk.Button(button_frame, text="変換開始", command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="クリア", command=self.clear_fields)
        self.clear_button.pack(side=tk.LEFT)
        
        # プログレスバー
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, mode='indeterminate')
        self.progress_bar.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # ログ表示
        log_frame = ttk.LabelFrame(main_frame, text="変換ログ", padding="10")
        log_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(7, weight=1)
        
        self.log_text = ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 初期状態設定
        self.on_mode_change()
        
    def on_mode_change(self):
        """モード変更時の処理"""
        if self.mode_var.get() == "single":
            self.input_button.config(text="ファイル選択")
            self.output_button.config(text="保存先選択")
        else:
            self.input_button.config(text="フォルダ選択")
            self.output_button.config(text="出力フォルダ選択")
            
    def on_resize_toggle(self):
        """リサイズチェックボックス切り替え時の処理"""
        state = "normal" if self.resize_var.get() else "disabled"
        self.width_spin.config(state=state)
        self.height_spin.config(state=state)
        
    def browse_input(self):
        """入力ファイル/フォルダ選択"""
        if self.mode_var.get() == "single":
            file_path = filedialog.askopenfilename(
                title="変換するファイルを選択",
                filetypes=[
                    ("画像ファイル", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif *.webp"),
                    ("すべてのファイル", "*.*")
                ]
            )
            if file_path:
                self.input_var.set(file_path)
        else:
            folder_path = filedialog.askdirectory(title="入力フォルダを選択")
            if folder_path:
                self.input_var.set(folder_path)
                
    def browse_output(self):
        """出力ファイル/フォルダ選択"""
        if self.mode_var.get() == "single":
            file_path = filedialog.asksaveasfilename(
                title="保存先を選択",
                defaultextension=f".{self.format_var.get().lower()}",
                filetypes=[
                    ("JPEG", "*.jpg"),
                    ("PNG", "*.png"),
                    ("BMP", "*.bmp"),
                    ("GIF", "*.gif"),
                    ("TIFF", "*.tiff"),
                    ("WebP", "*.webp"),
                    ("すべてのファイル", "*.*")
                ]
            )
            if file_path:
                self.output_var.set(file_path)
        else:
            folder_path = filedialog.askdirectory(title="出力フォルダを選択")
            if folder_path:
                self.output_var.set(folder_path)
                
    def clear_fields(self):
        """フィールドクリア"""
        self.input_var.set("")
        self.output_var.set("")
        self.log_text.delete(1.0, tk.END)
        
    def log_message(self, message):
        """ログメッセージ表示"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def start_conversion(self):
        """変換開始"""
        if not self.input_var.get() or not self.output_var.get():
            messagebox.showerror("エラー", "入力と出力を指定してください")
            return
            
        # UIを無効化
        self.convert_button.config(state="disabled")
        self.progress_bar.start()
        self.log_text.delete(1.0, tk.END)
        
        # 別スレッドで変換実行
        thread = threading.Thread(target=self.run_conversion)
        thread.daemon = True
        thread.start()
        
    def run_conversion(self):
        """変換実行（別スレッド）"""
        try:
            input_path = self.input_var.get()
            output_path = self.output_var.get()
            quality = self.quality_var.get()
            resize = (self.width_var.get(), self.height_var.get()) if self.resize_var.get() else None
            
            if self.mode_var.get() == "single":
                # 単一ファイル変換
                self.log_message(f"変換開始: {input_path}")
                success = self.converter.convert_image(input_path, output_path, quality, resize)
                if success:
                    self.log_message("変換が完了しました！")
                    messagebox.showinfo("完了", "変換が完了しました！")
                else:
                    messagebox.showerror("エラー", "変換に失敗しました")
            else:
                # バッチ変換
                self.log_message(f"バッチ変換開始")
                self.log_message(f"入力フォルダ: {input_path}")
                self.log_message(f"出力フォルダ: {output_path}")
                self.log_message(f"出力形式: {self.format_var.get()}")
                
                # コンソール出力をキャプチャするため、一時的にprint関数を置き換え
                original_print = print
                def gui_print(*args, **kwargs):
                    message = ' '.join(str(arg) for arg in args)
                    self.root.after(0, lambda: self.log_message(message))
                
                import builtins
                builtins.print = gui_print
                
                try:
                    self.converter.batch_convert(input_path, output_path, 
                                               self.format_var.get(), quality, resize)
                    self.root.after(0, lambda: messagebox.showinfo("完了", "バッチ変換が完了しました！"))
                finally:
                    builtins.print = original_print
                    
        except Exception as e:
            error_msg = f"エラーが発生しました: {str(e)}"
            self.root.after(0, lambda: self.log_message(error_msg))
            self.root.after(0, lambda: messagebox.showerror("エラー", error_msg))
        finally:
            # UIを有効化
            self.root.after(0, self.conversion_finished)
            
    def conversion_finished(self):
        """変換完了時の処理"""
        self.progress_bar.stop()
        self.convert_button.config(state="normal")


def main():
    """GUI版メイン関数"""
    root = tk.Tk()
    app = ImageConverterGUI(root)
    
    # ウィンドウを画面中央に配置
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == '__main__':
    main()