import imageinfo as ii
import discord
import random
import praw
import json
import summonerinfo as summ
from PIL import Image
import requests
from bs4 import BeautifulSoup as bs

with open('factlist.json') as f:
    factlist = json.load(f)

with open('helpmenu.json') as g:
    helpmenu = json.load(g)

with open('C:\\Users\\Marcello\\Documents\\Tokens.json') as h:  # this is used to keep all my api keys private
    tokenDict = json.load(h)


with open('eightball.json') as j:
    eightball = json.load(j)




reddit = praw.Reddit(client_id=tokenDict['redditid'],
                     client_secret=tokenDict['reddit'],
                     user_agent='Marcelinator')

client = discord.Client()


filterList = [] # Not in use yet

def uwuify(words):      # don't ask why I made this

    endinglist = ('OwO', 'XD', 'Rawr XD', ':3', 'UwU', "0w0")
    wordslist = ''
    words = words.upper()


    for letter in words:
        if letter == 'L' or letter == 'R':
            wordslist = wordslist + 'W'
        else:
            wordslist = wordslist + letter

    if 'YOU' in wordslist:
        wordslist = wordslist.replace("YOU", 'u')
    if 'FUCK' in wordslist:
        wordslist = wordslist.replace('FUCK', 'fudge')
    if 'SHIT' in wordslist:
        wordslist = wordslist.replace('SHIT', 'poop')

    wordslist = wordslist.lower()
    wordslist = wordslist + ' {}'.format(random.choice(endinglist))

    return wordslist


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!randomfact'):
        msg = random.choice(factlist)
        await client.send_message(message.channel, msg)

    if message.content.startswith('oof'):
        msg = 'Ouch my bones'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!doot'):
        msg = '<:doot:495351513267568650> <:doot:495351513267568650>'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!uwuify'):
        word = message.content[7:]                      #slice after the uwu, which is the value we want
        msg = uwuify(word)
        await client.send_message(message.channel, msg)

    if message.content.startswith('You ready?'):        # These lines of code are to give me moral support whilst testing my bot
        if message.author.name == 'Marcel':
            msg = 'Yes creator, I am ready'
        else:
            msg = "You're not my creator?"
        await client.send_message(message.channel, msg)

    if message.content.startswith("You've failed me"):
        if message.author.name == 'Marcel':
            msg = 'Sorry :('
        await client.send_message(message.channel, msg)

    if message.content.startswith("Good job!"):
        if message.author.name == 'Marcel':
            msg = 'Thank you :D'
        await client.send_message(message.channel, msg)

    if any(word in message.content for word in filterList):     # Not actually used but functionality is there
        await client.delete_message(message)

    if message.content.startswith('!dank'):
        dankmemes = reddit.subreddit('dankmemes').hot()
        postid = random.randint(0, 31)
        for i in range(0, postid):
            submission = next(x for x in dankmemes if not x.stickied)

        await client.send_message(message.channel, submission.url)

    if message.content.startswith('!hentai'):
        hentai = reddit.subreddit('hentai').hot()
        postid = random.randint(0, 31)
        for i in range(0, postid):
            submission = next(x for x in hentai if not x.stickied)

        await client.send_message(message.channel, submission.url)

    if message.content.startswith('!help'):
        menuNumb = 0
        if len(message.content) > 5:
            menuNumb = message.content[6:]
        if menuNumb == '2':
            msg = 'More of my commands \n' + '```diff\n'
            for helpcommands in helpmenu["2"]:
                msg = msg + helpcommands + '\n'
            msg = msg + '```'
        else:
            msg = 'Here are all my available commands \n' + '```diff\n'
            for helpcommands in helpmenu["1"]:
                msg = msg + helpcommands + '\n'
            msg = msg + '```'
        await client.send_message(message.channel, msg)

    if message.content.startswith('!redcomment'):
        try:
            redditorname = message.content[12:]
            redditor1 = reddit.redditor(redditorname)
            commentlist = list(redditor1.comments.hot())
            comment1 = random.choice(commentlist)
            msg = '```' + comment1.body + '```' + '~ {} in /r/{}'.format(redditorname, comment1.subreddit.display_name)
            await client.send_message(message.channel, msg)
        except Exception:
            msg = 'Sorry your user "{}", was not found'.format(redditorname)
            await client.send_message(message.channel, msg)

    if message.content.startswith('!r34s'):     # the functionality every discord bot should have, please hire me regardless of this
        keyword = message.content[6:]
        query = 'title:{} self:no site:i.redd.it OR site:i.imgur.com OR site:imgur.com OR site:gfycat.com'.format(keyword)
