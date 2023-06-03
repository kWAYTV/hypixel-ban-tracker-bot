class Utils:

    def __init__(self):
        self.semaphore = False

    async def change_semaphore(self, state: bool):
        self.semaphore = state

    async def get_semaphore(self):
        return self.semaphore