"""
ワンナイト人狼GMbot ver1.0
"""
import discord
from management.GameManager import GameManager
import asyncio
import os
client = discord.Client()
game = GameManager()

accesstoken = os.environ['DISCORD_BOT_TOKEN']
channelid = 674966854183157791

def addcommand(arg1, arg2):
    global command
    command[0].append(arg1)
    command[1].append(arg2)

# 自由に追加できるコマンドです。「addcommand("コマンド", "返すメッセージ")」で追加してください。
command = [[], []]
addcommand("!ハッピーラッキー", "スマイルイエーイ！")
addcommand("!黒服合同", "https://twitter.com/i/moments/1108160244809531392")
addcommand("!公式", "twittttther　https://twitter.com/bang_dream_gbp \n ホームページ https://bang-dream.bushimo.jp/")
addcommand("!遊び方", "https://github.com/tsubasa283paris/OneNightJinroBot/blob/master/README_1_0.md")

# ゲームフェーズごとに使えるコマンド一覧です。
commands_per_phase = {
    "standby" : ["!参加", "!観戦", "!参加者", "!開始", "!参加者リセット"],
    "night" : ["!占い", "!怪盗"],
    "day" : ["!投票", "!GM投票"]
}

# デフォルトの討論タイマーの時間(分)
discuss_time = 5


@client.event
async def on_ready():
    global mainch
    # Bot起動時の処理
    print('ログインしました')
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('------')

    mainch = client.get_channel(channelid)
    await mainch.send("YAPPY! HELLO、HAPPY WORLD！")


@client.event
async def on_message(message):
    global discuss_time
    mes = message.content.split(" ")
    aut = message.author

    if aut.bot:  # ボットのメッセージをハネる
       return

    if mes[0] == "!じゃあな":
        # ログアウト
        await message.channel.send("落ちます。お疲れ様でした。")
        await client.logout()
    elif mes[0] in command[0]:
        for i in range(len(command[0])):
            if mes[0] == command[0][i]:
                await mainch.send(command[1][i])
    elif mes[0] in commands_per_phase[game.phase]:
        if len(mes) == 1:
            chat = game.commands(aut, mes[0], None, None)
        elif len(mes) == 2:
            chat = game.commands(aut, mes[0], mes[1], None)
        elif len(mes) == 3:
            chat = game.commands(aut, mes[0], mes[1], mes[2])
        if chat[0] == "mainch":
            await mainch.send(chat[1])
        elif chat[0] == "dm":
            dm = await aut.create_dm()
            await dm.send(chat[1])
        if mes[0] == commands_per_phase["standby"][3] and game.startable:
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
            await votecheck()
        elif mes[0] == commands_per_phase["day"][1]:
            await votecheck()


async def process_game():
    chat = game.setjob() # 役職を割り振り、通知する
    for i in range(game.player.playernum()):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1][i])
    chat = game.watchmessage() # 観戦者にプレイヤーの役職を通知する
    for i in range(len(chat[0])):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1])
    await asyncio.sleep(10)
    await mainch.send(":first_quarter_moon_with_face: 夜になります。")
    chat = game.jobmessage() # ターンの存在する役職ごとにDMを送信する
    for i in range(len(chat[0])):
        dm = await chat[0][i].create_dm()
        await dm.send(chat[1][i])
    await mainch.send("役職持ちのプレイヤーへDMを送りました。60秒後に朝になります。")
    await asyncio.sleep(60)
    game.thiefact()
    game.phase = "day"
    cards = game.getcardslist()
    await mainch.send(":sun_with_face: 朝になりました！討論を開始してください。\n" + cards + "\n:alarm_clock: 討論時間は残り{}分です。".format(discuss_time))
    chat = game.watchmessage_thief() # 観戦者に怪盗の行動を通知する
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


async def votecheck():
    if game.vote_is_complete():
        await gameset()


async def gameset():
    game.result()
    await mainch.send(game.chat)
    await asyncio.sleep(5)
    mes = game.getresult()
    await mainch.send(mes)

# botの接続と起動
client.run(accesstoken)
