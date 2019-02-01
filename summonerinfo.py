from riotwatcher import RiotWatcher
from datetime import datetime, timedelta
import json
import pprint

with open('C:\\Users\\Marcello\\Documents\\Tokens.json') as t:  # to keep Riot api key secret

    tokenDict = json.load(t)

with open('basic_data.json') as b:
    dataDict = json.load(b)
    compareDate = dataDict['cacheDate']
    compareDateTwo = dataDict['cacheMatch']




lol = RiotWatcher(tokenDict['league'], v4=True)

region = 'na1'      # Will only search for NA accounts for now to keep it simple

# gameVersion = lol.data_dragon.versions_for_region(region)['n']['champion']

gameVersion = '9.2.1'

today = datetime.now()      # get todays date and time

compareDate = compareDate[:10]  # slice so we only get the year month date

compareDate = datetime.strptime(compareDate, '%Y-%m-%d')    # convert cached value to datetime for timedelta evaluation

compareDateTwo = compareDateTwo[:19]

compareDateTwo = datetime.strptime(compareDateTwo, '%Y-%m-%d %H:%M:%S')


print(compareDate)

    # Compare cached static data
if today >= compareDate + timedelta(days=13): # if 13 days have passed since cached date, then update json cache
    print('today is now more than cached date')
    with open('cached_data\\st_champion_data.json', 'w') as champCache: # cache champion data
        data = lol.data_dragon.champions(gameVersion, full=True)['data']
        json.dump(data, champCache, indent=4)
    with open('cached_data\\st_item_data.json', 'w') as itemCache:      # cache item data
        data = lol.data_dragon.items(gameVersion)
        json.dump(data, itemCache, indent=4)
    with open('cached_data\\map_data.json', 'w') as mapCache:    #cache map data
        data = lol.data_dragon.maps(gameVersion)
        json.dump(data, mapCache, indent=4)
    with open('basic_data.json', 'r+') as b:
        data = json.load(b)
        data['cacheDate'] = str(today)
        b.seek(0)
        json.dump(data, b, indent=4)
        b.truncate()
   # print('cached date now updated')

else:
   # print('compareDate has not passed yet, cache will not update')
    pass
    # Compare stored matchlist data

if today >= compareDateTwo + timedelta(minutes=35):
    with open('cached_data\\matchlist_data.json', 'r+') as matchlistData: #Clear matchlist cache after 35 minutes
        data = json.load(matchlistData)
        data.clear()
        matchlistData.seek(0)
        json.dump(data, matchlistData, indent=4)
        matchlistData.truncate()

    with open('basic_data.json', 'r+') as b:        # Update compare date for matchlist
        data = json.load(b)
        data['cacheMatch'] = str(today)
        b.seek(0)
        json.dump(data, b, indent=4)
        b.truncate()
        print('matchlist cleared!')


champDict = {}
itemDict = {}
mapDict = {}

with open('cached_data\\st_item_data.json') as b:
    itemDict = json.load(b)

with open('cached_data\\st_champion_data.json') as b:
    champDict = json.load(b)

with open('cached_data\\map_data.json') as b:
    mapDict = json.load(b)


# python file I made to help me test out the riot api retrieval for use in bot once I know it works
# Might make it into class?

def getSummonerId(summonerName):

    with open('cached_data\\summoner_id_data.json', 'r+') as c:
        data = json.load(c)
        if summonerName in data:
            return data[summonerName]
        else:
            data[summonerName] = lol.summoner.by_name('na1', summonerName)['accountId']
            c.seek(0)
            json.dump(data, c, indent=4)
            c.truncate()
            return data[summonerName]



def getMatchlist(summonerName):
    try:
        with open('cached_data\\matchlist_data.json', 'r+') as d:
            dataM = json.load(d)
            for item in dataM:
                for key in item:
                    if key == summonerName:
                        return item[key]
                       # print('written data loaded!')
            else:
                summonerId = getSummonerId(summonerName)
                mDict = {summonerName: lol.match.matchlist_by_account('na1', summonerId, end_index=50)['matches']}
                dataM.append(mDict)
                d.seek(0)
                json.dump(dataM, d, indent=4)
                d.truncate()

                for item in dataM:
                    for key in item:
                        if key == summonerName:
                            return item[key]
                       # print('data written!')
    except Exception:          # I'm lazy but its checking for a 404 name not found
        return 404



def kdaCalc(k, d, a):

    if d > 0:
        return round((k + a * 0.5)/d, 2)
    else:
        return round((k + a * 0.5) / (d + 1), 2)


