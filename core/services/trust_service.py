from infrastructure.repositories.user_repo import UserRepository


class TrustService:
    def __init__(self):
        self.users = UserRepository()

    async def decrease(self, user, amount: int):
        new_value = max(0, user.trust_score - amount)
        await self.users.update_trust(user.id, new_value)
        return new_value

    async def increase(self, user, amount: int):
        new_value = min(100, user.trust_score + amount)
        await self.users.update_trust(user.id, new_value)
        return new_value

    def xp_multiplier(self, trust_score: int) -> float:
        """
        Множитель XP на основе доверия:

        100 → 1.0 (обычный XP)
        80 → 0.8
        60 → 0.6
        40 → 0.4
        20 → 0.2
        0 → 0
        """
        return trust_score / 100
