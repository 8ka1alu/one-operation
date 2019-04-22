class Job():
    def __init__(self, jobname, iamjinro, iamteamjinro):
        self.jobname = jobname
        self.iamjinro = iamjinro
        self.iamteamjinro = iamteamjinro

class JobManager():
    def __init__(self):
        # 役職を追加する場合ここに足してください。特殊な行動を持つ場合いろいろ書き換えてください…。
        self.jobs = []
        self.jobs.append(Job("村人", False, False)) # 0
        self.jobs.append(Job("占い師", False, False)) # 1
        self.jobs.append(Job("怪盗", False, False)) # 2
        self.jobs.append(Job("人狼", True, True)) # 以下略
        self.jobs.append(Job("共有者", False, False))
        self.jobs.append(Job("狂人", False, True))

        # デフォルトのカード構成を変更する場合ここを書き換えてください。
        self.cards = {
            4 : [0, 0, 1, 2, 3, 3],
            5 : [0, 0, 0, 1, 2, 3, 3],
            6 : [0, 0, 1, 2, 3, 3, 4, 4],
            7 : [0, 0, 1, 2, 3, 3, 4, 4, 5],
            8 : [0, 0, 0, 1, 2, 3, 3, 4, 4, 5]
        }

    def exchange_card(self, playernum, id_to_remove, id_to_add):
        self.cards[playernum].remove(id_to_remove)
        self.cards[playernum].append(id_to_add)