Overview
This repositiory will using Python to call OpenWeather API to get: temperature, humidity, wind speed
Analysis Free Openweather API
- It has limit call api perday
So we need to limit call api. How can i do that?
-> I will cache the response request by saving it into txt file(maybe Redis after)
If user input call their bounding, i will check the corridate have already in the txt file. If yes, i will use that result store in txt to response to client, if not, i will use that coordinate to call api to Openweather

To not be outdated data information, i will use the worker to call every coordinate in txt file to update the waether by 10 minutes
