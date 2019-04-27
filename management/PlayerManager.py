import discord
import random
from JobManager import JobManager

class PlayerManager():
    def __init__(self):
        # players = [["PLAYER1#1234", "PLAYER2#5678", ...], [0, 1, ...](役職), ["n", "2", ...](投票先)]
        self.players = [[], [], []]
        # watchers = ["PLAYER1#1234", "PLAYER2#5678", ...]
        self.watchers = []
        self.job = JobManager()

    def playernum(self):
        return len(self.players[0])

    def reset(self):
        for i in range(self.playernum()):
            self.players[2][i] = "n"

    def add(self, author):
        if not author in self.watchers:
            if not author in self.players[0]:
                self.players[0].append(author)
                self.players[2].append("n")
                return "{} 参加承りました。現在の人数は{}人です。".format(author.mention, len(self.players[0]))
            else:
                id = self.players[0].index(author)
                self.players[0].pop(id)
                self.players[2].pop(id)
                return "{} 参加を取り消しました。現在の人数は{}人です。".format(author.mention, len(self.players[0]))
        else:
            return "{} :confounded: 観戦状態になっています。ゲーム参加を行うには観戦を取り消してください。".format(author.mention)

    def watch(self, author):
        if not author in self.players[0]:
            if not author in self.watchers:
                self.watchers.append(author)
                return "{} 観戦を承りました。".format(author.mention)
            else:
                id = self.watchers.index(author)
                self.watchers.pop(id)
                return "{} 観戦を取り消しました。".format(author.mention)
        else:
            return "{} :confounded: ゲーム参加状態になっています。観戦を行うには参加を取り消してください。".format(author.mention)

    def get_all_mention(self):
        ment = ""
        for i in range(len(self.players[0])):
            ment += "{} ".format(self.players[i].mention)
        return ment
            
    def shufflejob(self):
        joblist = self.job.cards[self.playernum()]
        random.shuffle(joblist)
        self.players[1] = joblist

    def thiefchange(self, id1, id2):
        temp = self.players[1][id2]
        self.players[1][id2] = self.players[1][id1]
        self.players[1][id1] = temp