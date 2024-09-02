import asyncio
#====================================================================

class Queue:

    async def queue(cid, TASKS, wait=1):
        while TASKS[0] != cid:
            await asyncio.sleep(wait)

    async def position(cid, TASKS):
        return TASKS.index(cid) if cid in TASKS else 0

    async def message(imog, text, TASKS, maximum=1):
        if len(TASKS) > maximum:
            try: await imog.edit(text=text)
            except Exception: pass

#====================================================================
