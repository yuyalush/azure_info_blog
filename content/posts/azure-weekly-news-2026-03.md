---
title: "【Azureウィークリーニュース】2026年3月末リリースの主要アップデートまとめ"
date: 2026-04-06T09:00:00+09:00
description: "2026年3月最終週にリリースされたAzureの主要アップデートをまとめてご紹介します。AKS、Cosmos DB、Azure Firewall、AI Foundryなど多岐にわたる重要な更新情報をお届けします。"
tags: ["Azure", "週次ニュース", "AKS", "Cosmos DB", "AI", "Bicep", "Azure Firewall"]
categories: ["ウィークリーニュース"]
showToc: true
TocOpen: false
draft: false
---

## はじめに

毎週月曜日は、先週リリースされた注目の Azure アップデートをまとめてお届けします。
2026年3月最終週は、インフラ・AI・セキュリティの各分野で多くの重要なアップデートがありました。

---

## 🚀 注目のアップデート

### 1. AKS Blue-Green エージェントプールアップグレード（パブリックプレビュー）

Azure Kubernetes Service (AKS) に **Blue-Green アップグレード**が追加されました。
従来のインプレースアップグレードに比べ、並列エージェントプールを作成して検証してから切り替えるため、リスクを大幅に軽減できます。

**主なメリット:**
- ダウンタイムなしでのクラスターアップグレードが可能
- 問題発生時の迅速なロールバック
- 本番ワークロードへの影響を最小化

👉 [AKS ドキュメント](https://learn.microsoft.com/ja-jp/azure/aks/)

---

### 2. Cosmos DB ミラーリング in Microsoft Fabric（プライベートエンドポイント対応・GA）

**Cosmos DB の Fabric ミラーリング**がプライベートエンドポイントに対応し、一般提供（GA）となりました。
金融・医療など厳格なネットワーク分離が必要な業界でも、安全にリアルタイム分析が可能になります。

**主な特徴:**
- プライベートネットワーク内でのセキュアな分析
- 仮想ネットワーク制限のサポート
- 規制産業向けコンプライアンス強化

👉 [Microsoft Fabric ドキュメント](https://learn.microsoft.com/ja-jp/fabric/)

---

### 3. Azure Database for MySQL の Fabric ミラーリング（パブリックプレビュー）

MySQL の運用データをほぼリアルタイムで Microsoft Fabric にレプリケートできるようになりました。
手動での ETL パイプライン構築が不要になり、データエンジニアリングの工数を大幅に削減できます。

---

### 4. Bicep Snapshot コマンド（GA）

長らく待望されていた **Bicep の `snapshot` コマンド**が一般提供になりました。
インフラのデプロイ前にプレビュー・検証が可能になり、変更レビューや承認ワークフロー、デバッグが格段に楽になります。

```bash
# Bicep snapshot の使用例
az deployment group what-if \
  --resource-group myRG \
  --template-file main.bicep
```

---

### 5. Azure Firewall ドラフト＆デプロイ（GA）

**Azure Firewall のドラフトモード**が一般提供となりました。
ファイアウォール設定をドラフト状態で変更・テスト・検証してから本番へコミットできるため、「本番でのテスト」リスクを排除できます。

---

### 6. 機密 VM 新シリーズ

データ利用中のセキュリティを強化する新 VM シリーズが発表されました：

| シリーズ | 特徴 |
|---|---|
| DCesv6 | 機密コンピューティング最適化 |
| DCedsv6 | ローカルディスク付き機密 VM |
| ECesv6 | メモリ最適化機密 VM |
| ECedsv6 | ローカルディスク付きメモリ最適化 |

---

### 7. Azure AI Foundry 新モデル統合

Azure AI Foundry に複数の最新 AI モデルが追加されました：

- **Grok 4.0** — xAI の最新大規模言語モデル
- **Qwen3.5** — Alibaba 製の多言語対応モデル
- **GPT-5.3 / GPT-5.4** — OpenAI 最新シリーズ
- **Phi-4-Reasoning-Vision** — Microsoft 製の推論特化型ビジョンモデル

---

### 8. Content Understanding ライブラリ（GA）

ドキュメント・メディア分析用の **Content Understanding SDK** が以下のプラットフォームで一般提供：

- .NET
- JavaScript
- Python

---

## ⚠️ 廃止予定のお知らせ

| 機能 | 廃止予定日 |
|---|---|
| Azure App Service / Functions の Python on Windows | 2027年3月 |
| ストレージアカウントの AzureDnsEndpoints | 2027年3月 |

早めの移行計画をご検討ください。

---

## まとめ

今週は特に **AI Foundry への新モデル追加** と **AKS Blue-Green アップグレード** が注目です。
また、Bicep Snapshot と Azure Firewall ドラフトモードの GA により、インフラ管理の安全性が大幅に向上しました。

最新の Azure アップデートは [Azure Updates 公式ページ](https://azure.microsoft.com/ja-jp/updates/) でご確認いただけます。

---

*この記事は毎週月曜日に更新されます。次回もお楽しみに！*
