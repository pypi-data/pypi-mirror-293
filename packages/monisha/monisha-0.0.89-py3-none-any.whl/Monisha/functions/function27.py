import asyncio
#====================================================================

class Queue:

    def __init__(self, wait=1, workers=1):
        self.working = []
        self.waiting = wait
        self.workers = workers

    async def waiting(self, tasks):
        while len(tasks) >= self.workers:
            await asyncio.sleep(self.waiting)
    
#====================================================================