def getChampName(id):

    champData = champDict

    for champ in champData:

        if champData[champ]['key'] == id:
            return champData[champ]['name']



def getItemName(id):

    if id != '0':
        return itemDict['data'][id]['name']
    else:
        return


def getItemNames(list):

    itemList = []

    for id in list:

        if id != 0:

            itemList.append(getItemName(id))


    return itemList

def getMatchPartDict(matchId):

    """Returns a dictionary containing the summoner names of all participants in a match with their participant Id"""



    summonerDict = {}

    i = 0
    match = lol.match.by_id(region, matchId)

    for keys in match['participantIdentities']:  # Use this to find corresponding participantId and summonerName
        accountName = match['participantIdentities'][i]['player']['summonerName']
        partId = match['participantIdentities'][i]['participantId']
        accountName = accountName.upper()   # This is to filter out case sensitivity

        summonerDict[accountName] = partId
        i += 1


    return summonerDict


def getPlayerMatch(summonerName, index=0, pFormat=False):

    # index of 0 is the most recent match going up to 100

    if index > 100 or index < 0:
        return


    matchList = getMatchlist(summonerName)

    if matchList == 404:
        return 404

    matchId = matchList[index]['gameId']

    summonernameC = summonerName.upper()

    match = lol.match.by_id('na1', matchId)

    summonerDict = getMatchPartDict(matchId)

    idVal = summonerDict[summonernameC] - 1

    pStats = match['participants'][idVal]['stats']

    pChampId = str(match['participants'][idVal]['championId'])

    pChampName = getChampName(pChampId)

    pKills = pStats['kills']

    pAssists = pStats['assists']

    pDeaths = pStats['deaths']

    pKDA = kdaCalc(pKills, pDeaths, pAssists)

    pTotalGold = pStats['goldEarned']

    mapId = str(match['mapId'])

    mapName = mapDict['data'][mapId]['MapName']

    pItemList = []

    for i in range(0, 7):

        itemId = pStats['item{}'.format(i)]

        itemId = str(itemId)

        if getItemName(itemId) is not None:

            pItemList.append(getItemName(itemId))

    # 10 is Twisted Treeline
    # 11 is Summoners rift
    # 12 is howling abyss
    # 21 is Nexus Blitz

    if match['mapId'] == 11:
        pWards = pStats['wardsPlaced']
        pCreeps = pStats['totalMinionsKilled'] + pStats['neutralMinionsKilledEnemyJungle'] + pStats['neutralMinionsKilled'] + pStats['neutralMinionsKilledTeamJungle']
    elif match['mapId'] == 10:
        pCreeps = pStats['totalMinionsKilled'] + pStats['neutralMinionsKilledEnemyJungle'] + pStats['neutralMinionsKilled'] + pStats['neutralMinionsKilledTeamJungle']
        pWards = 0
    elif match['mapId'] == 12:
        pWards = 0
        pCreeps = pStats['totalMinionsKilled']
    elif match['mapId'] == 21:
        pWards = pStats['wardsPlaced']
        pCreeps = pStats['totalMinionsKilled'] + pStats['neutralMinionsKilledEnemyJungle'] + pStats['neutralMinionsKilled'] + pStats['neutralMinionsKilledTeamJungle']



    pWin = pStats['win']

    pTotalDamage = pStats['totalDamageDealtToChampions']

    pDamageTaken = pStats['totalDamageTaken']

    pMulti = pStats['largestMultiKill']

    playerDict = {'Name': summonerName, 'Champ': pChampName, 'Items': pItemList,
                  'Gold': pTotalGold, 'CS': pCreeps, 'Kills': pKills, 'Deaths': pDeaths,
                  'Assists': pAssists, 'KDA': pKDA, 'Damage Taken': pDamageTaken,
                  'Damage Dealt': pTotalDamage, 'Wards Placed': pWards, 'Win': pWin, 'Multi': pMulti, 'Map': mapName}

    if pFormat:
        pp = pprint.PrettyPrinter(indent=3)
        playerDict = pp.pformat(playerDict)

    return playerDict

def transcribeDict(d):

    pString = "Summoner **{}** went as {} \nhad a score of **{}/{}/{}**" \
              " **KDA:** {}  **CS:** {} \n**Total Gold:** {} **Damage Dealt:** {} " \
              "**Damage Taken:** {} \n**Wards Placed:** {} \n**Map:** {} **Game won?**: {}"\
            .format(d['Name'], d['Champ'], d['Kills'], d['Deaths'], d['Assists'], d['KDA'], d['CS'], d['Gold'], d['Damage Dealt'], d['Damage Taken'], d['Wards Placed'], d['Map'], d['Win'])

    return pString



