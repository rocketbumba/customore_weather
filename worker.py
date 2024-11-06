import asyncio
import time

import aiohttp
import json
import schedule
import main




async def job():
    cache_data = main.read_dict_from_txt('hiep.json')
    async with aiohttp.ClientSession() as session:
        tasks = []
        results = {}
        for lat, lon in cache_data.keys():
            tasks.append(asyncio.create_task(main.fetch_weather(session, lat=lat, lon=lon)))
            results = await asyncio.gather(*tasks)
        cache_data = {}
        for item in results:
            for key, value in item.items():
                cache_data[key] = value
    main.save_dict_to_txt(cache_data, 'hiep.json')

def run_scheduler():
    schedule.every(10).minute.do(lambda : asyncio.run(job()))

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()