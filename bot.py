import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
import random
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
intents.message_content = True

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
        
        # 各選択肢のボタンを作成
        for i, option in enumerate(quiz['options']):
            button = Button(
                label=option,
                style=discord.ButtonStyle.primary,
                custom_id=f"quiz_{quiz['id']}_{i}"
            )
            button.callback = self.create_callback(i)
            self.add_item(button)
    
    def create_callback(self, option_index):
        async def callback(interaction: discord.Interaction):
            # 既に回答済みのユーザーをチェック
            if interaction.user.id in self.answered_users:
                await interaction.response.send_message(
                    "既に回答済みです！",
                    ephemeral=True
                )
                return
            
            # ユーザーを回答済みリストに追加
            self.answered_users.add(interaction.user.id)
            
            # 正解判定
            if option_index == self.correct_answer:
                response = f"🎉 正解です！\n\n**解説:**\n{self.quiz['explanation']}"
                await interaction.response.send_message(response, ephemeral=True)
            else:
                correct_option = self.quiz['options'][self.correct_answer]
                response = f"❌ 不正解です。\n\n**正解:** {correct_option}\n\n**解説:**\n{self.quiz['explanation']}"
                await interaction.response.send_message(response, ephemeral=True)
        
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
    
    # 現在の時刻を取得
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    time_emoji = "🌅" if now.hour == 7 else "☀️" if now.hour == 12 else "🌙"
    
    # Embedメッセージを作成
    embed = discord.Embed(
        title=f"{time_emoji} 本日のITクイズ",
        description=f"**問題:**\n{quiz['question']}",
        color=discord.Color.blue(),
        timestamp=now
    )
    embed.set_footer(text="正解と解説は選択後に表示されます")
    
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
    
    # 7:00, 12:00, 20:00 に実行
    target_times = [
        time(7, 0),   # 朝7時
        time(12, 0),  # 昼12時
        time(20, 0)   # 夜20時
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
