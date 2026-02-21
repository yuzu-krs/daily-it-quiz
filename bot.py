import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
import random
import re
import os
from datetime import datetime, time
from dotenv import load_dotenv
import pytz

# 環境変数を読み込む
load_dotenv()

# Bot設定
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
TIMEZONE = os.getenv('TIMEZONE', 'Asia/Tokyo')

# Intentsの設定
intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

# クイズデータを読み込む（複数JSONファイル対応）
def load_quizzes():
    all_quizzes = []
    quiz_dir = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(quiz_dir):
        if filename.endswith('_quizzes.json') or filename == 'quizzes.json':
            filepath = os.path.join(quiz_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                all_quizzes.extend(json.load(f))
    return all_quizzes

# クイズViewクラス（ボタン付き）
class QuizView(View):
    def __init__(self, quiz, correct_answer):
        super().__init__(timeout=None)
        self.quiz = quiz
        self.correct_answer = correct_answer
        self.answered_users = set()
        
        # 各選択肢のボタンを作成（A, B, C, Dのラベル）
        labels = ['A', 'B', 'C', 'D']
        colors = [
            discord.ButtonStyle.primary,    # 青
            discord.ButtonStyle.success,    # 緑
            discord.ButtonStyle.secondary,  # グレー
            discord.ButtonStyle.danger      # 赤
        ]
        for i in range(len(quiz['options'])):
            button = Button(
                label=labels[i],
                style=colors[i],
                custom_id=f"quiz_{quiz['id']}_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, option_index):
        async def callback(interaction: discord.Interaction):
            # 正解判定
            if option_index == self.correct_answer:
                response = f"🎉 正解です！\n\n**解説:**\n{self.quiz['explanation']}"
                await interaction.response.send_message(response, ephemeral=True, delete_after=30)
            else:
                correct_option = self.quiz['options'][self.correct_answer]
                response = f"❌ 不正解です。\n\n**正解:** {correct_option}\n\n**解説:**\n{self.quiz['explanation']}"
                await interaction.response.send_message(response, ephemeral=True, delete_after=30)
        
        return callback

# クイズを投稿する関数
async def post_quiz():
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"チャンネルID {CHANNEL_ID} が見つかりません")
        return
    
    # クイズデータを読み込む
    quizzes = load_quizzes()
    
    # ランダムにクイズを選択
    quiz = random.choice(quizzes)
    
    # 選択肢をシャッフル（正解のインデックスも追跡）
    original_correct = quiz['correct']
    options_with_index = list(enumerate(quiz['options']))  # [(0, "B:..."), (1, "A:..."), ...]
    random.shuffle(options_with_index)
    
    # シャッフル後の正解インデックスを特定
    new_correct = None
    shuffled_options = []
    labels = ['A', 'B', 'C', 'D']
    for new_idx, (orig_idx, option_text) in enumerate(options_with_index):
        if orig_idx == original_correct:
            new_correct = new_idx
        # 既存のラベル（"A.", "B:", "C：" 等）を除去して新しいラベルを付ける
        clean_text = re.sub(r'^[A-D]\s*[.。:：]\s*', '', option_text)
        shuffled_options.append(f"{labels[new_idx]}. {clean_text}")
    
    # quizのコピーを作成してシャッフル済みデータに差し替え
    quiz = dict(quiz)
    quiz['options'] = shuffled_options
    quiz['correct'] = new_correct
    
    # 現在の時刻を取得
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    time_emoji = "🌅"
    
    # 選択肢を整形（空行で区切る）
    options_text = "\n\n".join([f"**{option}**" for option in quiz['options']])
    
    # Embedメッセージを作成
    embed = discord.Embed(
        title=f"{time_emoji} 本日のITクイズ #{quiz['id']}",
        color=0x5865F2,  # Discord Blurple
        timestamp=now
    )
    embed.add_field(
        name="📝 問題",
        value=f"{quiz['question']}\n",
        inline=False
    )
    embed.add_field(
        name="💡 選択肢",
        value=options_text,
        inline=False
    )
    embed.set_footer(
        text=f"ボタンをクリックして回答してください • 正解と解説は選択後に表示されます • 毎朝7:00に出題",
        icon_url="https://cdn.discordapp.com/emojis/1234567890.png"  # Optional
    )
    
    # Viewを作成してメッセージを送信
    view = QuizView(quiz, quiz['correct'])
    await channel.send(embed=embed, view=view)
    print(f"クイズを投稿しました: {quiz['question'][:30]}...")

# スケジュールされたタスク
@tasks.loop(minutes=1)
async def scheduled_quiz():
    # 現在の時刻を取得
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    current_time = now.time()
    
    # 7:00 に実行
    target_times = [
        time(7, 0),   # 朝7時
        time(12, 0),   # 昼12時
        time(19, 0),   # 夜7時
    ]
    
    # 1分以内の誤差を許容
    for target_time in target_times:
        if (current_time.hour == target_time.hour and 
            current_time.minute == target_time.minute):
            await post_quiz()
            break

@scheduled_quiz.before_loop
async def before_scheduled_quiz():
    await bot.wait_until_ready()
    print("スケジューラーを開始します...")

# Bot起動時のイベント
@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました')
    print(f'Bot ID: {bot.user.id}')
    print(f'チャンネルID: {CHANNEL_ID}')
    print('------')
    
    # 起動時に1回クイズを投稿
    await post_quiz()
    
    # スケジューラーを開始
    if not scheduled_quiz.is_running():
        scheduled_quiz.start()

# テスト用コマンド（手動でクイズを投稿）
@bot.command(name='testquiz')
@commands.has_permissions(administrator=True)
async def test_quiz(ctx):
    """管理者用：手動でクイズを投稿"""
    await post_quiz()
    await ctx.send("テストクイズを投稿しました！", delete_after=5)

# Bot実行
if __name__ == '__main__':
    if not TOKEN:
        print("エラー: DISCORD_TOKENが設定されていません")
        print(".envファイルを作成してトークンを設定してください")
    elif not CHANNEL_ID:
        print("エラー: CHANNEL_IDが設定されていません")
        print(".envファイルにチャンネルIDを設定してください")
    else:
        bot.run(TOKEN)
