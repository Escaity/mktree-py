# mktree.py

テキストファイルに記述されたツリー構造から、実際のディレクトリとファイルを一括生成します。

プロジェクトの初期セットアップや、定型的なディレクトリ構造の複製を自動化します。

## 特徴

- **正確な階層解析**: 正規表現を用いてインデントを正確に計算するため、全角スペースや特殊な空白文字が含まれていても、見た目通りの階層構造を正確に再現します。
- **ルートディレクトリの無視**: 構造ファイルの 1 行目がルートディレクトリの場合、そのディレクトリ自体は作成せず、中身だけを現在の場所に展開します。
- **柔軟な書式対応**: `├──` や `└──` といった罫線の種類や有無に影響されません。
- **コメント対応**: `#` から始まる行や、行の途中からのコメントを無視します。
- **コマンドラインツール**: macOS や Linux 環境で、どこからでも呼び出せるコマンドとして設定可能です。

---

## 要件

- Python 3

---

## インストール (macOS / Linux)

スクリプトをシステムのどこからでも `mktree` コマンドとして実行できるように設定します。

1. **実行権限の付与**
   ターミナルで以下のコマンドを実行します。

   ```bash
   chmod +x mktree.py
   ```

2. **PATH への配置**
   スクリプトを PATH が通っているディレクトリにコピーします。

   ```bash
   # `sudo` を使うためパスワードが必要です
   sudo cp mktree.py /usr/local/bin/mktree
   ```

これで、新しいターミナルウィンドウを開けば、どこからでも `mktree` コマンドが使用できます。

---

## 使い方

1. 作成したいディレクトリ構造を記述したテキストファイル（例: `my-project.txt`）を用意します。

2. ターミナルで以下のコマンドを実行します。

   ```bash
   mktree my-project.txt
   ```

### 入力ファイルの書式

- 1 行に 1 つのファイルまたはディレクトリを記述します。
- **ディレクトリ**は、名前の末尾に必ずスラッシュ `/` を付けてください。
- 階層の深さは、行頭のインデント（空白や罫線）で表現します。
- ルートディレクトリは無視されます。

**書式例 (`my-project.txt`):**

```
# ルートディレクトリ（この行は無視され、中身だけが作成されます）
my-awesome-app/
    ├── README.md
    ├── package.json
    │
    └── src/
        ├── components/
        │   └── Button.jsx
        └── index.js
```

上記の例を実行すると、`my-awesome-app/` は作成されず、`README.md` や `src/` などが現在のディレクトリ直下に作成されます。

---

## 設定

スクリプト冒頭にある `INDENT_WIDTH` の値を変更することで、インデント 1 階層あたりの文字数を調整できます（デフォルトは 4）。

```python
# 1階層あたりのインデント文字数
INDENT_WIDTH = 4
```
