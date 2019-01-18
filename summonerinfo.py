from riotwatcher import RiotWatcher

import json
import pprint

with open('C:\\Users\\Marcello\\Documents\\Tokens.json') as t:

    tokenDict = json.load(t)

lol = RiotWatcher(tokenDict['league'], v4=True)

region = 'na1'

gameVersion = '9.1.1'



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

        else:

            pass

    return itemList

def getMatchPartDict(matchId):

    """Returns a dictionary containing the summoner names of all participants in a match with their participant Id"""

    summonerDict = {}

    match = lol.match.by_id(region, matchId)

    for i in range(0, 10):  # Use this to find corresponding participantId and summonerName
        accountName = match['participantIdentities'][i]['player']['summonerName']
        partId = match['participantIdentities'][i]['participantId']

        summonerDict[accountName] = partId

    return summonerDict


def getPlayerMatch(summonerName, index=0):

    # index of 0 is the most recent match going up to 100

    if index > 100 or index < 0:
        return

    index = int(index)

    matchId = getMatchlist(summonerName)[index]['gameId']

    print(matchId)

    match = lol.match.by_id('na1', matchId)

    summonerDict = getMatchPartDict(matchId)

    idVal = summonerDict[summonerName] - 1

    pStats = match['participants'][idVal]['stats']

    pChampId = str(match['participants'][idVal]['championId'])

    pChampName = getChampName(pChampId)

    pKills = pStats['kills']

    pAssists = pStats['assists']

    pDeaths = pStats['deaths']

    pKDA = kdaCalc(pKills, pDeaths, pAssists)

    pTotalGold = pStats['goldEarned']

    pItemList = []

    for i in range(0, 7):

        itemId = pStats['item{}'.format(i)]

        itemId = str(itemId)

        if getItemName(itemId) is not None:

            pItemList.append(getItemName(itemId))

    if match['gameMode'] != 'ARAM':
        pWards = pStats['wardsPlaced']
        pCreeps = pStats['totalMinionsKilled'] + pStats['neutralMinionsKilledEnemyJungle'] + pStats['neutralMinionsKilled'] + pStats['neutralMinionsKilledTeamJungle']
    else:
        pCreeps = pStats['totalMinionsKilled']
        pWards = 0


    pWin = pStats['win']

    pTotalDamage = pStats['totalDamageDealtToChampions']

    pDamageTaken = pStats['totalDamageTaken']

    pMulti = pStats['largestMultiKill']

    playerDict = {'Name': summonerName, 'Champ': pChampName, 'Items': pItemList,
                  'Gold': pTotalGold, 'CS': pCreeps, 'Kills': pKills, 'Deaths': pDeaths,
                  'Assists': pAssists, 'KDA': pKDA, 'Damage Taken': pDamageTaken,
                  'Damage Dealt': pTotalDamage, 'Wards Placed': pWards, 'Win': pWin, 'Multi': pMulti}

    pp = pprint.PrettyPrinter(indent=3)
    playerDict = pp.pformat(playerDict)

    return playerDict

def transcribeDict(d):

    pString = f"Summoner {d['Name']} went as {d['Champ']} went {d['Kills']}/{d['Deaths']}/{d['Assists']} KDA: {d['KDA']}  CS: {d['CS']} \n" \
              f" Total Gold: {d['Gold']} Damage Dealt: {d['Damage Dealt']} Damage Taken: {d['Damage Taken']} Wards Placed {d['Wards Placed']}"

    return pString







print(getPlayerMatch('Umbreon 62'))

















































