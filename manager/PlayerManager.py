"""
工事現場
"""
import discord

class PlayerMaster():
    def __init__(self):
        # players = [["PLAYER1#1919", "PLAYER2#0364", ...], ["villager", "diviner", ...], [0, 0, ...]]
        self.players = []

    def add(self, author):
        if not author in self.players[0]:
            self.players[0].append(author)
            self.players[1].append("null")
            self.players[2].append(0)
            return "{} 参加承りました。現在の人数は{}人です。".format(author.mention, len(self.players[0]))
        else:
            id = self.players[0].index(author)
            self.players[0].pop(id)
            self.players[1].pop(id)
            self.players[2].pop(id)
            return "{} 参加を取り消しました。現在の人数は{}人です。".format(author.mention, len(self.players[0]))