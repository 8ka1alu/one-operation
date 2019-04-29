import discord
import random
from PlayerManager import PlayerManager
from JobManager import JobManager

class GameManager():
    def __init__(self):
        self.player = PlayerManager()
        self.phase = "standby"
        self.divinerflag = True # 行動可能
        self.thiefflag = True
        self.winloseflag = 0 # 0であれば人間側の勝利、1であれば人狼側の勝利

    def reset(self):
        self.phase = "standby"
        self.player.reset()
        self.divinerflag = True
        self.thiefflag = True

    def setjob(self):
        self.player.shufflejob()
        retchat = [[], []]
        for i in range(self.player.playernum()):
            retchat[0][i] = self.player.players[0][i]
            retchat[1][i] = "{} あなたの役職は{}です。".format(
                retchat[0][i].mention,
                JobManager().get_job_name(self.player.players[1][i])
            )
        return retchat

    def jobmessage(self):
        retchat = [[], []]
        ment = []
        temp = self.player.players
        wolfid, twinid = [], []
        for i in range(self.player.playernum()):
            ment.append(temp[0][i].mention)
            if temp[1][i] == 3:
                wolfid.append(i)
            elif temp[1][i] == 4:
                twinid.append(i)
        for i in range(self.player.playernum()):
            if temp[1][i] == 1:
                retchat[0].append(temp[0][i])
                mes = ":six_pointed_star: 占う対象を選び、以下のコマンドを送ってください。\n"
                for j in range(len(ment)):
                    if i != j:
                        mes += "「!占い {}」: {}\n".format(j, ment[j])
                mes += "「!占い d」: 山札"
                retchat[1].append(mes)
            elif temp[1][i] == 2:
                retchat[0].append(temp[0][i])
                mes = ":tophat: 役職を盗む対象を選び、以下のコマンドを送ってください。\n"
                for j in range(len(ment)):
                    if i != j:
                        mes += "「!怪盗 {}」: {}\n".format(j, ment[j])
                retchat[1].append(mes)
            elif temp[1][i] == 3:
                retchat[0].append(temp[0][i])
                if len(wolfid) == 1:
                    retchat[1].append(":wolf: 人狼はあなた一人です。")
                elif len(wolfid) == 2:
                    if i == wolfid[0]:
                        wolfment = ment[wolfid[1]]
                    elif i == wolfid[1]:
                        wolfment = ment[wolfid[0]]
                    retchat[1].append(":wolf: 人狼はあなたと{}の二人です。".format(wolfment))
            elif temp[1][i] == 4:
                retchat[0].append(temp[0][i])
                if len(twinid) == 1:
                    retchat[1].append(":two_women_holding_hands:  共有者はあなた一人です。")
                elif len(twinid) == 2:
                    if i == twinid[0]:
                        twinment = ment[twinid[1]]
                    elif i == twinid[1]:
                        twinment = ment[twinid[0]]
                    retchat[1].append(":wolf: 共有者はあなたと{}の二人です。".format(twinment))
        return retchat

    def watchmessage(self):
        retchat = [[], []]
        temp = self.player.players
        tempj = JobManager()
        mes = ""
        for i in range(self.player.playernum()):
            mes += "{}: {}\n".format(
                temp[0][i],
                tempj.get_job_name(temp[1][i])
            )
        mes += "山札: {}, {}".format(
            tempj.get_job_name(temp[1][-2]),
            tempj.get_job_name(temp[1][-1])
        )
        for w in self.player.watchers:
            retchat[0].append(w)
        retchat[1] = mes
        return retchat

    def commands(self, author, com, id, id2):
        if com == "!参加":
            self.join(author)
        elif com == "!観戦":
            self.watch(author)
        elif com == "!人数":
            self.confirm_num()
        elif com == "!ゲーム開始":
            self.gamestart()
        elif com == "!占い":
            self.diviner(author, id)
        elif com == "!怪盗":
            self.thief(author, id)
        elif com == "!投票":
            self.vote(author, id)
        elif com == "!結果":
            self.result()
        elif com == "!GM投票":
            self.gmvote(id, id2)
        return [self.chatflag, self.chat]

    def join(self, author):
        self.chatflag = "mainch"
        self.chat = self.player.add(author)

    def watch(self, author):
        self.chatflag = "mainch"
        self.chat = self.player.watch(author)

    def confirm_num(self):
        self.chatflag = "mainch"
        num = self.player.playernum()
        self.chat = "現在の参加人数は{}人です。".format(num)

    def gamestart(self):
        self.chatflag = "mainch"
        self.chat = self.player.get_all_mention() + "\n:wolf: {}人でのワンナイト人狼ゲームを開始します。\nゲーム参加者へDMにて役職を通知しました。10秒後に夜になります。".format(len(self.player.players[0]))
        self.phase = "night"

    def diviner(self, author, id):
        self.chatflag = "dm"
        divinerid = self.player.players[0].index(author)
        tempj = JobManager()
        if self.player.players[1][divinerid] == 1 and self.divinerflag:
            if id == "d":
                self.chat = "山札は{}と{}です。".format(
                    tempj.get_job_name(self.player.players[1][-2]),
                    tempj.get_job_name(self.player.players[1][-1])
                )
                self.divinerflag = False
            else:
                try:
                    id = int(id)
                    self.chat = "{}は{}です。".format(
                        self.player.players[0][id].mention,
                        tempj.get_job_name(self.player.players[1][id])
                    )
                    self.divinerflag = False
                except:
                    self.chat = ":tired_face: 無効なコマンドです。上記よりコマンドをコピーしてご利用ください。"
        else:
            self.chat = ":thinking: あなたは占い師ではない、もしくはすでに占いが完了しているようです。"

    def thief(self, author, id):
        self.chatflag = "dm"
        thiefid = self.player.players[0].index(author)
        tempj = JobManager()
        if self.player.players[1][thiefid] == 1 and self.thiefflag:
            try:
                id = int(id)
                self.chat = "{}と役職を入れ替えました。あなたは現在{}です。".format(
                    self.player.players[0][id].mention,
                    tempj.get_job_name(self.player.players[1][id])
                )
                self.player.thiefchange(thiefid, id)
                self.thiefflag = False
            except:
                self.chat = ":tired_face: 無効なコマンドです。上記よりコマンドをコピーしてご利用ください。"
        else:
            self.chat = ":thinking: あなたは怪盗ではない、もしくはすでに怪盗が完了しているようです。"

    def vote(self, author, id):
        self.chatflag = "dm"
        voteid = self.player.players[0].index(author)
        if id == "p":
            self.player.players[2][voteid] = id
            self.chat = "平和村に投票しました。"
            return
        else:
            for i in range(self.player.playernum()):
                if id == "{}".format(i):
                    self.player.players[2][voteid] = id
                    self.chat = "{}に投票しました。".format(self.player.players[0][i].mention)
                    return
            self.chat = ":tired_face: 無効なコマンドです。テキストチャンネルよりコマンドをコピーしてご利用ください。"
        
    def result(self):
        self.chatflag = "mainch"
        if "n" in self.player.players[2]:
            self.chat = ":hushed: まだ全員の投票が済んでいないようです。"
            return
        votelist = [0 for i in range(self.player.playernum())]
        peace = 0
        for i in range(self.player.playernum()):
            if self.player.players[2][i] == "p":
                peace += 1
            else:
                votelist[int(self.player.players[2][i])] += 1
        ranked = self.rank(votelist)
        tsuri = []
        for i in range(len(ranked)):
            if ranked[i] == 1:
                tsuri.append(i)
        if peace > votelist[tsuri[0]]:
            self.chat = "投票の結果、平和村が選ばれました。"
            self.is_peace()
        elif len(tsuri) == 1:
            self.chat = "投票の結果、{}が処刑されました。".format(self.player.players[0][tsuri[0]].mention)
            self.kill(tsuri[0])
        elif len(tsuri) >= 2:
            random.shuffle(tsuri)
            self.chat = "投票の結果、{}が処刑されました。(ランダム)".format(self.player.players[0][tsuri[0]].mention)
            self.kill(tsuri[0])

    def rank(self, data):
        rank = [1 for n in range(len(data))]
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i] < data[j]:
                    rank[i] += 1
        return rank

    def kill(self, id):
        if self.player.players[1][id] == 3:
            self.winloseflag = 0
        else:
            self.winloseflag = 1

    def is_peace(self):
        if self.player.players[1][-2] == 3 and self.player.players[1][-1] == 3:
            self.winloseflag = 0
        else:
            self.winloseflag = 1

    def gmvote(self, id1, id2):
        self.chatflag = "mainch"
        if id2 == "p":
            self.player.players[2][int(id1)] = id2
            self.chat = "平和村に投票しました。"
            return
        else:
            for i in range(self.player.playernum()):
                if id2 == "{}".format(i):
                    self.player.players[2][int(id1)] = id2
                    self.chat = "{}に投票しました。".format(self.player.players[0][i].mention)
                    return
    
    def votemessage(self):
        retchat = "以下のコマンドをコピーして投票を行ってください。\n"
        for i in range(self.player.playernum()):
            retchat += "「!投票 {}」: {}\n".format(i, self.player.players[0][i].mention)
        retchat += "「!投票 p」: 平和村"
        return retchat

    def getresult(self):
        humanlist, wolflist = [], []
        tempj = JobManager()
        for i in range(self.player.playernum()):
            if tempj.jobs[self.player.players[1][i]].iamteamwolf:
                wolflist.append(i)
            else:
                humanlist.append(i)
        humans, wolfs = [], []
        for h in humanlist:
            humans.append("{}: {}\n".format(
                self.player.players[0][h].mention,
                tempj.jobs[self.player.players[1][h]].jobname
            ))
        for w in wolflist:
            wolfs.append("{}: {}\n".format(
                self.player.players[0][h].mention,
                tempj.jobs[self.player.players[1][h]].jobname
            ))
        if self.winloseflag == 0:
            mes = "村人チームの勝利です。\n"
            for h in humans:
                mes += ":trophy: " + h
            for w in wolfs:
                mes += ":flag_white: " + w
        else:
            mes = "人狼チームの勝利です。\n"
            for w in wolfs:
                mes += ":trophy: " + w
            for h in humans:
                mes += ":flag_white: " + h
        return mes