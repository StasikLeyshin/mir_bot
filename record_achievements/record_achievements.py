



class record_achievements:

    def __init__(self, create_mongo, user_id):
        self.create_mongo = create_mongo
        self.user_id = user_id
        self.warn_awards = {
            1: "С почином, добро пожаловать на контроль",
            3: "На бан уже заработал, будем посмотреть",
            5: "Как ты только бан не получил? Или получил? Ну, всякое бывает",
            10: "FBI OPEN UP!",
            20: "Админ, ты в курсе, что есть перманентный бан? Двадцать варнов это уже ту мач"
        }
        self.ban_awards = {
            1: "Любопытно, стоит ли ждать назад?",
            2: "Посмотрите на это, урок не был усвоен. Не делайте так",
            5: "КТО ИЗ АДМИНОВ ТВОЙ ДРУГ? ПРИЗНАВАЙСЯ!",
            7: "Админ, он неисправим, одумайся",
            10: "Никаких больше вечеринок. Я отказываюсь давать разбан"
        }

    async def run(self, kol_warn=0, kol_ban=0, achievement=" ", ach_kol=0):
        msg = []
        ban = 0
        warn_chek = False
        ban_chek = False
        res = 0
        if int(kol_warn) in self.warn_awards:
            msg.append(f"🏅 {self.warn_awards[int(kol_warn)]}")
            res = await self.create_mongo.profile_users_add(self.user_id, f"🏅 {self.warn_awards[int(kol_warn)]}", -3)
            warn_chek = True
        if int(kol_ban) in self.ban_awards:
            msg.append(f"🎖 {self.ban_awards[int(kol_ban)]}")
            res = await self.create_mongo.profile_users_add(self.user_id, f"🎖 {self.ban_awards[int(kol_ban)]}", -8)
            ban_chek = True

        if not warn_chek and kol_warn != 0:
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-3)
        if not ban_chek and kol_ban != 0:
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)

        if achievement != " ":
            res = await self.create_mongo.profile_users_add(self.user_id, f"{achievement}", ach_kol)

        if res[1] <= -50:
            ban = 2
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)
            return ban, msg, res[1]

        if res[1] <= -30:
            ban = 1
            res = await self.create_mongo.profile_users_add(self.user_id, scores=-8)
            return ban, msg, res[1]

        return ban, msg, res[1]