# Search params arent really working for now, but I will keep them incase
        r34list = []
        r34 = reddit.subreddit('rule34')
        try:
            for submission in r34.search(query, params={'include_over_18': 'on'}, limit=25):
                r34list.append(submission.url)
            r34post = (random.choice(r34list))
            await client.send_message(message.channel, r34post)

        except Exception:
            await client.send_message(message.channel, 'No images were found!')

    if message.content.startswith('!8ball'):
        msg = random.choice(eightball)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!randnumb'):
        numList = message.content.split()
        if len(numList) is 1:
            msg = random.randint(0, 101)
        elif len(numList) is 2:
            msg = random.randint(0, int(numList[1]) + 1)
        elif len(numList) >= 3:
            msg = random.randint(int(numList[1]), int(numList[2]) + 1)

        await client.send_message(message.channel, str(msg))

    if message.content.startswith('!lolmatch'):
        summonerName = message.content[10:]
        try:
            msg = summ.getPlayerMatch(summonerName)
            if msg == 404:
                await client.send_message(message.channel, 'Summoner name does not exist in NA')
            else:
                msg = summ.transcribeDict(msg)
                await client.send_message(message.channel, msg)
        except Exception:  # Very lazy will fix later
            await client.send_message(message.channel, 'Sorry try again in a few minutes!')

    if message.content.startswith('!lolavg'):
        summonerName = message.content[8:]
        try:
            msg = summ.analyzeMatchlist(summonerName)
            if msg == 404:
                await client.send_message(message.channel, 'Summoner name does not exist in NA')
            else:
                await client.send_message(message.channel, msg)
        except Exception:
            await client.send_message(message.channel, 'Sorry try again in a few minutes!')

    if message.content.startswith('!enhance'):
        contrast = 2.0
        if len(message.content) > 8:
            contrast = float(message.content[9:])
        if contrast > 1000:
            contrast = 1000
        try:
            picurl = message.attachments[0]['url']

        except IndexError:
            await client.send_message(message.channel, "File not attached or incorrect file! Try again")

        img = ii.getImage(picurl)
        img = ii.enhanceImage(img, contrast=contrast)
        img.save('tempimg.png')
        await client.send_file(message.channel, "tempimg.png", content="Done!", filename="result.png")

    if message.content.startswith('!grayscale'):
        picurl = message.attachments[0]['url']
        img = ii.getImage(picurl).convert(mode='RGB')
        pall = Image.open('templates\\grayscale.png').convert(mode='P')
        img = ii.quantizetopalette(img, pall)
        img.save('tempimg.png')
        await client.send_file(message.channel, "tempimg.png", content="Done!", filename="result.png")

    if message.content.startswith('!sharpen'):
        sharp = 2.0
        if len(message.content) > 8:
            sharp = float(message.content[9:])
        if sharp > 1000:
            sharp = 1000
        try:
            picurl = message.attachments[0]['url']

        except IndexError:
            await client.send_message(message.channel, "File not attached or incorrect file! Try again")

        img = ii.getImage(picurl)
        img = ii.sharpenImage(img, sharp=sharp)
        img.save('tempimg.png')
        await client.send_file(message.channel, "tempimg.png", content="Done!", filename="result.png")

    if message.content.startswith('!mememaker'): # This is a fun one
        tmpltWords = message.content[11:]
        picTok = tmpltWords[:3]
        print(picTok)
        tmpltWords = tmpltWords[3:]
        tmpltWords = tmpltWords.split(':')
        if picTok == 'tj ':
            if len(tmpltWords[0]) > 50 or len(tmpltWords[1]) > 50:
                await client.send_message(message.channel, "Sorry your inputs are too long!")
            elif len(tmpltWords) != 2:
                await client.send_message(message.channel, "Sorry wrong amount of inputs!")
            else:
                btText = ii.textSplitter(tmpltWords[0])
                upText = ii.textSplitter(tmpltWords[1])
                img = Image.open('templates\\tomjerry.jpg')
                img = ii.addTj(img, btText, upText)
                img.save('tempimg.png')
                await client.send_file(message.channel, "tempimg.png", content="Done!", filename="result.png")
        elif picTok == 'eb ':
            if len(tmpltWords[0]) > 50 or len(tmpltWords[1]) > 50 or len(tmpltWords[2]) > 50 or len(tmpltWords[3]) > 50:
                await client.send_message(message.channel, "Sorry your inputs are too long!")
            elif len(tmpltWords) != 4:
                await client.send_message(message.channel, "Sorry wrong amount of inputs!")
            else:
                oneText = ii.textSplitter(tmpltWords[0], maxline=2)
                twoText = ii.textSplitter(tmpltWords[1], maxline=2)
                threeText = ii.textSplitter(tmpltWords[2], maxline=2)
                fourText = ii.textSplitter(tmpltWords[3], maxline=2)
                img = Image.open('templates\\expbrain.png')
                img = ii.addEb(img, oneText, twoText, threeText, fourText)
                img.save('tempimg.png')
                await client.send_file(message.channel, "tempimg.png", content="Done!", filename="result.png")
        else:
            await client.send_message(message.channel, "Sorry, wrong template name!")




    # if message.content.startswith('!wiki'):      Upcoming feature in the works
    #     pageName = message.content[6:]
    #     if ' ' in pageName:
    #         pageName = pageName.replace(' ', '_')
    #     try:
    #         pageName = 'https://en.wikipedia.org/wiki/' + pageName
    #     except Exception:
    #         await client.send_message(message.channel, 'Wiki page not found!')
    #     pageText = requests.get(pageName).text
    #     soup = bs(pageText, 'html.parser')
    #     pageText = soup.get_text()
    #     pageText = pageText.split('.')
    #     print(pageText)
    #     pageSummary = []
    #     for i in range(0, 8):
    #         pageSummary.append(pageText[i] + '. ')
    #     pageSummary = str(pageSummary)
    #     await client.send_message(message.channel, pageSummary)












@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')




client.run(tokenDict['discord'])