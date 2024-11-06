# Weather API

## Overview 

This repository will utilize Python Core to call the OpenWeather API to retrieve temperature, humidity, and wind speed data. The primary objective is to optimize the number of API calls to OpenWeather due to limitations in the free plan, which includes:

- Rate Limits: A maximum number of API calls per minute
- Uptime: 95% uptime guarantee

Proposed Solution:

To address these constraints, we will implement the following strategies:

- Parallel API Calls:

  - Simultaneously make multiple API calls to OpenWeather to minimize waiting time.
- Response Caching:

  - Store API responses in JSON files (or potentially Redis later) to reduce the need for redundant calls.
  - When a client requests weather information for a city within a bounding box, first check the JSON file.
  - If the coordinates are found, return the cached data.
  - Otherwise, make an API call to fetch the missing data.
- Data Freshness:

  - Employ a scheduling library to periodically update the cached weather data for all coordinates in the JSON file, ensuring data freshness.
  - A 10-minute interval is suggested for these updates.

## Improvement 
To address the scalability issue of a large JSON file, we can implement an LRU (Least Recently Used) cache. This strategy will prioritize the caching of frequently accessed cities, while removing less frequently used ones to optimize cache space.

To update the cache efficiently, we can utilize a cron job or a message queue system. This approach allows for the separation of the server that handles client requests from the server that makes API calls. This separation can improve performance and resource utilization. Additionally, we can implement a backup server to ensure redundancy and minimize downtime in case of API call failures on the primary server.

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

