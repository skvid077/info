import asyncio

from database.queries import queries

from database.tasks import main as tasks_main
from database.models import main as models_main
from database.json_models import main as json_models_main

from database.queries import queries


async def main():
    await tasks_main()
    await models_main()
    json_models_main()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
