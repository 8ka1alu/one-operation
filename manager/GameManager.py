"""
工事現場
"""
from manager.PlayerManager import PlayerManager

class GameManager():
    def __init__(self):
        player = PlayerManager()
        self.phase = "standby"

    def phase(self):
        return self.phase

    def commands(self, author, com, id):
        if com == "!参加":
            self.join(author)
        elif com == "!観戦":
            self.watch(author)
        elif com == "!ゲーム開始":
            self.gamestart()
        elif com == "!占い":
            self.diviner(author, id)
        elif com == "!怪盗":
            self.thief(author, id)
        elif com == "!投票開始":
            self.votestart()
        elif com == "!投票":
            self.vote(author, id)
        elif com == "!結果":
            self.result()
        return [self.chatflag, self.chat]

    def join(self, author):
        self.chatflag = "mainch"
        self.chat = self.player.add(author)

    def watch(self, author):
        self.player.watch
