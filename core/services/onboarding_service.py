from infrastructure.repositories.user_repo import UserRepository
from core.services.gamification_service import GamificationService
from core.services.achievement_service import AchievementService


class OnboardingService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.gamification = GamificationService()
        self.achievements = AchievementService()

    async def needs_onboarding(self, user) -> bool:
        return not getattr(user, "is_onboarded", False)

    async def complete_onboarding(self, user):
        """
        Завершение онбординга:
        - помечаем пользователя как прошедшего онбординг
        - начисляем XP
        - выдаём ачивку
        """
        # 1. Помечаем как прошедшего онбординг
        user.is_onboarded = True
        await self.user_repo.update(user)

        # 2. XP за онбординг
        level, total_xp, earned_xp = await self.gamification.add_xp(
            user,
            xp_amount=50,
            reason="onboarding",
        )

        # 3. Ачивка за онбординг
        achievement = await self.achievements.grant_onboarding(user)

        return {
            "xp": earned_xp,
            "total_xp": total_xp,
            "level": level,
            "achievement": achievement,
        }
