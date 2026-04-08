#!/usr/bin/env python3
"""Azure週次ニュース記事を自動生成するスクリプト

GitHub Models API (gpt-4o-mini) でAzure公式RSSフィードを日本語まとめ記事に変換し、
Hugo用Markdownファイルとして出力します。
"""

import datetime
import os
import re
import sys

import feedparser
from openai import OpenAI

AZURE_FEEDS = [
    "https://azure.microsoft.com/en-us/blog/feed/",
    "https://azure.microsoft.com/en-us/updates/feed/",
]

GITHUB_MODELS_ENDPOINT = "https://models.inference.ai.azure.com"
MODEL_NAME = "gpt-4o-mini"


def get_week_range():
    """先週の月曜〜日曜の日付範囲を返す"""
    today = datetime.date.today()
    last_monday = today - datetime.timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + datetime.timedelta(days=6)
    return last_monday, last_sunday


def fetch_entries(feed_url, start_date, end_date):
    """RSS feedから指定期間のエントリを取得"""
    try:
        feed = feedparser.parse(feed_url)
        result = []
        for entry in feed.entries:
            pub_date = None
            for attr in ("published_parsed", "updated_parsed"):
                t = getattr(entry, attr, None)
                if t:
                    pub_date = datetime.date(*t[:3])
                    break
            if pub_date and start_date <= pub_date <= end_date:
                summary = re.sub(r"<[^>]+>", "", entry.get("summary", ""))[:400].strip()
                result.append({
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "summary": summary,
                    "published": pub_date.isoformat(),
                })
        return result
    except Exception as e:
        print(f"Warning: {feed_url} の取得失敗: {e}", file=sys.stderr)
        return []


def generate_with_ai(entries, start_date, end_date, github_token):
    """GitHub Models API (gpt-4o-mini) で日本語記事を生成"""
    client = OpenAI(base_url=GITHUB_MODELS_ENDPOINT, api_key=github_token)

    period = f"{start_date.strftime('%Y年%m月%d日')}〜{end_date.strftime('%Y年%m月%d日')}"
    news_text = "\n".join(
        f"- [{e['title']}]({e['link']}) ({e['published']})\n  {e['summary']}"
        for e in entries[:30]
    )

    prompt = f"""あなたはAzureの技術情報を日本語でまとめる専門ブログライターです。
以下の{period}のAzure公式情報を元に、日本語のAzureウィークリーニュース記事を作成してください。

## 収集した情報
{news_text}

## 出力要件
- 完全に日本語で書く
- Hugo Markdown形式で本文のみ出力（front matterは含めない）
- 冒頭に「今週のハイライト」を箇条書きで3〜5件まとめる
- 続いてカテゴリ別（AI・機械学習、コンピューティング、セキュリティ、開発ツール、その他）に整理
- 各ニュースを2〜3文で日本語要約し、元記事リンクを必ず付ける
- エンジニア向けの簡潔・実用的な文体で書く
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.7,
    )
    return response.choices[0].message.content


def generate_simple(entries, start_date, end_date):
    """AIなしのシンプルなフォールバック記事生成"""
    period = f"{start_date.strftime('%Y年%m月%d日')}〜{end_date.strftime('%Y年%m月%d日')}"

    if not entries:
        return (
            f"今週（{period}）はAzureの主要アップデートが見つかりませんでした。\n\n"
            "最新情報は下記公式サイトをご確認ください。\n\n"
            "- [Azure ブログ](https://azure.microsoft.com/ja-jp/blog/)\n"
            "- [Azure アップデート](https://azure.microsoft.com/ja-jp/updates/)\n"
        )

    lines = [
        f"今週（{period}）のAzure最新情報をまとめてお届けします。\n",
        "## 今週のアップデート\n",
    ]
    for e in entries:
        lines.append(f"### [{e['title']}]({e['link']})")
        lines.append(f"*公開日: {e['published']}*\n")
        if e["summary"]:
            lines.append(f"{e['summary']}\n")
    lines += [
        "---",
        "*この記事は自動生成されました。詳細は各リンク先をご確認ください。*",
    ]
    return "\n".join(lines)


def build_post(body, start_date, end_date):
    """Hugo front matter + 本文を組み合わせてファイルパスと内容を返す"""
    period_start = start_date.strftime("%Y年%m月%d日")
    period_end = end_date.strftime("%Y年%m月%d日")
    today = datetime.date.today().isoformat()
    filepath = f"content/posts/azure-weekly-{start_date.strftime('%Y-%m-%d')}.md"

    front_matter = f"""---
title: "Azureウィークリーニュース（{period_start}〜{period_end}）"
date: {today}
draft: false
tags:
  - "Azure"
  - "週次ニュース"
  - "アップデート"
categories:
  - "週次ニュース"
description: "{period_start}〜{period_end}のAzure最新情報をまとめてお届けします。"
---
"""
    return filepath, front_matter + body


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN が設定されていません", file=sys.stderr)
        sys.exit(1)

    start, end = get_week_range()
    print(f"対象期間: {start} 〜 {end}")

    entries = []
    for url in AZURE_FEEDS:
        batch = fetch_entries(url, start, end)
        print(f"  {len(batch)}件 <- {url}")
        entries.extend(batch)

    # 重複除去（リンクで判定）
    seen: set[str] = set()
    unique = []
    for e in entries:
        if e["link"] not in seen:
            seen.add(e["link"])
            unique.append(e)
    print(f"取得完了: {len(unique)}件（重複除去後）")

    body = None
    if unique:
        try:
            print("GitHub Models API で記事生成中...")
            body = generate_with_ai(unique, start, end, token)
            print("AI生成完了")
        except Exception as e:
            print(f"Warning: AI生成失敗 ({e})、シンプル形式にフォールバック")

    if body is None:
        body = generate_simple(unique, start, end)

    filepath, content = build_post(body, start, end)

    if os.path.exists(filepath):
        print(f"スキップ（既存）: {filepath}")
        return

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"記事作成: {filepath}")

    # GitHub Actions の出力変数に設定
    gha_output = os.environ.get("GITHUB_OUTPUT")
    if gha_output:
        with open(gha_output, "a") as f:
            f.write(f"filepath={filepath}\n")


if __name__ == "__main__":
    main()
