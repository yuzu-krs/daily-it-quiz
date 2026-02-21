# Discord IT クイズBot

## Bot説明文（Discord Developer Portal用）

> 毎朝7:00 JST、ITエンジニア向けの4択クイズを自動投稿するBotです。
> ネットワーク・セキュリティ・クラウド・AI・Web開発など20以上のカテゴリから出題。
> ボタンをクリックするだけで回答でき、即座に正解と解説を確認できます。
> チームの学習習慣づくりや技術力アップにご活用ください！

---

## 概要

毎朝7時にDiscordチャンネルでITに関する4択クイズを自動投稿するボットです。

### 対応クイズカテゴリ（20カテゴリ以上）

| カテゴリ             | 内容                                        |
| -------------------- | ------------------------------------------- |
| ネットワーク         | TCP/IP・HTTP・DNS など                      |
| セキュリティ         | 脆弱性・暗号化・認証 など                   |
| クラウド             | AWS・GCP・Azure など                        |
| AI / データ          | 機械学習・LLM・データ分析 など              |
| Web開発              | HTML/CSS・JavaScript・フレームワーク など   |
| データベース         | SQL・NoSQL・設計 など                       |
| Linux / OS           | コマンド・カーネル・システム管理 など       |
| プログラミング       | アルゴリズム・言語仕様・設計パターン など   |
| コンテナ             | Docker・Kubernetes など                     |
| DevOps               | CI/CD・IaC・監視 など                       |
| モバイル             | iOS・Android・クロスプラットフォーム など   |
| 攻撃技術（Web/認証） | SQLインジェクション・XSS・認証バイパス など |
| 攻撃技術（インフラ） | ポートスキャン・ラテラルムーブメント など   |
| 攻撃技術（AI/LLM）   | プロンプトインジェクション・モデル攻撃 など |
| CS基礎               | アルゴリズム・データ構造・計算理論 など     |
| 応用                 | 総合的な高難易度問題                        |
| エンタメIT           | ゲーム・アニメ・ITトリビア など             |

## 機能

- 📅 **自動投稿**: 毎朝7:00 JST に自動でクイズを投稿
- 🎯 **多彩なカテゴリ**: ネットワーク・セキュリティ・AI・クラウドなど20カテゴリ以上、大量のクイズを収録
- 🔀 **選択肢シャッフル**: 毎回ランダムに選択肢の順序を変更（暗記対策）
- 🔘 **ボタン式回答**: クリックで簡単に回答できるインタラクティブUI
- ✅ **即時フィードバック**: 回答後すぐに正解・不正解と解説を表示
- 🔒 **プライバシー保護**: 回答結果は本人にのみ表示（ephemeral）
- 🛠️ **手動投稿コマンド**: 管理者は `!testquiz` コマンドで任意のタイミングに出題可能

## セットアップ

### 1. 必要な環境

- Python 3.8以上
- Discordアカウント
- Discord Bot Token

### 2. Discord Botの作成

