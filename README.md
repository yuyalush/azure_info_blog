# ☁️ Azure Tech Blog

Azureに関する最新情報・公式ブログ・注目のGitHubリポジトリをご紹介する技術ブログです。  
[Hugo](https://gohugo.io/) + [PaperMod](https://github.com/adityatelange/hugo-PaperMod) テーマで構築し、GitHub Pages で公開しています。

🌐 **公開URL**: https://yuyalush.github.io/azure_info_blog/

---

## 📂 ディレクトリ構成

```
azure_info_blog/
├── .github/
│   └── workflows/
│       ├── deploy.yml          # mainへのpushで自動ビルド・デプロイ
│       └── daily-news.yml      # 毎日9:00 JSTにAzureニュースを自動生成・投稿
├── content/
│   └── posts/                  # ブログ記事（Markdown）
├── scripts/
│   └── generate_weekly_news.py # Azureデイリーニュース自動生成スクリプト
├── themes/
│   └── PaperMod/               # Hugo テーマ（git submodule）
└── hugo.toml                   # Hugo 設定ファイル
```

---

## 🚀 GitHub Pages 自動デプロイ

`main` ブランチへのプッシュをトリガーに、GitHub Actions が自動でブログをビルド・公開します。

```
main にプッシュ
  └─▶ deploy.yml が起動
        ├─ Hugo でビルド (hugo --minify)
        └─ GitHub Pages へデプロイ
```

**ワークフロー**: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

---

## 📰 Azureデイリーニュース自動生成

毎日 **9:00 JST** に GitHub Actions が自動で前日のAzure最新情報をまとめた記事を生成・投稿します。

### 実行フロー

```
毎日 9:00 JST（cron: 0 0 * * *）
  └─▶ weekly-news.yml が起動
        ├─① Azure公式RSSフィードを取得（前日分）
        │     - https://azure.microsoft.com/en-us/blog/feed/
        │     - https://azure.microsoft.com/en-us/updates/feed/
        ├─② GitHub Models API（gpt-4o-mini）で日本語記事を自動生成
        │     ※ API利用不可時はRSSデータをそのまま整形（フォールバック）
        ├─③ Hugo Markdown形式で記事ファイルを生成
        │     → content/posts/azure-news-YYYY-MM-DD.md
        ├─④ リポジトリへコミット・プッシュ
        └─⑤ Hugo ビルド → GitHub Pages デプロイ
```

**ワークフロー**: [`.github/workflows/daily-news.yml`](.github/workflows/daily-news.yml)  
**スクリプト**: [`scripts/generate_weekly_news.py`](scripts/generate_weekly_news.py)

### 手動実行

GitHub の **Actions** タブ → **Azureデイリーニュース自動生成・公開** → **Run workflow** から手動実行できます。

---

## 🛠️ ローカル開発

### 前提条件

- [Hugo](https://gohugo.io/installation/) (extended版)
- Git

### セットアップ

```bash
git clone --recurse-submodules https://github.com/yuyalush/azure_info_blog.git
cd azure_info_blog
```

### ローカルプレビュー

```bash
hugo server -D
```

ブラウザで http://localhost:1313 を開きます。

### 記事の追加

```bash
hugo new posts/my-article.md
```

`content/posts/my-article.md` が生成されます。`draft: false` に変更すると公開対象になります。

---

## 📝 記事フォーマット

```markdown
---
title: "記事タイトル"
date: 2026-04-06
draft: false
tags:
  - "Azure"
  - "タグ名"
categories:
  - "カテゴリ名"
description: "記事の説明文"
---

本文をここに書きます。
```

---

## ⚙️ 技術スタック

| 項目 | 内容 |
|------|------|
| 静的サイトジェネレーター | [Hugo](https://gohugo.io/) |
| テーマ | [PaperMod](https://github.com/adityatelange/hugo-PaperMod) |
| ホスティング | [GitHub Pages](https://pages.github.com/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) |
| AI記事生成 | [GitHub Models](https://github.com/marketplace/models) (gpt-4o-mini) |
| 言語 | 日本語 |
