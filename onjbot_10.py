"""
ワンナイト人狼GMbot ver1.0
工事現場
"""
import discord
# import onenight_jinro_10 as onj
from manager.GameManager import GameManager
client = discord.Client()


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
forbidden_commands_per_phase = {
    "standby" : ["!参加", "!観戦", "!ゲーム開始"],
    "night" : ["!占い", "!怪盗"],
    "day" : ["!投票開始"],
    "dusk" : ["!投票", "!結果"]
}


@client.event
async def on_ready():
    # Bot起動時の処理
    print('ログインしました')
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('------')

    await mainch.send("YAPPY! HELLO、HAPPY WORLD！")

    game = GameManager()


@client.event
async def on_message(message):
    mes = message.content.split(" ")
    aut = message.author

    if aut.bot:  # ボットのメッセージをハネる
       return

    if mes[0] in forbidden_commands_per_phase[game.phase()]:
        chat = game.commands(aut, mes[0], mes[1])
        if chat[0] = "mainch":
            await mainch.send(chat[1])
        elif chat[0] = "dm":
            dm = aut.create_dm()
            await dm.send(chat[1])
            
    for c in command:
        if mes[0] == c[0]:
            await message.channel.send(c[1])

    if mes[0] == "!じゃあな":
        # ログアウト
        await message.channel.send("落ちます。お疲れ様でした。")
        await client.logout()


# botの接続と起動
client.run(accesstoken)