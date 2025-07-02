#!/usr/bin/env python3
# ==============================================================================
# Description: 正規表現を用いてインデントを正確に計算し、
#              ルートディレクトリを無視してディレクトリツリーを生成する。
# Usage: python3 mktree.py <path_to_structure_file>
# ==============================================================================
import argparse
import re
from pathlib import Path

# --- 設定 ---
INDENT_WIDTH = 4

def create_structure_from_file(filepath: str):
    """テキストファイルからディレクトリ構造を生成する"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: ファイルが見つかりません: {filepath}")
        return
    except Exception as e:
        print(f"❌ Error: An error occurred: {e}")
        return

    path_stack = []
    base_path = Path.cwd()

    level_offset = 0          # 階層レベルを調整するためのオフセット値
    first_line_processed = False # 最初の行を処理したかどうかのフラグ

    for line_num, line in enumerate(lines, 1):
        line_content = line.split('#')[0].rstrip()

        if not line_content.strip():
            continue

        match = re.search(r'[^ │├└─\s]', line_content)
        if not match:
            continue

        indentation = match.start()
        name = line_content[indentation:]
        level = indentation // INDENT_WIDTH

        # 最初の有効な行の処理
        if not first_line_processed:
            first_line_processed = True
            # もし最初の行がレベル0のディレクトリなら、それを無視してレベルオフセットを1に設定
            if level == 0 and name.endswith('/'):
                level_offset = 1
                continue # この行の処理をスキップして次の行へ

        # 決定されたオフセットをレベルから引く
        level -= level_offset
        if level < 0: level = 0 # 安全装置

        while len(path_stack) > level:
            path_stack.pop()

        parent_path = base_path.joinpath(*path_stack) if path_stack else base_path
        full_path = parent_path.joinpath(name.rstrip('/'))

        try:
            if name.endswith('/'):
                print(f"📁 Creating Directory: {full_path}")
                full_path.mkdir(parents=True, exist_ok=True)
                path_stack.append(name.rstrip('/'))
            else:
                print(f"📄 Creating File:      {full_path}")
                full_path.parent.mkdir(parents=True, exist_ok=True)
                full_path.touch()
        except OSError as e:
            print(f"❌ Error on line {line_num}: Could not create {full_path}. Reason: {e}")

    print("\n✅ Structure creation complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="テキストファイルからディレクトリ構造を生成します。")
    parser.add_argument("filepath", help="ディレクトリツリーが書かれたテキストファイルのパス")
    args = parser.parse_args()
    create_structure_from_file(args.filepath)