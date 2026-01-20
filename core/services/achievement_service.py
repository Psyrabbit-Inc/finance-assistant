from infrastructure.repositories.achievement_repo import AchievementRepository


class AchievementService:

    def __init__(self):
        self.repo = AchievementRepository()

    async def grant_first_transaction(self, user):
        if not await self.repo.exists(user.id, "FIRST_TRANSACTION"):
            return await self.repo.add(
                user.id,
                "FIRST_TRANSACTION",
                "Первая транзакция 🎉",
                "Ты сделал первый шаг в финансовой осознанности!",
            )

    async def grant_streak_3(self, user, streak: int):
        if streak >= 3 and not await self.repo.exists(user.id, "STREAK_3"):
            return await self.repo.add(
                user.id,
                "STREAK_3",
                "3 дня подряд 🔥",
                "Ты уже 3 дня подряд ведешь учёт!",
            )

    async def grant_streak_7(self, user, streak: int):
        if streak >= 7 and not await self.repo.exists(user.id, "STREAK_7"):
            return await self.repo.add(
                user.id,
                "STREAK_7",
                "7 дней подряд 🔥🔥",
                "Неделя финансовой дисциплины!",
            )

    async def grant_level_3(self, user, level: int):
        if level >= 3 and not await self.repo.exists(user.id, "LEVEL_3"):
            return await self.repo.add(
                user.id,
                "LEVEL_3",
                "3 уровень 🥉",
                "Ты достиг 3 уровня мастерства!",
            )

    async def grant_level_5(self, user, level: int):
        if level >= 5 and not await self.repo.exists(user.id, "LEVEL_5"):
            return await self.repo.add(
                user.id,
                "LEVEL_5",
                "5 уровень 🥇",
                "Ты добрался до 5 уровня — серьёзная заявка!",
            )

    async def grant_onboarding(self, user):
        CODE = "ONBOARDING_COMPLETE"

        exists = await self.repo.exists(user.id, CODE)
        if exists:
            return None

        return await self.repo.add(
            user_id=user.id,
            code=CODE,
            name="Первый шаг!",
            description="Ты прошёл онбординг и получил свою первую награду 🎉"
        )