1. [Discord Developer Portal](https://discord.com/developers/applications) にアクセス
2. 「New Application」をクリックして新しいアプリケーションを作成
3. 左メニューから「Bot」を選択
4. 「Add Bot」をクリックしてボットを作成
5. 「TOKEN」の下にある「Reset Token」をクリックしてトークンを取得（後で使用）
6. 「Privileged Gateway Intents」セクションで以下を有効化:
   - `MESSAGE CONTENT INTENT`

### 3. Botの招待

1. 左メニューから「OAuth2」→「URL Generator」を選択
2. 「SCOPES」で以下を選択:
   - `bot`
   - `applications.commands`
3. 「BOT PERMISSIONS」で以下を選択:
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
   - `Use Slash Commands`
4. 生成されたURLをブラウザで開き、ボットをサーバーに招待

### 4. チャンネルIDの取得

1. Discordの「ユーザー設定」→「詳細設定」→「開発者モード」を有効化
2. クイズを投稿したいチャンネルを右クリック
3. 「IDをコピー」を選択

### 5. プロジェクトのセットアップ

```bash
# リポジトリをクローン（またはダウンロード）
cd daily-quiz

# 仮想環境を作成（推奨）
python -m venv venv

# 仮想環境を有効化
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 6. 環境変数の設定

```bash
# .env.exampleをコピーして.envファイルを作成
copy .env.example .env  # Windows
# または
cp .env.example .env    # Mac/Linux
```

`.env`ファイルを開いて以下を設定:

```env
DISCORD_TOKEN=あなたのボットトークン
CHANNEL_ID=クイズを投稿するチャンネルID
TIMEZONE=Asia/Tokyo
```

### 7. ボットの起動

```bash
python bot.py
```

正常に起動すると、以下のようなメッセージが表示されます:

```
ボット名 としてログインしました
Bot ID: 123456789
チャンネルID: 987654321
------
スケジューラーを開始します...
```

## 使い方

### 自動投稿

ボットが起動していれば、自動的に毎朝以下の時間にクイズが投稿されます:

- 🌅 朝 7:00

### 手動テスト（管理者のみ）

サーバーの管理者権限を持つユーザーは、以下のコマンドで手動でクイズを投稿できます:

```
!testquiz
```

### クイズへの回答

1. 投稿されたクイズの選択肢ボタンをクリック
2. 正解・不正解と解説がプライベートメッセージで表示されます
3. 各ユーザーは1つのクイズに1回のみ回答可能

## クイズの追加・編集

`quizzes.json`ファイルを編集することで、クイズを追加・変更できます。

### フォーマット

```json
{
  "id": 1,
  "question": "質問文",
  "options": ["A. 選択肢1", "B. 選択肢2", "C. 選択肢3", "D. 選択肢4"],
  "correct": 0,
  "explanation": "解説文"
}
```

- `id`: 一意の識別番号（重複しないように）
- `question`: クイズの質問文
- `options`: 4つの選択肢（配列）
- `correct`: 正解の選択肢のインデックス（0-3）
  - 0 = A, 1 = B, 2 = C, 3 = D
- `explanation`: 正解の解説

## トラブルシューティング

### ボットがメッセージを送信しない

1. ボットが正しくチャンネルにアクセスできるか確認
2. チャンネルIDが正しいか確認
3. ボットに適切な権限（Send Messages、Embed Links）があるか確認

### トークンエラー

1. `.env`ファイルが正しく作成されているか確認
2. トークンが正しくコピーされているか確認（前後の空白に注意）
3. Discord Developer Portalでトークンを再生成

### クイズが重複して出題される

- ボットを再起動すると出題履歴がリセットされます
- 常時稼働させる場合は、データベースに履歴を保存する実装を追加することを推奨

### タイムゾーンが合わない

`.env`ファイルの`TIMEZONE`を確認してください。日本時間の場合は`Asia/Tokyo`を設定します。

## ファイル構成

```
discord/
├── bot.py                        # メインボットコード
├── quizzes.json                  # 汎用クイズデータ
├── network_quizzes.json          # ネットワーク
├── security_quizzes.json         # セキュリティ
├── cloud_quizzes.json            # クラウド
├── ai_data_quizzes.json          # AI・データ
├── web_dev_quizzes.json          # Web開発
├── database_quizzes.json         # データベース
├── linux_os_quizzes.json         # Linux・OS
├── programming_quizzes.json      # プログラミング
├── container_quizzes.json        # コンテナ
├── devops_quizzes.json           # DevOps
├── mobile_quizzes.json           # モバイル
├── cs_basics_quizzes.json        # CS基礎
├── advanced_quizzes.json         # 応用
├── attack_web_auth_quizzes.json  # 攻撃技術（Web・認証）
├── attack_infra_quizzes.json     # 攻撃技術（インフラ）
├── attack_ai_llm_quizzes.json    # 攻撃技術（AI・LLM）
├── entertainment_it_quizzes.json # エンタメIT
├── requirements.txt              # Python依存パッケージ
├── .env.example                  # 環境変数のテンプレート
├── .env                          # 環境変数（自分で作成）
└── README.md                     # このファイル
```

## 常時稼働

### ローカル環境で24時間稼働

- PCを常時起動しておく必要があります
- バックグラウンドで実行する場合は、タスクスケジューラー（Windows）やsystemd（Linux）を使用

### クラウドサービスで稼働（推奨）

無料または低コストでボットを24時間稼働できるサービス:

1. **Heroku** (無料枠あり)
2. **Railway** (月$5の無料クレジット)
3. **Replit** (無料プランあり)
4. **Google Cloud Run** (無料枠あり)
5. **AWS EC2** (t2.microの無料枠)

## ライセンス

MIT License

## サポート

問題が発生した場合は、Issueを作成してください。

## 今後の拡張案

- [ ] データベース連携（出題履歴、統計）
- [ ] ユーザーごとの正解率記録
- [ ] ランキング機能
- [ ] カテゴリ別クイズ
- [ ] 難易度設定
- [ ] クイズ作成コマンド
- [ ] Webhookサポート