def getStatlist(matchlist, name):

    nameC = name.upper()
    matchStats = []
    for match in matchlist:
        summDict = getMatchPartDict(match['gameId'])        # get the actual player stats from each of those matches in a list
        idVal = summDict[nameC] - 1
        pStats = match['participants'][idVal]['stats']
        matchStats.append(pStats)

    return matchStats



def getAvgStat(statlist, stat, mapId=11):

    newList = []
    if stat == 'wardsPlaced' and mapId == 12:   # checking for ARAM
        return 0

    if stat == 'wardsPlaced' and mapId == 10:    # checking for TT
        return 0

    if stat == 'neutralMinionsKilled' and mapId == 12:
        return 0

    try:
        if stat == 'kda':
            for stats in statlist:
                newList.append(kdaCalc(stats['kills'], stats['deaths'], stats['assists']))
        else:
            for stats in statlist:
                newList.append(stats[stat])

    except KeyError:   # return -1 if we get an incorrect key in the function
        return -1



    return sum(newList)/len(newList)


def getAverageChampion(matches, name):

    """Returns a tuple of the most common champion and how much you have played it in the sample size"""

    # Alphabetical order takes priority if two champions are played the same amount and played more than once

    nameC = name.upper()
    champNames = []
    for match in matches:
        summDict = getMatchPartDict(match['gameId'])
        idVal = summDict[nameC] - 1
        champId = str(match['participants'][idVal]['championId'])
        champNames.append(getChampName(champId))
    max = 0
    mName = ''
    champNames.reverse()
    for name in champNames:
        if champNames.count(name) >= max:
            max = champNames.count(name)
            mName = name
    if max == 1:    # if all champs are different
        return 0
    elif max >= 2:
        return mName, max       # returns a tuple





def analyzeMatchlist(name, mapId=11, recent=5):   # Recent will analyze last 5 games played by default, if not then last x games played

    matchlist = getMatchlist(name)
    if matchlist == 404:            # check for valid matchlist and valid map Ids
        return 404
    if mapId != 11 and mapId != 12 and mapId != 10:   # Rest in peace Nexus Blitz
        return 404

    if recent > 25:     # make sure max analyzable matches is 25
        recent = 25

    matches = []
    i = 0
    j = 0

    while i < 25 and j < recent:      # Analyzes a quarter of all matches to search for correct map
        matchId = matchlist[i]['gameId']
        match = lol.match.by_id('na1', matchId)
        if match['mapId'] == mapId:
            matches.append(match)
            j += 1
        i += 1


    matchStats = getStatlist(matches, name)

    avgDeaths = getAvgStat(matchStats, 'deaths')

    avgKills = getAvgStat(matchStats, 'kills')

    avgAssists = getAvgStat(matchStats, 'assists')

    avgKDA = round(getAvgStat(matchStats, 'kda'), 2)

    avgChamp = getAverageChampion(matches, name)

    if avgChamp == 0:
        champString = "has been playing different champions lately"
    elif avgChamp[1] == 2:
        champString = f"has been playing a bit of {avgChamp[0]} lately"
    elif avgChamp[1] >= 6:
        champString = f"has been playing too much {avgChamp[0]}!"
    else:
        champString = f"has been practicing their {avgChamp[0]} lately"

    if avgKills >= 10:
        extraString = f" has been on a complete rampage with an average of {avgKills} kills!"
    elif avgAssists >= 18:
        extraString = f" has been a team players with over {avgAssists} assists!"
    elif avgDeaths <= 4:
        extraString = f" has been immortal the past few games with an average of {avgDeaths} deaths!"
    elif avgDeaths >= 8 and avgKills <= 8:
        extraString = f" has been feeding too much lately! Oops!"
    else:
        extraString = f" has been cruising through games."


    if avgKDA <= 0.32:
        kdaString = f"You gotta work on your KDA.. its only {avgKDA}.."
    elif avgKDA >= 3.3:
        kdaString = f"Your KDA these past games is phenomenal! It's at {avgKDA}!"
    elif avgKDA >= 1.9:
        kdaString = f"You have a solid KDA, keep it up! It's at {avgKDA}"

    else:
        kdaString = f"Your KDA could be better. It's at {avgKDA}"

    return f"{name} {champString} and{extraString} {kdaString}"


# print(analyzeMatchlist('stacheross', recent=10))

 # print(transcribeDict(getPlayerMatch('Umbreon 62'))) # line to test script with my summonner name






