# coding: utf-8
"""
ワンナイト人狼GMbot ver1.1(beta)
"""

import discord
import random
import onenight_jinro_1_1b as onj
import time
from time import sleep
import os

accesstoken = os.environ['DISCORD_BOT_TOKEN']
channelid = 674966854183157791

# ==========ワンナイト人狼用変数宣言==========
client = discord.Client()
gameflag = 0 # 参加待機状態で1, ゲーム開始状態になれば2, 投票状態になれば3
uranai_flag = False # 行動可能かどうか
kaito_flag = False
ninzu = 0
uranai_id = 0
kaito_id = 0
jinro_id = []
playername = []
watchername = []
playerclass = []
watcherclass = []
tohyo_flag = [] # すでに投票を行ったかどうか
heiwa = 0 # 平和村投票
heiwa_flag = [] # 平和村に投票したかどうか
calleveryone = ""
mainch = None
game = None
globt = None

# ==========お遊び用変数宣言==========
command = []
# command.append(["コマンド", "返すメッセージ"])
command.append(["!ハッピーラッキー", "スマイルイエーイ！"])
command.append(["!黒服合同", "https://twitter.com/i/moments/1108160244809531392"])
command.append(["!公式", "twittttther　https://twitter.com/bang_dream_gbp \n ホームページ https://bang-dream.bushimo.jp/"])
command.append(["!遊び方", "https://github.com/tsubasa283paris/OneNightJinroBot/blob/master/README.md"])


@client.event
async def on_ready():
    print('ログインしました')
    print(client.user.name)  # ボットの名前
    print(client.user.id)  # ボットのID
    print(discord.__version__)  # discord.pyのバージョン
    print('------')

    mainch = client.get_channel(channelid)
    await mainch.send("YAPPY! HELLO、HAPPY WORLD！")
    await client.change_presence(status=discord.Status.idle,activity=discord.Game(name='ワンナイト人狼'))

