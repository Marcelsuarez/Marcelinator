# Marcelinator
Python based Discord Bot that has basic utilities and multiple API integration

This is a Discord bot that I've made on my own free time, it is a passion project for me and I plan to add
much more functionality to it in the future. Right now the bot is private as I can't currently host it 24/7 but
I plan to. 



## Changelog

-**Version 0.1.0** <sub><sup>1/17/19</sup></sub>
* Release! Discord bot has reddit api functionality and basic features. Working on league of legends data extraction
* Bot is still unavailable for public, but code is now

-**Version 0.1.1** <sub><sup>1/20/19</sup></sub> 
* Added `!lolmatch` command to retrieve basic info on a summoner's most recent match
* Added and changed some of the `!8ball` outputs to better match yes/no questions
* Updated `!helplist`
* Fixed up `summonerinfo.py` to be more modularized and removed test cases
* Added more comments throughout the code

-**Version 0.1.2** <sub><sup>1/31/19</sup></sub>
* Fixed `!lolmatch`, was throwing wrong exceptions
* Formatted `!lolmatch` output for readability
* Fixed some minor redundant code in `summonerinfo.py`
* Bot is now optimized for doing less requests to the Riot Api by using caches
* Added cache folders and files to save some dynamic info and a lot of static info, being powered by JSON
* Added `!lolavg` command to retrieve averages and comment on your most recent matches on Summoner's Rift
* Updated functions to reflect optimized cache usage
* Caches automatically refresh after certain periods
* Updated `!helplist`
* Added and updated comments throughout code




