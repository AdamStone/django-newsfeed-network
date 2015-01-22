import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kero.settings")

from network.models import User, Node
import time
import random
import feedparser

rss = {
'general':[
    'http://www.reddit.com/.rss',
    'http://digg.com/rss/top.rss',
    'http://feeds.mashable.com/Mashable',
    'http://blog.flickr.net/en/feed/atom/',
    'http://www.gawker.com/index.xml',
    'http://feeds.gawker.com/gizmodo/full',
    'http://feeds.feedburner.com/upworthy',
    'http://feeds.feedburner.com/CrackedRSS',
],
'news-US':[
    'http://rss.newser.com/rss/section/3.rss',
    'http://feeds.huffingtonpost.com/huffingtonpost/LatestNews',
    
],
'news-world':[
    'http://rss.newser.com/rss/section/2.rss',
    'http://www.huffingtonpost.com/feeds/verticals/world/index.xml',
    'http://www.foreignpolicy.com/node/feed',
    'http://online.wsj.com/xml/rss/3_7085.xml',

],
'politics-left':[
    'http://www.huffingtonpost.com/feeds/verticals/politics/index.xml',
    'http://feeds.dailykos.com/dailykos/index.xml',
    'http://krugman.blogs.nytimes.com/feed',
    'http://salon.com.feedsportal.com/c/35105/f/648624/index.rss',
],
'politics-right':[
    'http://www.redstate.com/feed/',
    'http://drudgereportfeed.com/rss.xml',

],
'politics-general':[
    'http://rss.newser.com/rss/section/4.rss',
    'http://www.mediaite.com/feed/',
    'http://online.wsj.com/xml/rss/3_7041.xml',
],
'business':[
    'http://online.wsj.com/xml/rss/3_7014.xml',
    'http://feeds.feedburner.com/TechCrunch/',
    'http://rss.newser.com/rss/section/5.rss',
    'http://www.huffingtonpost.com/feeds/verticals/business/index.xml',
    'http://www.huffingtonpost.com/feeds/verticals/money/index.xml',
    'http://feeds.feedburner.com/entrepreneur/latest',
],
'science':[
    'http://feeds.nationalgeographic.com/ng/NGM/NGM_Magazine',
    'http://feeds.nationalgeographic.com/ng/News/News_Main',
    'http://rss.newser.com/rss/section/6.rss',
    'http://www.huffingtonpost.com/feeds/verticals/science/index.xml',
    'http://rss.sciam.com/ScientificAmerican-Global',
],
'tech':[
    'http://feeds.feedburner.com/TechCrunch/',
    'http://www.engadget.com/rss.xml',
    'http://feeds.wired.com/wired/index',
    'http://rss.newser.com/rss/section/7.rss',
    'http://www.huffingtonpost.com/feeds/verticals/technology/index.xml',
    'http://feeds.arstechnica.com/arstechnica/index',
],
'gaming':[
    'http://www.joystiq.com/rss.xml',
],
'entertainment':[
    'http://rss.newser.com/rss/section/15.rss',
    'http://www.huffingtonpost.com/feeds/verticals/media/index.xml',
    'http://www.huffingtonpost.com/feeds/verticals/entertainment/index.xml',
],
'celebrity':[
    'http://www.tmz.com/rss.xml',
    'http://rss.newser.com/rss/section/12.rss',
    'http://www.huffingtonpost.com/feeds/verticals/celebrity/index.xml',
],
'travel':[
    'http://rss.newser.com/rss/section/22.rss',
    'http://www.huffingtonpost.com/feeds/verticals/travel/index.xml',
],
'crime':[
    'http://rss.newser.com/rss/section/13.rss',
    'http://www.huffingtonpost.com/feeds/verticals/crime/news.xml',
],
'sports':[
    'http://rss.newser.com/rss/section/8.rss',
    'http://www.huffingtonpost.com/feeds/verticals/sports/index.xml',
],
'health':[
    'http://rss.newser.com/rss/section/17.rss',
    'http://www.huffingtonpost.com/feeds/verticals/healthy-living/index.xml',
],
'religion':[
    'http://www.huffingtonpost.com/feeds/verticals/religion/index.xml',
],
'photos':[
    'http://feeds.nationalgeographic.com/ng/photography/photo-of-the-day/',
],
}

personalities = {
    'liberal':['news-US','politics-left', 'politics-general'],
    'conservative':['news-US','politics-right','business'],
    'techie':['tech', 'gaming'],
    'traveler':['news-world', 'travel'],
    'scientist':['science','photos'],
    'gossipgirl':['entertainment','celebrity','crime'],
    'sportsfan':['sports', 'entertainment'],
    'yogi':['religion','health']
}

def get_from_rss(n=1, categories = []):
    links = []
    while len(links) < n:
        if not categories:
            category = random.choice(rss.keys())
        else:
            category = random.choice(categories)
        feed_url = random.choice(rss[category])
        feed = feedparser.parse(feed_url)
        try:
            choice = random.choice(feed['entries'])
            link = choice['link']
            if link:
                links.append(link)
        except Exception:
            pass
    return links
    
    
class Sharebot:
    def __init__(self, node=None, username='', email='', password='', personality='', interests=[], population=None):
        if node:
            self.user = node.user
            self.node = node
            self.personality = self.user.email[:-12]
            self.interests = personalities[self.personality]
        else:
            self.user = User.objects.create_user(username, email, password)
            self.node = self.user.node            
            self.personality = personality
            self.interests = interests
            self.population = population
    
class Population:
    def __init__(self, sharebots=[]):
        if sharebots:
            self.bots = sharebots
            for bot in self.bots:
                bot.population = self
    
    def populate(self, bots=498):
        for i in range(bots):
            if not i% 10: print i
            personality, interests = random.choice(personalities.items())
            bot = Sharebot(username='bot'+str(i), 
                           email=str(personality)+'@example.com', 
                           password='password', 
                           personality=personality, 
                           interests=interests, 
                           population=self)
            self.bots.append(bot)
            
    def shuffle(self, connections=100):
        for node in Node.objects.all():
            node.shuffle(verbose=True, connections=connections)
            
    def run(self):
        active = random.sample(self.bots, 100)
        while True:
            bot = random.choice(active)
            web_sample = get_from_rss(1, bot.interests)
            for url in web_sample:
                bot.node.share(url)
                print str(bot.user.username) + ' shared: \n' + url + '\n\n'
                
            # change active
            roll = random.choice(range(10))
            if roll == 1:
                active.pop()
            elif roll == 9:
                choice = random.choice(self.bots)
                if choice not in active:
                    active.append(choice)
            sleep = random.choice(range(20))
            print 'sleep time: ', sleep
            time.sleep(sleep)
            

nodes = Node.objects.exclude(user__username='stone')
bots = []

if nodes:
    for node in nodes:
        s = Sharebot(node)
        bots.append(s)

P = Population(bots)
P.run()