@client.event
async def on_message(message):
    global gameflag, ninzu, playername, watchername, playerclass, watcherclass, mainch, calleveryone, tohyo_flag, heiwa_flag, heiwa, mainch
    global uranai_id, kaito_id, jinro_id
    global uranai_flag, kaito_flag
    global game
    global globt
    
    if message.author.bot:  # ボットのメッセージをハネる
       return

    """
    ==========ここからワンナイト人狼部分==========
    """

    if message.content == "!人狼スタート":
        await message.channel.send(":first_quarter_moon_with_face: ワンナイト人狼の試合を始めます。\n参加者の方は当チャンネルにて「!参加」と、ゲームを観戦する方は「!観戦」とお送りください。\n参加メッセージを送り終え、準備が整いましたら「!開始」とお送りください。ゲームが開始されます。")
        gameflag = 1
        ninzu = 0
        playername = []
        watchername = []
        playerclass = []
        watcherclass = []
        tohyo_flag = []
        mainch = client.get_channel(channelid)
    
    elif message.content == "!参加":
        ment = message.author.mention
        if gameflag == 1:
            if watchername.count(ment) == 1:
                await mainch.send("{} 観戦を取り消し、参加を承りました。".format(ment))
                watchername.remove(ment)
                watcherclass.remove(message.author)
                ninzu += 1
                playername.append(ment)
                playerclass.append(message.author)
                tohyo_flag.append([0, 0])
                heiwa_flag.append(0)
                role1 = discord.utils.get(message.guild.roles, name='観戦者')
                await message.author.remove_roles(role1)
                role0 = discord.utils.get(message.guild.roles, name='参加者')
                await message.author.add_roles(role0)
            else:
                if playername.count(ment) == 0:
                    await mainch.send("{} 参加承りました。".format(ment))
                    ninzu += 1
                    playername.append(ment)
                    playerclass.append(message.author)
                    tohyo_flag.append([0, 0])
                    heiwa_flag.append(0)
                    role0 = discord.utils.get(message.guild.roles, name='参加者')
                    await message.author.add_roles(role0)
                elif playername.count(ment) == 1:
                    await mainch.send("{} 参加を取り消しました。".format(ment))
                    ninzu -= 1
                    playername.remove(ment)
                    playerclass.remove(message.author)
                    tohyo_flag.remove([0, 0])
                    heiwa_flag.remove(0)
                    role1 = discord.utils.get(message.guild.roles, name='参加者')
                    await message.author.remove_roles(role1)
                
        elif gameflag == 0:
            await message.channel.send("❕ゲームが待機状態になっていないようです。")
        else:
            await message.channel.send("❕ゲーム進行中です。現在のゲームが終了するまでお待ち下さい。")

    elif message.content == "!観戦":
        ment = message.author.mention
        if gameflag == 1:
            if playername.count(ment) == 1:
                await mainch.send("{} 参加を取り消し、観戦を承りました。".format(ment))
                ninzu -= 1
                playername.remove(ment)
                playerclass.remove(message.author)
                tohyo_flag.remove([0, 0])
                heiwa_flag.remove(0)
                watchername.append(ment)
                watcherclass.append(message.author)
                role1 = discord.utils.get(message.guild.roles, name='参加者')
                await message.author.remove_roles(role1)
                role0 = discord.utils.get(message.guild.roles, name='観戦者')
                await message.author.add_roles(role0)
            else:
                if watchername.count(ment) == 0:
                    await mainch.send("{} 観戦承りました。".format(ment))
                    watchername.append(ment)
                    watcherclass.append(message.author)
                    role0 = discord.utils.get(message.guild.roles, name='観戦者')
                    await message.author.add_roles(role0)
                elif playername.count(ment) == 1:
                    await mainch.send("{} 観戦を取り消しました。".format(ment))
                    watchername.remove(ment)
                    watcherclass.remove(message.author)
                    role1 = discord.utils.get(message.guild.roles, name='観戦者')
                    await message.author.remove_roles(role1)
                    
        elif gameflag == 0:
            await message.channel.send("❕ゲームが待機状態になっていないようです。")
        else:
            await message.channel.send("❕ゲーム進行中です。現在のゲームが終了するまでお待ち下さい。")

    elif message.content == "!開始":

        if gameflag == 1:
            """
            ==========ゲームの開始==========
            """

            if ninzu < 4:
                await mainch.send("❕プレイヤーの人数が足りていないようです。「!人数」で人数を確認し、4人以上になっていることを確認してください。")
            elif ninzu > 7:
                await mainch.send("❕プレイヤーの人数が多すぎるようです。「!人数」で人数を確認し、7人以下になっていることを確認してください。")
            else:
                gameflag = 2
                ment = ""
                for pn in playername:
                    ment += pn
                    ment += ", "
                uranai_flag = True
                kaito_flag = True
                heiwa = 0

                await mainch.send(ment + " {}人でのワンナイト人狼ゲームを開始します。".format(ninzu))
                game = onj.OneNightJinro("{}".format(ninzu), "default")

                jinro_id = []
                print(game.players())
                for i in range(ninzu + 2):
                    if game.players()[i][0] == 1:
                        uranai_id = i
                    elif game.players()[i][0] == 2:
                        kaito_id = i
                    elif game.players()[i][0] == 3:
                        jinro_id.append(i)

                calleveryone = ""
                for i in range(ninzu):
                    calleveryone += playername[i]
                    calleveryone += " "
                    dm = await playerclass[i].create_dm()
                    await dm.send("{} あなたの役職は".format(playername[i]) + game.yakushoku_winlose(i) + "です。")

                await mainch.send("ダイレクトメッセージにて役職を通知しました。10秒後に夜になります。")

                kekka = ""
                for i in range(ninzu):
                    kekka += "{} : ".format(playername[i]) + game.yakushoku_winlose(i)
                    kekka += "\n"
                for i in range(len(watcherclass)):
                    dm = await watcherclass[i].create_dm()
                    await dm.send(kekka)

                sleep(10)
                # ==========占い師のターン==========
                await mainch.send("夜になります。")
                await mainch.send("占い師のターン。20秒後に人狼のターンになります。")
                
                if uranai_id < ninzu:
                    """
                    ==========占い師がいるとき==========
                    """
                    globt = time.time()
                    uranai_message = ""
                    for i in range(ninzu):
                        if i == uranai_id:
                            continue
                        else:
                            uranai_message += "「!u{}」: {} \n".format(i, playername[i])
                    uranai_message += "「!u-1」: 山札"

                    dm = await playerclass[uranai_id].create_dm()
                    await dm.send("{} 占う相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[uranai_id]))
                    await dm.send(uranai_message)

                else:
                    """
                    ==========占い師がいないとき==========
                    """
                    sleep(20)
                    # ==========人狼のターン==========
                    await mainch.send("人狼のターン。10秒後に怪盗のターンになります。")
                    if jinro_id[1] < ninzu:
                        """
                        ==========人狼が二人共いるとき==========
                        """
                        t = time.time()
                        for i in range(2):
                            jid = jinro_id[i - 1]
                            dm = await playerclass[jinro_id[i]].create_dm()
                            await dm.send("あなたと{}が人狼です。".format(playername[jid]))
                        while True:
                            c = time.time()
                            if c - t >= 10:
                                # ==========怪盗のターン==========
                                await mainch.send("怪盗のターン。20秒後に夜が明けます。")
                                break
                        if kaito_id < ninzu:
                            """
                            ==========怪盗がいるとき==========
                            """
                            globt = time.time()
                            kaito_message = ""
                            for i in range(ninzu):
                                if i == kaito_id:
                                    continue
                                else:
                                    kaito_message += "「!k{}」: {} \n".format(i, playername[i])
                            dm = await playerclass[kaito_id].create_dm()
                            await dm.send("{} 役職を盗む相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[kaito_id]))
                            await dm.send(kaito_message)
                        else:
                            """
                            ==========怪盗がいないとき==========
                            """
                            sleep(20)
                            # ==========夜明け==========
                            await mainch.send(calleveryone + "夜が明けました。討論を開始してください。")
                            await mainch.send("投票の準備が整いましたら「!投票」とお送りください。")
                            gameflag = 3

                    elif jinro_id[1] >= ninzu:
                        """
                        ==========人狼が一人のみのとき==========
                        """
                        t = time.time()
                        dm = await playerclass[jinro_id[0]].create_dm()
                        await dm.send("人狼はあなた一人です。")
                        while True:
                            c = time.time()
                            if c - t >= 10:
                                # ==========怪盗のターン==========
                                await mainch.send("怪盗のターン。20秒後に夜が明けます。")
                                break
                        # 占い師と人狼が山札にいるので怪盗はいる
                        globt = time.time()
                        kaito_message = ""
                        for i in range(ninzu):
                            if i == kaito_id:
                                continue
                            else:
                                kaito_message += "「!k{}」: {} \n".format(i, playername[i])
                        dm = await playerclass[kaito_id].create_dm()
                        await dm.send("{} 役職を盗む相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[kaito_id]))
                        await dm.send(kaito_message)

        elif gameflag == 0:
            await mainch.send("❕ゲームが待機状態になっていないようです。")
        else:
            await mainch.send("❕ゲームはすでに開始されています。")

    """
    ==========占い師がいるとき==========
    """
    
    for i in range(-1, ninzu):
        if message.content == "!u{}".format(i):
            if uranai_flag and message.author == playerclass[uranai_id]:
                dm = await playerclass[uranai_id].create_dm()
                if i != -1:
                    await dm.send("占いの結果{}は".format(playername[i]) + game.yakushoku(game.uranai_check(i)) + "でした。")
                    uranai_flag = False
                elif i == -1:
                    yama = game.uranai_check(-1)
                    await dm.send("占いの結果山札は" + yama[0] + "と" + yama[1] + "でした。")
                    uranai_flag = False
                while True:
                    c = time.time()
                    if c - globt >= 20:
                        # ==========怪盗のターン==========
                        await mainch.send("人狼のターン。10秒後に怪盗のターンになります。")
                        break
                if jinro_id[1] < ninzu:
                    """
                    ==========人狼が二人共いるとき==========
                    """
                    t = time.time()
                    for i in range(2):
                        jid = jinro_id[i - 1]
                        dm = await playerclass[jinro_id[i]].create_dm()
                        await dm.send("あなたと{}が人狼です。".format(playername[jid]))
                    while True:
                        c = time.time()
                        if c - t >= 10:
                            # ==========怪盗のターン==========
                            await mainch.send("怪盗のターン。20秒後に夜が明けます。")
                            break
                    if kaito_id < ninzu:
                        """
                        ==========怪盗がいるとき==========
                        """
                        globt = time.time()
                        kaito_message = ""
                        for i in range(ninzu):
                            if i == kaito_id:
                                continue
                            else:
                                kaito_message += "「!k{}」: {} \n".format(i, playername[i])
                        dm = await playerclass[kaito_id].create_dm()
                        await dm.send("{} 役職を盗む相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[kaito_id]))
                        await dm.send(kaito_message)
                    else:
                        """
                        ==========怪盗がいないとき==========
                        """
                        sleep(20)
                        # ==========夜明け==========
                        await mainch.send(calleveryone + "夜が明けました。討論を開始してください。")
                        await mainch.send("投票の準備が整いましたら「!投票」とお送りください。")
                        gameflag = 3
                elif jinro_id[1] >= ninzu and jinro_id[0] < ninzu:
                    """
                    ==========人狼が一人のみのとき==========
                    """
                    t = time.time()
                    dm = await playerclass[jinro_id[0]].create_dm()
                    await dm.send("人狼はあなた一人です。")
                    while True:
                        c = time.time()
                        if c - t >= 10:
                            # ==========怪盗のターン==========
                            await mainch.send("怪盗のターン。20秒後に夜が明けます。")
                            break
                    if kaito_id < ninzu:
                        """
                        ==========怪盗がいるとき==========
                        """
                        globt = time.time()
                        kaito_message = ""
                        for i in range(ninzu):
                            if i == kaito_id:
                                continue
                            else:
                                kaito_message += "「!k{}」: {} \n".format(i, playername[i])
                        dm = await playerclass[kaito_id].create_dm()
                        await dm.send("{} 役職を盗む相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[kaito_id]))
                        await dm.send(kaito_message)
                    else:
                        """
                        ==========怪盗がいないとき==========
                        """
                        sleep(20)
                        # ==========夜明け==========
                        await mainch.send(calleveryone + "夜が明けました。討論を開始してください。")
                        await mainch.send("投票の準備が整いましたら「!投票」とお送りください。")
                        gameflag = 3
                elif jinro_id[0] >= ninzu:
                    """
                    ==========人狼がいないとき==========
                    """
                    sleep(10)
                    # ==========怪盗のターン==========
                    await mainch.send("怪盗のターン。20秒後に夜が明けます。")
                    # 人狼がいないので怪盗はいる
                    globt = time.time()
                    kaito_message = ""
                    for i in range(ninzu):
                        if i == kaito_id:
                            continue
                        else:
                            kaito_message += "「!k{}」: {} \n".format(i, playername[i])
                    dm = await playerclass[kaito_id].create_dm()
                    await dm.send("{} 役職を盗む相手を選んでください。以下のコマンドをコピーして送ってください：".format(playername[kaito_id]))
                    await dm.send(kaito_message)
            else:
                dm = await message.author.create_dm()
                await dm.send("占いが完了している、もしくはあなたは占い師ではないようです")

    """
    ==========怪盗がいるとき==========
    """
    
    for i in range(-1, ninzu):
        if message.content == "!k{}".format(i):
            if kaito_flag and message.author == playerclass[kaito_id]:
                dm = await playerclass[kaito_id].create_dm()
                await dm.send("怪盗の結果{}と役職を入れ替え、あなたは{}になりました。".format(playername[i], game.kaitou_change(kaito_id, i)))
                kaito_flag = False
                while True:
                    c = time.time()
                    if c - globt >= 20:
                        # ==========夜明け==========
                        await mainch.send(calleveryone + "夜が明けました。討論を開始してください。")
                        await mainch.send("投票の準備が整いましたら「!投票」とお送りください。")
                        gameflag = 3
                        break
            else:
                dm = await message.author.create_dm()
                await dm.send("怪盗が完了している、もしくはあなたは怪盗ではないようです")


    if message.content == "!投票":
        if gameflag == 3:
            tohyo_message = ""
            for i in range(ninzu):
                tohyo_message += "「!t{}」: {} \n".format(i, playername[i])
            tohyo_message += "「!th」: 平和村"
            await mainch.send(calleveryone + "投票に入ります。各プレイヤーは当アカウント宛に「!t」の後ろに以下の英数字をつけてダイレクトメッセージを送ってください：")
            await mainch.send(tohyo_message)
            await mainch.send("投票結果および試合結果の表示を行う際には「!結果」とお送りください。")
        else:
            await mainch.send("❕ゲームが待機状態になっていない、もしくは夜が明けていないようです。")

    for i in range(ninzu):
        if message.content == "!t{}".format(i):
            tid = playerclass.index(message.author)
            if tohyo_flag[tid][0] == 0 and heiwa_flag[tid] == 0:
                game.tohyo(i)
                await message.channel.send("{} に投票しました。".format(playername[i]))
                tohyo_flag[tid][0] = 1
                tohyo_flag[tid][1] = i
                await mainch.send("{} が投票を完了しました。".format(playername[tid]))
            elif tohyo_flag[tid][0] == 1 and heiwa_flag[tid] == 1:
                heiwa -= 1
                game.tohyo(i)
                await message.channel.send("平和村への投票を取り消し、{} に投票しました。".format(playername[i]))
                tohyo_flag[tid][1] = i
                heiwa_flag[tid] = 0
            elif tohyo_flag[tid][0] == 1 and heiwa_flag[tid] == 0:
                game.untohyo(tohyo_flag[tid][1])
                game.tohyo(i)
                await message.channel.send("{} への投票を取り消し、{} に投票しました。".format(playername[tohyo_flag[tid][1]], playername[i]))
                tohyo_flag[tid][1] = i

    if message.content == "!th":
        tid = playerclass.index(message.author)
        if tohyo_flag[tid][0] == 0:
            heiwa += 1
            await message.channel.send("平和村に投票しました。")
            tohyo_flag[tid][0] = 1
            heiwa_flag[tid] = 1
            await mainch.send("{} が投票を完了しました。".format(playername[tid]))
        else:
            heiwa += 1
            await message.channel.send("{} への投票を取り消し、平和村に投票しました。".format(playername[tohyo_flag[tid][1]]))
            game.untohyo(tohyo_flag[tid][1])
            heiwa_flag[tid] = 1

    if message.content == "!結果":
        kekkaflag = 1
        for i in range(ninzu):
            if tohyo_flag[i][0] == 0:
                kekkaflag *= 0
        if kekkaflag == 1:
            kekka = ""
            for i in range(ninzu):
                kekka += "{} : ".format(playername[i]) + game.yakushoku_winlose(i)
                kekka += "\n"
            tsuri = game.tsuri()
            if heiwa >= game.players()[tsuri[0]][1]:
                await mainch.send(calleveryone + "投票の結果、平和村が選ばれました。")
                sleep(2)
                if game.heiwa():
                    await mainch.send(":first_quarter_moon_with_face: おめでとう！平和村でした。皆さんの勝利です(？)。")
                    await mainch.send(kekka)
                else:
                    await mainch.send(":first_quarter_moon_with_face: なんと！村には人狼が潜んでいました……。人狼チームの勝利です。")
                    await mainch.send(kekka)

            elif len(tsuri) == 1:
                await mainch.send(calleveryone + "投票の結果、{} が処刑されました。".format(playername[tsuri[0]]))
                sleep(2)
                if game.shirokuro_winlose(tsuri[0]) == 0:
                    await mainch.send(":first_quarter_moon_with_face: {}は人間であったため、人狼チームの勝利です。".format(playername[tsuri[0]]))
                    await mainch.send(kekka)
                elif game.shirokuro_winlose(tsuri[0]) == 1:
                    await mainch.send(":first_quarter_moon_with_face: {}は人狼であったため、人間チームの勝利です。".format(playername[tsuri[0]]))
                    await mainch.send(kekka)
            else:
                tsurare = ""
                tninzu = 0
                for i in range(len(tsuri)):
                    tsurare += "{}".format(playername[tsuri[i]])
                    tsurare += "\n"
                    tninzu += 1
                await mainch.send(calleveryone + "投票の結果、" + tsurare + "の{}人が選ばれました。このうちからランダムで処刑します。".format(tninzu))
                random.shuffle(tsuri)
                sleep(2)
                await mainch.send(calleveryone + "おみくじの結果、{} が処刑されました。".format(playername[tsuri[0]]))
                sleep(2)
                if game.shirokuro_winlose(tsuri[0]) == 0:
                    await mainch.send(":first_quarter_moon_with_face: {}は人間であったため、人狼チームの勝利です。".format(playername[tsuri[0]]))
                    await mainch.send(kekka)
                elif game.shirokuro_winlose(tsuri[0]) == 1:
                    await mainch.send(":first_quarter_moon_with_face: {}は人狼であったため、人間チームの勝利です。".format(playername[tsuri[0]]))
                    await mainch.send(kekka)
            heiwa = 0
            gameflag = 1
            tohyo_flag = []
            for i in range(ninzu):
                tohyo_flag.append([0, 0])
                heiwa_flag.append(0)
        else:
            await mainch.send("❕全員の投票が済んでいません。")

    elif message.content == "!人数":
        await message.channel.send("{} 現在の人数は{}人です".format(message.author.mention, ninzu))

    elif message.content == "!遊び方":
        await message.channel.send("https://github.com/tsubasa283paris/OneNightJinroBot/blob/master/README.md")

    if message.content == "!人狼終了":
        await mainch.send(":first_quarter_moon_with_face: ワンナイト人狼を終了します。")
        await mainch.send("Special Thanks アルパカくん。https://twitter.com/smilingAlpaca")
        gameflag = 0
        ninzu = 0
        playername  = []
        playerclass = []
        tohyo_flag  = []

    """
    ==========ここまでワンナイト人狼部分==========
    """

    for c in command:
        if message.content == c[0]:
            await message.channel.send(c[1])

    if message.content == "!じゃあな":
        # ログアウト
        role1 = discord.utils.get(message.guild.roles, name='観戦者')
        await member.remove_roles(role1)
        role0 = discord.utils.get(message.guild.roles, name='参加者')
        await member.remove_roles(role0)
        await message.channel.send("落ちます。お疲れ様でした。")
        await client.logout()


# botの接続と起動
client.run(accesstoken)
