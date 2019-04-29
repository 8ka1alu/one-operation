"""
ワンナイト人狼GMbot ver1.0
"""
import discord
from management.GameManager import GameManager
import asyncio
client = discord.Client()
game = GameManager()


# ids.txtからBotのアクセストークンとメインのテキストチャンネルIDを取得します
with open("ids.txt", "r") as f:
    string = f.read()
accesstoken = string.split()[0]
mainch = client.get_channel(int(string.split()[1]))

# 自由に追加できるコマンドです。「command.append(["コマンド", "返すメッセージ"])」で追加してください。
command = []
command.append(["!ハッピーラッキー", "スマイルイエーイ！"])
command.append(["!黒服合同", "https://twitter.com/i/moments/1108160244809531392"])
command.append(["!公式", "twittttther　https://twitter.com/bang_dream_gbp \n ホームページ https://bang-dream.bushimo.jp/"])
command.append(["!遊び方", "https://github.com/tsubasa283paris/OneNightJinroBot/blob/master/README.md"])

# ゲームフェーズごとに使えるコマンド一覧です。
commands_per_phase = {
    "standby" : ["!参加", "!観戦", "!人数", "!ゲーム開始"],
    "night" : ["!占い", "!怪盗"],
    "day" : ["!投票", "!結果", "!GM投票"]
}

# デフォルトの討論タイマーの時間(分)
discuss_time = 5


@client.event
async def on_ready():
    # Bot起動時の処理
    print('ログインしました')
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('------')

    await mainch.send("YAPPY! HELLO、HAPPY WORLD！")


@client.event
async def on_message(message):
    global discuss_time
    mes = message.content.split(" ")
    aut = message.author

    if aut.bot:  # ボットのメッセージをハネる
       return

    if mes[0] in commands_per_phase[game.phase]:
        chat = game.commands(aut, mes[0], mes[1], mes[2])
        if chat[0] == "mainch":
            await mainch.send(chat[1])
        elif chat[0] == "dm":
            dm = aut.create_dm()
            await dm.send(chat[1])
        if mes[0] == commands_per_phase["standby"][3]:
            if len(mes) == 1:
                await process_game()
            elif len(mes) > 1:
                try:
                    discuss_time = int(mes[1])
                    await process_game()
                except:
                    await mainch.send(":tired_face: 無効なコマンドです。タイマーの設定がおかしいようです。")
        elif mes[0] == commands_per_phase["day"][0]:
            await mainch.send("{}さんが投票を完了しました。".format(aut.mention))
        elif mes[0] == commands_per_phase["day"][1]:
            await gameset()
    else:
        message.channel.send(":tired_face: 無効なコマンドです。")
            
    for c in command:
        if mes[0] == c[0]:
            await message.channel.send(c[1])

    if mes[0] == "!じゃあな":
        # ログアウト
        await message.channel.send("落ちます。お疲れ様でした。")
        await client.logout()


async def process_game():
    chat = game.setjob() # 役職を割り振り、通知する
    for i in range(game.player.playernum()):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1][i])
    await asyncio.sleep(10)
    await mainch.send(":first_quarter_moon_with_face: 夜になります。")
    chat = game.jobmessage() # ターンの存在する役職ごとにDMを送信する
    for i in range(len(chat[0])):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1][i])
    await mainch.send("役職持ちのプレイヤーへDMを送りました。30秒後に朝になります。")
    await asyncio.sleep(30)
    game.phase = "day"
    await mainch.send(":sun_with_face: 朝になりました！討論を開始してください。\n:alarm_clock: 討論時間は残り{}分です。".format(discuss_time))
    chat = game.watchmessage() # 観戦者に役職と怪盗の結果を通知する
    for i in range(len(chat[0])):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1])
    for i in range(1, discuss_time): # タイマーが1分ごとに通知
        await asyncio.sleep(60)
        await mainch.send("討論時間は残り{}分です。".format(discuss_time - i))
    await asyncio.sleep(60)
    await mainch.send(":alarm_clock: 討論時間が終了しました。")
    chat = game.votemessage() # 投票アクションのコマンドを通知
    await mainch.send(chat)

async def gameset():
    await asyncio.sleep(5)
    mes = game.getresult()
    await mainch.send(mes)

# botの接続と起動
client.run(accesstoken)