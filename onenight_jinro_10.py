import random

class OneNightJinro:
    def __init__(self, player_number = "", game_mode = ""): # いずれもstr
        self.player_number = "4"
        self.game_mode = "default"
        global playernum, gamemode, exc
        playernum = int(player_number) # プレイヤー人数
        gamemode = game_mode # ゲーム設定(default以外使うのか…？)
        exc = 0 # 例外処理をidで返す用。0は正常

        # print("人数は{}人で、ゲームモードは".format(playernum) + gamemode + "です")
        global players
        players = [[0, 0] for x in range(playernum + 2)] # players配列
        """
        players配列について
        プレイヤー人数 * (役職, 投票数)　の二次元配列。
        役職は 0 = 村人、1 = 占い師、2 = 怪盗、3 = 人狼
        """

        if playernum < 4:
            exc = 1 # 人数エラー
        if playernum == 4:
            players[0][0] = 0
            players[1][0] = 0
            players[2][0] = 1
            players[3][0] = 2
            players[4][0] = 3
            players[5][0] = 3
        if playernum == 5:
            players[0][0] = 0
            players[1][0] = 0
            players[2][0] = 0
            players[3][0] = 1
            players[4][0] = 2
            players[5][0] = 3
            players[6][0] = 3
        if playernum == 6:
            players[0][0] = 0
            players[1][0] = 0
            players[2][0] = 0
            players[3][0] = 0
            players[4][0] = 1
            players[5][0] = 2
            players[6][0] = 3
            players[7][0] = 3
        if playernum > 6:
            exc = 1

        random.shuffle(players)

    def exc(self):
        return exc

    def players(self):
        return players

    def yakushoku(self, yaku): # 数字もらって役職名を返すだけ用
        if yaku == 0:
            return "村人"
        if yaku == 1:
            return "占い師"
        if yaku == 2:
            return "怪盗"
        if yaku == 3:
            return "人狼"

    def yakushoku_winlose(self, id): # IDもらって役職名を返すだけ用
        if players[id][0] == 0:
            return "村人"
        if players[id][0] == 1:
            return "占い師"
        if players[id][0] == 2:
            return "怪盗"
        if players[id][0] == 3:
            return "人狼"

    def shirokuro(self, yaku): # 数字もらって0人間か1人狼かを返すだけ用
        if yaku <= 2:
            return "人間"
        else:
            return "人狼"

    def shirokuro_winlose(self, id): # IDもらって0人間か1人狼か返す用
        if players[id][0] <= 2:
            return 0
        else:
            return 1
        
    def uranai_check(self, id): # 占い師。idはターゲット
        if id == -1: # -1は山札参照
            yama = [self.shirokuro(players[-1][0]), self.shirokuro(players[-2][0])]
            return yama
        else:
            return players[id][0]

    def kaitou_change(self, id1, id2): # 怪盗。id1はプレイヤー、id2はターゲット
        temp = players[id2][0]
        players[id2][0] = players[id1][0]
        players[id1][0] = temp
        return self.shirokuro(temp)

    def jinro_check(self, id): # 人狼。idはプレイヤー。-1味方がいないかwolfid誰が味方かを返します
        wolfid = -1
        for i in range(len(players) - 2):
            if players[i][0] == 3 and i != id:
                wolfid = i
        return wolfid

    def tohyo(self, id):
        players[id][1] += 1

    def untohyo(self, id):
        players[id][1] -= 1

    def rank(self, data): # 投票結果の比較の材料
        rank = [1 for n in range(len(data))]
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i] < data[j]:
                    rank[i] += 1
        return rank

    def tsuri(self): # 投票結果を返します
        ranked = []
        tsuri = []
        for i in range(len(players) - 2):
            ranked.append(players[i][1])
        ranked = self.rank(ranked)
        for i in range(len(ranked)):
            if ranked[i] == 1:
                tsuri.append(i)
        return tsuri

    def heiwa(self): # 平和村かどうかを返します
        heiwa = True
        for i in range(len(players) - 2):
            if players[i][0] == 3:
                heiwa = False
            else:
                continue
        return heiwa

    def printp(self):
        print(players)

