import discord
import random
from management.JobManager import JobManager

class PlayerManager():
    def __init__(self):
        self.playerid = []
        self.playerjob = []
        self.votetarget = []
        self.watcherid = []
        self.job = JobManager()

    def initiate(self):
        self.playerid = []
        self.playerjob = []
        self.votetarget = []
        self.watcherid = []
        self.job = JobManager()

    def playernum(self):
        return len(self.playerid)

    def reset(self):
        for i in range(self.playernum()):
            self.votetarget[i] = "n"

    def add(self, author):
        if not author in self.watcherid:
            if not author in self.playerid:
                self.playerid.append(author)
                self.votetarget.append("n")
                return "{} 参加承りました。現在の人数は{}人です。".format(author.mention, len(self.playerid))
            else:
                id = self.playerid.index(author)
                self.playerid.pop(id)
                self.votetarget.pop(id)
                return "{} 参加を取り消しました。現在の人数は{}人です。".format(author.mention, len(self.playerid))
        else:
            return "{} :confounded: 観戦状態になっています。ゲーム参加を行うには観戦を取り消してください。".format(author.mention)

    def watch(self, author):
        if not author in self.playerid:
            if not author in self.watcherid:
                self.watcherid.append(author)
                return "{} 観戦を承りました。".format(author.mention)
            else:
                id = self.watcherid.index(author)
                self.watcherid.pop(id)
                return "{} 観戦を取り消しました。".format(author.mention)
        else:
            return "{} :confounded: ゲーム参加状態になっています。観戦を行うには参加を取り消してください。".format(author.mention)

    def get_all_mention(self):
        ment = ""
        for i in range(len(self.playerid)):
            ment += "{} ".format(self.playerid[i].mention)
        return ment
            
    def shufflejob(self):
        joblist = self.job.cards[self.playernum()]
        random.shuffle(joblist)
        self.playerjob = joblist

    def thiefchange(self, id1, id2):
        temp = self.playerjob[id2]
        self.playerjob[id2] = self.playerjob[id1]
        self.playerjob[id1] = temp