# Weather API

## Overview 

This repositiory will using Python Core to call API of OpenWeather to get these information: temperature, humidity, wind speed. 
And the goal of it is optimize numbers call API of OpenWeather because it will use free plan, it has some limit options:
- It has limit call api per minutes
- Only 95% Uptime

So my solution:
- Using parallel API calls to OpenWeather API to optimize waiting time.
- Will cache the response by saving it into json file(maybe Redis after).
- If client need to get weather of city in a bounding box. First check that coordiate have already in the Json file, if yes, will use that information to response to the client. Just call OpenWeather API by coordiate not in json file.
- To not be outdated data information in json file, will use the schedule job libary to call every coordinate in json file to update the waether by 10 minutes.

## Improvement 
My solution has limit, if the record in json is to big. For example, i save 100 hundred city in json file, every 10 minutes, i will call 100 times to update that information. It is not effcient. I will improve it using LRU cache. To be more specific, i will cache the Least Recently Used city by checking the last time it had been searched, if the last time searched is too old, i will remove it from the cache to get more space for another city

I will use cronjob or message queue to call API to update the cache data. It will improve, you can seprate the sever to get information and server to call API. Will have backup server if some sever call API has trouble and reduce resource of main server

## Run my code 🕵️
Insert your api key into store_key.txt



First install requirement.txt by using this command
```
pip install requirement.txt
```

It is a simple python file, so you only need this command to run my code, remember, cd to code file =))

```
python3 main.py
```
```
python3 worker.py
```

