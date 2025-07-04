#!/usr/bin/env python3
# ==============================================================================
# mktree.py (出力先指定機能付き)
# ------------------------------------------------------------------------------
# Description: 正規表現を用いてインデントを正確に計算し、
#              生成先のディレクトリを指定できる最終版。
# Usage: python3 mktree.py <structure_file> [-o <output_path>]
# ==============================================================================
import argparse
import re
from pathlib import Path

# --- 設定 ---
INDENT_WIDTH = 4

def create_structure_from_file(filepath: str, output_dir: str | None = None):
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

    # 出力先パスが指定されていればそれを基準に、なければ現在の場所を基準にする
    if output_dir:
        base_path = Path(output_dir)
        # もし指定された出力先ディレクトリが存在しなければ、それも作成する
        base_path.mkdir(parents=True, exist_ok=True)
        print(f"➡️  Output directory set to: {base_path.resolve()}")
    else:
        base_path = Path.cwd()

    path_stack = []
    level_offset = 0
    first_line_processed = False

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

        if not first_line_processed:
            first_line_processed = True
            if level == 0 and name.endswith('/'):
                level_offset = 1
                continue

        level -= level_offset
        if level < 0: level = 0

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
    # 必須の引数 (構造ファイル)
    parser.add_argument("filepath", help="ディレクトリツリーが書かれたテキストファイルのパス")

    # オプションの引数 (出力先)
    parser.add_argument(
        "-o", "--output",
        help="生成先のディレクトリパス。省略した場合は現在のディレクトリに作成します。",
        default=None # デフォルトはNone（指定なし）
    )
    args = parser.parse_args()

    # メイン関数に引数を渡す
    create_structure_from_file(args.filepath, args.output)