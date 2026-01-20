from infrastructure.repositories.antifraud_repo import AntiFraudRepository
from core.services.trust_service import TrustService


class AntiFraudService:
    MAX_TX_PER_MINUTE = 5
    MAX_TX_AMOUNT = 10_000_000

    def __init__(self):
        self.repo = AntiFraudRepository()
        self.trust = TrustService()

    async def validate_transaction(self, user, amount: float) -> bool:
        await self.repo.log(user.id, "transaction", amount)

        # слишком частые транзакции
        recent = await self.repo.count_recent(user.id, "transaction", minutes=1)
        if recent > self.MAX_TX_PER_MINUTE:
            await self.trust.decrease(user, 10)  # -10 доверия
            return False

        # слишком большие суммы
        if amount > self.MAX_TX_AMOUNT:
            await self.trust.decrease(user, 20)  # -20 доверия
            return False

        # нормальное поведение — даём награду доверием
        await self.trust.increase(user, 1)

        return True
