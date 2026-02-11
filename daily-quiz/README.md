# Discord IT クイズBot

毎日決まった時間（朝7時、昼12時、夜20時）にDiscordチャンネルでITに関する4択クイズを自動投稿するボットです。

## 機能

- 📅 **自動投稿**: 毎日3回（7:00、12:00、20:00 JST）に自動でクイズを投稿
- 🎯 **4択クイズ**: ITに関する様々なトピックのクイズ（30問以上収録）
- 🔘 **ボタン式回答**: クリックで簡単に回答できるインタラクティブUIl
- ✅ **即時フィードバック**: 回答後すぐに正解・不正解と解説を表示
- 🔄 **重複防止**: 一度出題されたクイズは全問出題されるまで再出題されない
- 🔒 **プライバシー保護**: 回答結果は本人にのみ表示（ephemeral）

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

ボットが起動していれば、自動的に毎日以下の時間にクイズが投稿されます:

- 🌅 朝 7:00
- ☀️ 昼 12:00
- 🌙 夜 20:00

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
daily-quiz/
├── bot.py              # メインボットコード
├── quizzes.json        # クイズデータ
├── requirements.txt    # Python依存パッケージ
├── .env.example        # 環境変数のテンプレート
├── .env                # 環境変数（自分で作成）
├── .gitignore          # Gitで無視するファイル
└── README.md           # このファイル
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
