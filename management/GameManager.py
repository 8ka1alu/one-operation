import discord
import random
from management.PlayerManager import PlayerManager
from management.JobManager import JobManager

class GameManager():
    def __init__(self):
        self.player = PlayerManager()
        self.phase = "standby"
        self.divinerflag = True # 行動可能
        self.thiefflag = True
        self.winloseflag = 0 # 0であれば人間側の勝利、1であれば人狼側の勝利

    def initiate(self):
        self.phase = "standby"
        self.player.reset()
        self.divinerflag = True
        self.thiefflag = True
        self.winloseflag = 0

    def setjob(self):
        self.phase = "night"
        self.player.shufflejob()
        retchat = [[], []]
        for i in range(self.player.playernum()):
            retchat[0].append(self.player.playerid[i])
            retchat[1].append("{} あなたの役職は{}です。".format(
                retchat[0][i].mention,
                JobManager().get_job_name(self.player.playerjob[i])
            ))
        return retchat

    def jobmessage(self):
        retchat = [[], []]
        ment = []
        wolfid, twinid = [], []
        for i in range(self.player.playernum()):
            ment.append(self.player.playerid[i].mention)
            if self.player.playerjob[i] == 3:
                wolfid.append(i)
            elif self.player.playerjob[i] == 4:
                twinid.append(i)
        for i in range(self.player.playernum()):
            if self.player.playerjob[i] == 1:
                retchat[0].append(self.player.playerid[i])
                mes = ":six_pointed_star: 占う対象を選び、以下のコマンドを送ってください。\n"
                for j in range(len(ment)):
                    if i != j:
                        mes += "「!占い {}」: {}\n".format(j, ment[j])
                mes += "「!占い d」: 山札"
                retchat[1].append(mes)
            elif self.player.playerjob[i] == 2:
                retchat[0].append(self.player.playerid[i])
                mes = ":tophat: 役職を盗む対象を選び、以下のコマンドを送ってください。\n"
                for j in range(len(ment)):
                    if i != j:
                        mes += "「!怪盗 {}」: {}\n".format(j, ment[j])
                retchat[1].append(mes)
            elif self.player.playerjob[i] == 3:
                retchat[0].append(self.player.playerid[i])
                if len(wolfid) == 1:
                    retchat[1].append(":wolf: 人狼はあなた一人です。")
                elif len(wolfid) == 2:
                    if i == wolfid[0]:
                        wolfment = ment[wolfid[1]]
                    elif i == wolfid[1]:
                        wolfment = ment[wolfid[0]]
                    retchat[1].append(":wolf: 人狼はあなたと{}の二人です。".format(wolfment))
            elif self.player.playerjob[i] == 4:
                retchat[0].append(self.player.playerid[i])
                if len(twinid) == 1:
                    retchat[1].append(":two_women_holding_hands: 共有者はあなた一人です。")
                elif len(twinid) == 2:
                    if i == twinid[0]:
                        twinment = ment[twinid[1]]
                    elif i == twinid[1]:
                        twinment = ment[twinid[0]]
                    retchat[1].append(":two_women_holding_hands: 共有者はあなたと{}の二人です。".format(twinment))
            elif self.player.playerjob[i] == 5:
                retchat[0].append(self.player.playerid[i])
                if len(wolfid) == 0:
                    retchat[1].append(":spy: 人狼はいません。")
                if len(wolfid) == 1:
                    wolfment = ment[wolfid[0]]
                    retchat[1].append(":spy: 人狼は{}の一人です。".format(wolfment))
                elif len(wolfid) == 2:
                    wolfment = [ment[wolfid[0]], ment[wolfid[1]]]
                    retchat[1].append(":spy: 人狼は{}と{}の二人です。".format(wolfment[0], wolfment[1]))
        return retchat

    def watchmessage(self):
        retchat = [[], []]
        tempj = JobManager()
        mes = ""
        for i in range(self.player.playernum()):
            mes += "{}: {}\n".format(
                self.player.playerid[i].mention,
                tempj.get_job_name(self.player.playerjob[i])
            )
        mes += "山札: {}, {}".format(
            tempj.get_job_name(self.player.playerjob[-2]),
            tempj.get_job_name(self.player.playerjob[-1])
        )
        for w in self.player.watcherid:
            retchat[0].append(w)
        retchat[1] = mes
        return retchat

    def watchmessage_thief(self):
        retchat = [[], []]
        for w in self.player.watcherid:
            retchat[0].append(w)
        if self.thiefflag == True:
            retchat[1] = "怪盗は行動をしませんでした。"
        else:
            retchat[1] = "怪盗は{}と役職を交換し、{}になりました。".format(
                self.player.playerid[self.thieftarget].mention,
                JobManager().jobs[self.player.playerjob[self.thiefid]].jobname
            )
        return retchat


    def commands(self, author, com, id, id2):
        if com == "!参加":
            self.join(author)
        elif com == "!観戦":
            self.watch(author)
        elif com == "!参加者":
            self.confirm_player()
        elif com == "!開始":
            self.gamestart()
        elif com == "!参加者リセット":
            self.playerreset()
        elif com == "!占い":
            self.diviner(author, id)
        elif com == "!怪盗":
            self.thief(author, id)
        elif com == "!投票":
            self.vote(author, id)
        elif com == "!GM投票":
            self.gmvote(id, id2)
        return [self.chatflag, self.chat]

    def join(self, author):
        self.chatflag = "mainch"
        self.chat = self.player.add(author)

    def watch(self, author):
        self.chatflag = "mainch"
        self.chat = self.player.watch(author)

    def confirm_player(self):
        self.chatflag = "mainch"
        num = self.player.playernum()
        mes = self.player.get_all_mention()
        self.chat = "現在の参加者は" + mes + "の{}人です。".format(num)

    def gamestart(self):
        self.chatflag = "mainch"
        if self.player.playernum() >= 4 and self.player.playernum() <= 8:
            self.chat = self.player.get_all_mention() + "\n:wolf: {}人でのワンナイト人狼ゲームを開始します。\nゲーム参加者へDMにて役職を通知しました。10秒後に夜になります。".format(len(self.player.playerid))
            self.startable = True
        else:
            self.chat = "ゲーム人数が足りない、もしくは多すぎるようです。「!参加者」で参加人数を確認してください。"
            self.startable = False

    def playerreset(self):
        self.chatflag = "mainch"
        self.player.initiate()
        self.chat = "参加者情報をリセットしました。"

    def diviner(self, author, id):
        self.chatflag = "dm"
        actorid = self.player.playerid.index(author)
        tempj = JobManager()
        if self.player.playerjob[actorid] == 1 and self.divinerflag:
            if id == "d":
                self.chat = "山札は{}と{}です。".format(
                    tempj.get_job_name(self.player.playerjob[-2]),
                    tempj.get_job_name(self.player.playerjob[-1])
                )
                self.divinerflag = False
            else:
                try:
                    id = int(id)
                    self.chat = "{}は{}です。".format(
                        self.player.playerid[id].mention,
                        tempj.get_job_name(self.player.playerjob[id])
                    )
                    self.divinerflag = False
                except:
                    self.chat = ":tired_face: 無効なコマンドです。上記よりコマンドをコピーしてご利用ください。"
        else:
            self.chat = ":thinking: あなたは占い師ではない、もしくはすでに占いが完了しているようです。"

    def thief(self, author, id):
        self.chatflag = "dm"
        actorid = self.player.playerid.index(author)
        tempj = JobManager()
        if self.player.playerjob[actorid] == 2 and self.thiefflag:
            try:
                id = int(id)
                self.chat = "{}と役職を入れ替えました。あなたは現在{}です。".format(
                    self.player.playerid[id].mention,
                    tempj.get_job_name(self.player.playerjob[id])
                )
                self.thiefflag = False
                self.thiefid = actorid
                self.thieftarget = id
            except:
                self.chat = ":tired_face: 無効なコマンドです。上記よりコマンドをコピーしてご利用ください。"
        else:
            self.chat = ":thinking: あなたは怪盗ではない、もしくはすでに怪盗が完了しているようです。"

    def vote(self, author, id):
        self.chatflag = "dm"
        voteid = self.player.playerid.index(author)
        if id == "p":
            self.player.votetarget[voteid] = id
            self.chat = "平和村に投票しました。"
            return
        else:
            for i in range(self.player.playernum()):
                if id == "{}".format(i):
                    self.player.votetarget[voteid] = id
                    self.chat = "{}に投票しました。".format(self.player.playerid[i].mention)
                    return
            self.chat = ":tired_face: 無効なコマンドです。テキストチャンネルよりコマンドをコピーしてご利用ください。"
        
    def result(self):
        votelist = [0 for i in range(self.player.playernum())]
        peace = 0
        for i in range(self.player.playernum()):
            if self.player.votetarget[i] == "p":
                peace += 1
            else:
                votelist[int(self.player.votetarget[i])] += 1
        ranked = self.rank(votelist)
        tsuri = []
        for i in range(len(ranked)):
            if ranked[i] == 1:
                tsuri.append(i)
        if peace > votelist[tsuri[0]]:
            self.chat = "投票の結果、平和村が選ばれました。"
            self.is_peace()
        elif len(tsuri) == 1:
            self.chat = "投票の結果、{}が処刑されました。".format(self.player.playerid[tsuri[0]].mention)
            self.kill(tsuri[0])
        elif len(tsuri) >= 2:
            random.shuffle(tsuri)
            self.chat = "投票の結果、{}が処刑されました。(ランダム)".format(self.player.playerid[tsuri[0]].mention)
            self.kill(tsuri[0])

    def rank(self, data):
        rank = [1 for n in range(len(data))]
        for i in range(len(data)):
            for j in range(len(data)):
                if data[i] < data[j]:
                    rank[i] += 1
        return rank

    def kill(self, id):
        if self.player.playerjob[id] == 3:
            self.winloseflag = 0
        else:
            self.winloseflag = 1

    def is_peace(self):
        if self.player.playerjob[-2] == 3 and self.player.playerjob[-1] == 3:
            self.winloseflag = 0
        else:
            self.winloseflag = 1

    def gmvote(self, id1, id2):
        self.chatflag = "mainch"
        if id2 == "p":
            self.player.votetarget[int(id1)] = id2
            self.chat = "平和村に投票しました。"
            return
        else:
            for i in range(self.player.playernum()):
                if id2 == "{}".format(i):
                    self.player.votetarget[int(id1)] = id2
                    self.chat = "{}に投票しました。".format(self.player.playerid[i].mention)
                    return

    def thiefact(self):
        if not self.thiefflag:
            self.player.thiefchange(self.thiefid, self.thieftarget)

    def getcardslist(self):
        retchat = "現在のカード構成は以下の通りです。\n"
        tempj = JobManager()
        for i in range(self.player.playernum() + 2):
            c = tempj.cards[self.player.playernum()][i]
            retchat += tempj.jobs[c].jobname + " "
        return retchat
    
    def votemessage(self):
        retchat = "以下のコマンドをコピーして投票を行ってください。\n"
        for i in range(self.player.playernum()):
            retchat += "「!投票 {}」: {}\n".format(i, self.player.playerid[i].mention)
        retchat += "「!投票 p」: 平和村"
        return retchat

    def vote_is_complete(self):
        if "n" in self.player.votetarget:
            return False
        else:
            return True

    def getresult(self):
        humanlist, wolflist = [], []
        tempj = JobManager()
        for i in range(self.player.playernum()):
            if tempj.jobs[self.player.playerjob[i]].iamteamwolf:
                wolflist.append(i)
            else:
                humanlist.append(i)
        humans, wolfs = [], []
        for h in humanlist:
            humans.append("{}: {}\n".format(
                self.player.playerid[h].mention,
                tempj.jobs[self.player.playerjob[h]].jobname
            ))
        for w in wolflist:
            wolfs.append("{}: {}\n".format(
                self.player.playerid[w].mention,
                tempj.jobs[self.player.playerjob[w]].jobname
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
        self.initiate()
        return mes