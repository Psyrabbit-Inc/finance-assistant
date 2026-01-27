class ServicesMiddleware:
    def __init__(self, services: dict):
        self.services = services

    async def __call__(self, handler, event, data):
        data.update(self.services)
        return await handler(event, data)