# Arduino Environmental Alert System

It is a system that will allow you to monitor the temperature and humidity in your apartment, for example. It is very easy to set up and allows you to do a lot of things.

## Why did I do this?

I wanted to create some project with Arduino that could measure temperature and humidity and then send it to a PC. I also wanted to experiment and this seemed like a good idea.

## Features

- Ability to send emails
- Ability to create graphs and data into tables
- 24/7 monitoring possible
- Buzzer warning when limits are exceeded

## Scripts

Everything works on the Arduino code, which collects data and then the Python code on the PC monitors it.

## How it works?

The DHT11 sends information to the Arduino, which is programmed to send information at 9600. It is then taken over by python code, which monitors the information and if the temperature/humidity is outside the allowed range, it sends an email!

![image](https://github.com/mavory/Arduino-Environmental-Alert-System/blob/main/Photos/DHT11%20(1).png?raw=true)
