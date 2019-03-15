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

-**Version 0.2.0** <sub><sup>2/21/19</sup></sub>
* Fixed some issues of `!randomfact` when it came to outputting facts
* Updated and reformatted `!helplist' adding potentially more menus (They still don't look pretty)
* Added new commands such as `!grayscale`, `!sharpen`, `!enhance` and `!mememaker`
* Bot now has the power to process images and output them through commands!
* Added a folder to store meme templates, shaders, font and other image related goodness
* Created `imageinfo.py` to help store image related functions
* Adjusted some code in `main.py` and `summonerinfo.py` for better readability
* Added even more comments!
* Uses a `tempimg.png` file to store outputted images

-**Version 0.2.1** <sub><sup>3/15/19</sup></sub>
* Added all the cache stuff into a function
* Added and fixed more comments slightly
* Fixed issue of the `!r34s` giving back invalid links, will now only give links from reddit, imgur and gfycat
* More potential content for `!r34s`
* `!redcomment` now also gives post name as further comment context




