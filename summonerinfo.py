from riotwatcher import RiotWatcher

import json
import pprint

with open('C:\\Users\\Marcello\\Documents\\Tokens.json') as t:

    tokenDict = json.load(t)

lol = RiotWatcher(tokenDict['league'], v4=True)

region = 'na1'

gameVersion = lol.data_dragon.versions_for_region(region)['n']['champion']



# python file I made to help me test out the riot api retrieval for use in bot once I know it works
# Might make it into class?

def getSummonerId(summonerName):

    return lol.summoner.by_name('na1', summonerName)['accountId']


def getMatchlist(summonerName):

    summonerId = getSummonerId(summonerName)

    matchlist = lol.match.matchlist_by_account('na1', summonerId)['matches']

    return matchlist


def kdaCalc(k, d, a):

    if d > 0:
        return round((float(k + a * 0.5)/d), 2)
    else:
        return round((float(k + a * 0.5) / (d + 1)), 2)


def getChampName(id):

    champData = lol.data_dragon.champions(gameVersion, full=True)['data']

    for champ in champData:

        if champData[champ]['key'] == id:
            return champData[champ]['name']



def getItemName(id):

    if id != '0':
        return lol.data_dragon.items(gameVersion)['data'][id]['name']
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

    index = int(index)
    try:
        matchId = getMatchlist(summonerName)[index]['gameId']
    except Exception:       # I'm lazy but its checking for a 404 name not found
        return 404

    summonernameC = summonerName.upper()

    print(matchId)

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

    mapName = lol.data_dragon.maps(gameVersion)['data'][mapId]['MapName']

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

    pString = "Summoner {} went as {} \nhad a score of {}/{}/{}" \
              " KDA: {}  CS: {} \nTotal Gold: {} Damage Dealt: {} " \
              "Damage Taken: {} \nWards Placed: {} Map: {} Win: {}"\
            .format(d['Name'], d['Champ'], d['Kills'], d['Deaths'], d['Assists'], d['KDA'], d['CS'], d['Gold'], d['Damage Dealt'], d['Damage Taken'], d['Wards Placed'], d['Map'], d['Win'])

    return pString





 # print(transcribeDict(getPlayerMatch('Umbreon 62'))) # line to test script with my summonner name

















































