import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kero.settings")

from network.models import Content, Node, Connection, Share
from django.contrib.auth.models import User
from urlparse import urlparse, urlunparse
import random
import requests
from bs4 import BeautifulSoup
import feedparser

""" multi-feeds:
http://feeds.gawker.com/gizmodo/full
http://www.wired.com/about/rss_feeds/
http://arstechnica.com/rss-feeds/
http://techcrunch.com/rssfeeds/
http://www.huffingtonpost.com/syndication/

"""

rss = {
'general':[
    'http://www.reddit.com/.rss',
    'http://digg.com/rss/top.rss',
    'http://feeds.mashable.com/Mashable',
    'http://blog.flickr.net/en/feed/atom/',
    'http://www.gawker.com/index.xml',
    'http://feeds.gawker.com/gizmodo/full',
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
#~ 'celebrity':[
    #~ 'http://www.tmz.com/rss.xml',
    #~ 'http://rss.newser.com/rss/section/12.rss',
    #~ 'http://www.huffingtonpost.com/feeds/verticals/celebrity/index.xml',
#~ ],
'travel':[
    'http://rss.newser.com/rss/section/22.rss',
    'http://www.huffingtonpost.com/feeds/verticals/travel/index.xml',
],
'crime':[
    'http://rss.newser.com/rss/section/13.rss',
    'http://www.huffingtonpost.com/feeds/verticals/crime/news.xml',
],
#~ 'sports':[
    #~ 'http://rss.newser.com/rss/section/8.rss',
    #~ 'http://www.huffingtonpost.com/feeds/verticals/sports/index.xml',
#~ ],
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

def get_from_rss(n=1):
    links = []
    while len(links) < n:
        category = random.choice(rss.keys())
        feed_url = random.choice(rss[category])
        feed = feedparser.parse(feed_url)
        choice = random.choice(feed['entries'])
        link = choice['link']
        links.append(link)
    return links

#~ d = feedparser.parse('http://feeds.huffingtonpost.com/huffingtonpost/LatestNews')
#~ print d.keys()
#~ print d['entries'][0].keys()
#~ print d['entries'][0]['title']
#~ print d['entries'][0]['link']

#~ url = u'http://'
#~ import requests
#~ hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
#~ req = requests.Request('GET', url, headers=hdr).prepare()
#~ print req

websites = {

'science':[
    'http://www.livescience.com/28954-ancient-europeans-mysteriously-vanished.html',
    'http://www.sciencedaily.com/releases/2013/04/130423135845.htm',
    'http://www.huffingtonpost.co.uk/2013/04/24/mars-rover-penis-nasa_n_3144656.html',
    #~ 'http://www.the-scientist.com/?articles.view/articleNo/35134/title/Lab-grown-Kidneys-Work-in-Rats/',
    #~ 'http://www.the-scientist.com/?articles.view/articleNo/35110/title/Nano-suit-Protects-Animals-from-Vacuum/',
    'http://www.nasa.gov/mission_pages/kepler/news/kepler-62-kepler-69.html',
    #~ 'http://www.the-scientist.com/?articles.view/articleNo/35088/title/A-Link-Between-Autism-and-Cannabinoids/',
    'http://www.the-scientist.com/?articles.view/articleNo/35106/title/Beer-Tastes-Intoxicating/',],
'inspiration':[
    'http://www.fourhourworkweek.com/blog/2013/05/02/a-few-thoughts-on-content-creation-monetization-and-strategy/',
    'http://shialabeowulf.tumblr.com/post/33670447154/99-life-hacks-to-make-your-life-easier',
    'http://www.fourhourworkweek.com/blog/2013/05/01/family-fat-loss-foodist/',
    'http://www.marksdailyapple.com/do-we-need-rites-of-passage-part-2/#axzz2RzYtMVEs',
    'http://www.youtube.com/watch?v=_MZiu0popJQ',
    'http://deadspin.com/college-athlete-ends-career-to-donate-bone-marrow-to-ma-477585815',],
'music':[
    'http://www.vice.com/read/the-flaming-lips-you-lust-video',
    'http://www.dak.com/reviews/3306story.cfm?Ref=G&PM=Brush&type=GCont&Srh=BrushClean&gclid=CKqg4uGr87YCFYNxQgodkkoAkA',
    'http://www.youtube.com/watch?v=d6J8O8Ououk&feature=youtu.be',
    'http://2020k.wordpress.com/2013/04/20/boards-of-canada-distribute-new-vinyl-releases-out-for-national-records-day/',
    'http://sunn.bandcamp.com/',],    
'animals':[
    'http://newswatch.nationalgeographic.com/2013/05/05/pictures-take-a-look-through-natures-most-transparent-animals/?source=hp_dl5_newswatch_transparent_animals_20130507',
    'http://news.nationalgeographic.com/news/2001/10/1003_SnappingShrimp.html',
    'http://deepseafauna.tumblr.com/',],
'entertainment':[
    'http://io9.com/patton-oswalts-8-minute-episode-vii-pitch-is-delightfu-474924224',
    'http://www.buzzfeed.com/nataliem15/14-engagement-photos-that-will-make-you-happy-you-a0ne',
    'http://www.youtube.com/watch?v=jHFhZLJajlc',
    'http://insidetv.ew.com/2013/04/21/game-of-thrones-dragon-scene/',],
'religion':[
    'http://www.dailykos.com/story/2013/05/01/1206266/-Killing-the-world-because-Jesus',
    'http://freethoughtblogs.com/axp/2013/04/23/scientific-cluelessness-and-idle-threats/',],
'diet':[
    'http://www.npr.org/blogs/health/2013/04/01/175961020/paleo-diet-echoes-physical-culture-movement-of-yesteryear',
    'http://www.ncbi.nlm.nih.gov/pubmed/23535495',
    'http://truth-out.org/opinion/item/15982-dont-let-monsanto-kill-the-humble-but-wholesome-dandelion',
    'http://www.edmontonjournal.com/Going+against+grain+People+with+celiac+disease+have+gluten+free+many+others+following/8302882/story.html',
    'http://worldtruth.tv/usda-forces-whole-foods-to-accept-monsanto/',
    'http://www.opposingviews.com/i/health/david-whipple-saves-mcdonalds-burger-1999-looks-exactly-same',
    'http://www.wheatbellyblog.com/2013/04/fettucine-alfredo-from-the-wheat-belly-cookbook/',
    'http://www.doctoroz.com/videos/paleo-diet-craze-pt-1',
    'http://www.marksdailyapple.com/primal-paleo-soda-water-listerine-tamarind-chicory-cherimoya/',],
'news':[
    'http://www.nytimes.com/2013/04/28/magazine/diederik-stapels-audacious-academic-fraud.html?pagewanted=all&_r=1',
    #~ 'http://www.foxnews.com/us/2013/04/15/thousands-giant-snails-causing-problems-for-florida-homeowners/?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+foxnews%2Fnational+%28Internal+-+US+Latest+-+Text%29',
    'http://rt.com/op-edge/boston-bombers-tsarnaev-brothers-172/',],
'politics':[
    'http://www.thedailybeast.com/articles/2013/05/01/shocker-oregon-health-study-shows-no-significant-health-impacts-from-joining-medicaid.html',
    'http://www.huffingtonpost.com/bruce-e-levine/the-systemic-crushing-of-_b_2840316.html',
    'http://www.nytimes.com/2013/04/28/opinion/sunday/whither-moral-courage.html?smid=fb-share&_r=0',
    'http://www.theatlantic.com/magazine/archive/2013/05/the-millennial-stimulus-plan/309297/',
    'http://www.thedailyshow.com/watch/wed-april-24-2013/weak-constitution',
    'http://www.guardian.co.uk/commentisfree/2013/apr/22/boston-marathon-terrorism-aurora-sandy-hook',],
'gaming':[
    'http://blogs.halowaypoint.com/Headlines/post/2013/05/01/The-Halo-Bulletin-5113.aspx',],
'tech':[
    'http://news.cnet.com/8301-11386_3-57582475-76/google-nike-jawbone-and-the-fight-to-win-wearable-computing/',
    'http://www.jorgecastro.org/2013/05/01/13-reasons-to-deploy-with-ubuntu-server-part-3/',
    'http://www.huffingtonpost.com/2013/04/26/new-york-times-google-glass_n_3166010.html?utm_hp_ref=technology',
    'http://www.huffingtonpost.com/2013/04/29/buddy-cup_n_3177488.html?utm_hp_ref=technology',
    'http://www.huffingtonpost.com/2013/04/29/mark-zuckerberg-salary_n_3178371.html?utm_hp_ref=technology',
    'http://www.huffingtonpost.com/2013/04/29/human-extinction-technology-video_n_3162456.html?utm_hp_ref=technology&ir=Technology',
    'http://www.zdnet.com/will-90-percent-of-users-always-hate-windows-8-7000012348/',
    'http://www.forbes.com/sites/johngaudiosi/2013/04/22/pizza-hut-enlists-pro-gamer-david-walshy-walsh-to-promote-microsoft-kinect-xbox-app/',],
'photography':[
    'http://www.collective-evolution.com/2013/02/02/21-fascinating-images-that-make-simple-things-profound/',
    'http://www.theatlantic.com/infocus/2013/04/winners-of-the-2013-sony-world-photography-awards/100504/',],
}

""" http://feedproxy.google.com/~r/entrepreneur/latest/~3/uzL35yJYLYc/story01.htm 
link redirects, so page parser doesn't get any data. User posts empty link. """

#~ import urllib2
#~ for url in ["http://entrian.com/", "http://entrian.com/does-not-exist/", "wharrgarbl"]:
    #~ try:
        #~ connection = urllib2.urlopen(url)
        #~ if str(connection.getcode())[0] == '2':
            #~ print 'success'
        #~ connection.close()
    #~ except urllib2.HTTPError as e:
        #~ print e.code
    #~ except urllib2.URLError as e:
        #~ print e.reason
    #~ except ValueError as e:
        #~ print e



#~ ts = Node.objects.get(user__username='user10')
#~ print ts.receivers.all()
#~ print ts.senders.all()
#~ print ts.incoming.all()
#~ print ts.outgoing.all()


#~ url = 'http://www.huffingtonpost.com/2013/04/26/new-york-times-google-glass_n_3166010.html'
#~ content= Content.objects.get(url=url)
#~ content.save(refresh=True)

#~ for topic in websites.values():
    #~ for url in topic:
        #~ print url
        #~ content = Content.objects.filter(url=url)
        #~ print '\t', content, '\n'
   
#~ url = 'http://www.nasa.gov/mission_pages/kepler/news/kepler-62-kepler-69.html'
#~ s = requests.Session()
#~ hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
#~ req = requests.Request('GET', url, headers=hdr).prepare()
#~ resp = s.send(req)
#~ print resp
#~ soup = BeautifulSoup(resp.content, "lxml")

#~ print websites['science']
            
""" uncomment to create users """
#~ for i in range(1,100):
    #~ print i
    #~ u = User.objects.create_user('user'+str(i+1), 'user@example.com', 'password')

""" uncomment to shuffle all connections """
#~ nodes = Node.objects.all()
#~ for node in nodes:
    #~ node.shuffle(verbose=True, connections=5)

""" uncomment to share random links (from RSS) """
nodes = Node.objects.all()
for node in nodes:
    web_sample = get_from_rss(3)
    for url in web_sample:
        print url, '\n'
        node.share(url)
    print node
    
""" uncomment to share random links (from website list) """
#~ nodes = Node.objects.all()
#~ for node in nodes:
    #~ topic = random.choice(websites.keys())
    #~ choices = len(websites[topic])
    #~ if choices > 5:
        #~ choices = 5
    #~ web_sample = random.sample(websites[topic], choices)
    #~ for url in web_sample:
        #~ node.share(url)
    #~ print node
    
    
""" uncomment to experiment with intersecting sets """
#~ def intersect_recursion(current, remaining, threshold):
    #~ new = remaining.pop()
    #~ intersect = current.intersection(new)
    #~ print intersect
    #~ if len(intersect) < threshold:
        #~ return intersect
    #~ elif not remaining:
        #~ return random.sample(intersect, threshold)        
    #~ else:
        #~ result = intersect_recursion(intersect, remaining, threshold) # len(result) always less than threshold
        #~ need = threshold - len(result)
        #~ if need:
            #~ remainder = intersect.difference(result)
            #~ result = result.union(random.sample(remainder, need))
        #~ return result
        
#~ networks = [set([1,2]), set([1,2,3,4,5]), set([1]), set([1,2,3]), set([1,2,3,4,5,6,7,8,9])]
#~ ##~ networks = [set([1,2,3,4,5]), set([1,2,3,4,5,6,7,8,9])]
#~ networks = sorted(networks, key=len)
#~ current = networks.pop()
#~ print networks
#~ ##~ print intersect_recursion(current, networks, 2)
#~ print set.union(*networks)

""" uncomment to play with url handling """
#~ from bs4 import BeautifulSoup
#~ import requests
#~ 
#~ class Link:
    #~ def __init__(self, url):
        #~ self.url = url
        #~ self.title = None
        #~ self.description = None
        #~ self.keywords = None
        #~ self.image = None
        #~ 
    #~ def save(self, *args, **kwargs):
        #~ """ 'name' refers to the name of the meta tag, and includes options 'description' and 'keywords' 
        #~ among others. If 'description' or 'keywords' tag is identified, self.description and self.keywords
        #~ are set to equal the content of the tag. Lowercase forced for consistency. """
        #~ if self.url and not (self.title or self.keywords or self.description or self.image):
            #~ s = requests.Session()
            #~ hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
            #~ req = requests.Request('GET', self.url, headers=hdr).prepare()
            #~ resp = s.send(req)
            #~ print 'resp', resp
            #~ if '404' in resp:
                #~ print self.url
            #~ soup = BeautifulSoup(resp.content, "lxml")
            #~ limit = 100#self._meta.get_field('title').max_length
            #~ self.title = soup.title.string[:limit]
            #~ print self.title
            #~ meta = soup.find_all('meta')
            #~ for tag in meta:
                #~ if 'name' in tag.attrs and tag.attrs['name'].lower() in ['keywords']:
                    #~ limit = 300#self._meta.get_field('keywords').max_length      # check field max_length
                    #~ content = tag.attrs['content'][:limit-3]+'...'          # limit field to max_length
                    #~ setattr(self, 'keywords', content) 
                #~ if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description']:
                    #~ print 'description detected'
                    #~ limit = 300#self._meta.get_field('description').max_length      # check field max_length
                    #~ content = tag.attrs['content'][:limit-3]+'...'          # limit field to max_length
                    #~ setattr(self, 'description', content)   
                    #~ print self.description
                #~ elif not self.description and 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:description', 'twitter:description']:
                    #~ print 'elif entered'
                    #~ field = tag.attrs['property'].lower()                       
                    #~ limit = 300#self._meta.get_field(field).max_length      # check field max_length
                    #~ content = tag.attrs['content'][:limit-3]+'...'          # limit field to max_length
                    #~ setattr(self, 'description', content)   
                #~ #if 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:image', 'twitter:image']:
                #~ #    field = tag.attrs['property'].lower()                       
                #~ #    limit = 300#self._meta.get_field(field).max_length      # check field max_length
                #~ #    content = tag.attrs['content'][:limit]                  # limit field to max_length
                #~ #    setattr(self, 'image', content)               
            #~ img = image_extractor(self.url, soup)
            #~ setattr(self, 'image', img[1])
                #~ 
            #~ if not self.description: # no meta description tag
                #~ ps = soup.find_all('p')
                #~ if ps:
                    #~ limit = 1000
                    #~ for p in ps:
                        #~ print len(p.text), p.text
                        #~ if len(p.text) > 100:
                            #~ self.description = p.text[:limit-3]+'...'
                            #~ break
#~ 
#~ import urllib
#~ 
#~ def getsize(url):
    #~ try:
        #~ file = urllib.urlopen(url)
        #~ size = file.headers.get("content-length")
        #~ file.close()
        #~ if size:
            #~ return int(size)
        #~ else:
            #~ return 0
    #~ except:
        #~ return 0
#~ 
#~ def image_extractor(url, soup=None):
    #~ if not soup:
        #~ s = requests.Session()
        #~ hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
        #~ req = requests.Request('GET', url, headers=hdr).prepare()
        #~ resp = s.send(req)
        #~ print 'resp', resp
        #~ soup = BeautifulSoup(resp.content, "lxml")
    #~ img = soup.body.find_all('img')
    #~ candidates = []
    #~ for tag in img:
        #~ # check each image, adding points for different tests
        #~ score = 0
        #~ url = tag.attrs['src']
        #~ if 'gravatar' in url:
            #~ break
        #~ 
        #~ if url[0] == '/':
            #~ parsed = urlparse(url)
            #~ url = urlunparse((parsed.scheme, parsed.netloc, url, '', '', ''))
        #~ 
        #~ # width check
        #~ #if 'width' in tag.attrs and tag.attrs['width'] > 200:
        #~ #    score += tag.attrs['width']/10.
        #~ 
        #~ # size check
        #~ score += getsize(url)/100
        #~ 
        #~ #if 'alt' in tag.attrs and tag.attrs['alt']:
        #~ #    score += 500
        #~ print score
        #~ if score > 20:
            #~ candidates.append((score, url))
    #~ 
    #~ candidates = sorted(candidates)
    #~ print candidates
    #~ #for c in candidates:
     #~ #   print c, '\n'
    #~ return candidates[-1]
    

""" uncomment to play with beautifulsoup """
#~ websitelist = random.choice(websites.values())
#~ url = random.choice(websitelist)
#~ s = requests.Session()
#~ hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
#~ req = requests.Request('GET', url, headers=hdr).prepare()
#~ resp = s.send(req)
#~ print 'resp', resp
#~ if '404' in resp:
    #~ print self.url
#~ soup = BeautifulSoup(resp.content, "lxml")
#~ print soup.body


    

##~ url = 'http://tinyurl.com/cn45f7d'
##~ url = 'http://news.yahoo.com/yellowstones-volcano-bigger-thought-134714973.html'
##~ url = 'http://www.tytnetwork.com'
#~ url = 'http://www.marksdailyapple.com/primal-paleo-soda-water-listerine-tamarind-chicory-cherimoya/'

#~ websitelist = random.choice(websites.values())
#~ url = random.choice(websitelist)
#~ l = Link(url)
#~ 
#~ l.save()
#~ print 'description:'
#~ print l.description, '\n'
#~ print l.image


#~ class Member(models.Model):
    #~ user = models.OneToOneField(User, related_name='member')
    #~ recruiters = models.ManyToManyField('self', through = 'Membership',  related_name = 'recruits',  symmetrical=False)
    #~ other_custom_info = ... 
    #~ 
#~ def create_member(member, instance, created, **kwargs):
    #~ if created:
        #~ member, created = Node.objects.get_or_create(user=instance)
#~ 
#~ post_save.connect(create_member, member=User)
#~ 
#~ class UserManagedGroup(Group):
    #~ leader = models.ForeignKey(Member, related_name='leaded_groups')
    #~ members = models.ManyToManyField(Member, through='Membership', related_name='managed_groups')
#~ 
#~ class Membership(models.Model):
    #~ recruit = models.ForeignKey(Member, related_name='memberships')
    #~ recruited_by = models.ForeignKey(Member, related_name='recruitments')
    #~ group = models.ForeignKey(UserManagedGroup, related_name='memberships')
    #~ 
    #~ date_added = ...
    #~ membership_justification = ...

