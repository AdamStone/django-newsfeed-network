from django.db import models
from django.db.models import Q
from django.utils import timezone
import datetime
import random
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import adaptive
from bs4 import BeautifulSoup
import requests
import socket
import urllib2
try:
    from urllib.parse import urlsplit, urlunsplit
except ImportError:     # Python 2
    from urlparse import urlsplit, urlunsplit

""" UTILITY """

from http_handling import standardize_url, image_extractor, validate_url

socket.setdefaulttimeout(10)

""" CUSTOM FIELDS """

class NoSlashURLField(models.URLField):
    description = "Remove the slash"
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        super(NoSlashURLField, self).__init__(*args, **kwargs)
        
    def to_python(self, value):
        def split_url(url):
            """
            Returns a list of url parts via ``urlparse.urlsplit`` (or raises a
            ``ValidationError`` exception for certain).
            """
            try:
                return list(urlsplit(url))
            except ValueError:
                # urlparse.urlsplit can raise a ValueError with some
                # misformatted URLs.
                raise ValidationError(self.error_messages['invalid'])

        value = super(NoSlashURLField, self).to_python(value)
        if value:
            url_fields = split_url(value)
            if not url_fields[0]:
                # If no URL scheme given, assume http://
                url_fields[0] = 'http'
            if not url_fields[1]:
                # Assume that if no domain is provided, that the path segment
                # contains the domain.
                url_fields[1] = url_fields[2]
                url_fields[2] = ''
                # Rebuild the url_fields list, since the domain segment may now
                # contain the path too.
                url_fields = split_url(urlunsplit(url_fields))
#            if not url_fields[2]:
#                # the path portion may need to be added before query params
#                url_fields[2] = '/'
            value = urlunsplit(url_fields)
        return value


""" DATA CLASSES """

class Content(models.Model):
    url = NoSlashURLField(max_length=1000)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, max_length=200)
    keywords = models.TextField(blank=True)    
    image = models.URLField(blank=True, max_length=1000)
    image_type = models.NullBooleanField(default=None)
    #~ image_type = models.PositiveSmallIntegerField(null=True)
   #sharers = ManyToManyField(Node, related_name = sharedcontent)
    
    def __unicode__(self):
        return self.url
        
    def save(self, refresh=False, *args, **kwargs):
        if self.url:
            if refresh or not (self.title and self.description and self.image):
                s = requests.Session()
                hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
                req = requests.Request('GET', self.url, headers=hdr).prepare()
                resp = s.send(req)
                print resp
                soup = BeautifulSoup(resp.content, "lxml")
                limit = self._meta.get_field('title').max_length    # check field max_length
                if soup.title.string:
                    self.title = soup.title.string[:limit]              # limit title to max_length
                meta = soup.find_all('meta')
                og = None
                for tag in meta:
                    if 'name' in tag.attrs and tag.attrs['name'].lower() in ['keywords']:
                        #~ limit = self._meta.get_field('keywords').max_length      # check field max_length
                        if 'content' in tag.attrs:
                            content = tag.attrs['content']#[:limit-3]+'...'           # limit field to max_length
                            setattr(self, 'keywords', content) 
                    if 'name' in tag.attrs and tag.attrs['name'].lower() in ['description']:
                        limit = self._meta.get_field('description').max_length   # check field max_length
                        content = tag.attrs['content'][:limit-3]+'...'           # limit field to max_length
                        setattr(self, 'description', content)   
                    elif not self.description and 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:description', 'twitter:description']:
                        field = tag.attrs['property'].lower()                       
                        limit = self._meta.get_field('description').max_length           # check field max_length
                        content = tag.attrs['content'][:limit-3]+'...'           # limit field to max_length
                        setattr(self, 'description', content)   
                    if 'property' in tag.attrs and tag.attrs['property'].lower() in ['og:image']:#, 'twitter:image']:
                        field = tag.attrs['property'].lower()                       
                        og = tag.attrs['content'] 
                if not self.description: # no meta description tag
                    ps = soup.find_all('p')
                    if ps:
                        limit = self._meta.get_field('description').max_length
                        for p in ps:
                            if len(p.text) > 100:
                                self.description = p.text[:limit-3]+'...'
                                break
                    
                limit = self._meta.get_field('image').max_length
                print 'extracting image...'
                img, img_type = image_extractor(self.url, soup, limit, og)
                print 'before set: ', self.image_type
                setattr(self, 'image', img)   
                setattr(self, 'image_type', img_type)
                print 'after set: ', self.image_type
                
            super(Content, self).save(*args, **kwargs)
            print 'from query: ', Content.objects.get(pk=self.pk).image_type
        
    def split_title(self):
        if '|' in self.title:
            index = self.title.index('|')
            return self.title[:index], self.title[index+2:]
        else: 
            return self.title, ''
        
        
        
class Node(models.Model):
    user = models.OneToOneField(User)
    receivers = models.ManyToManyField('self', through='Connection', related_name='senders', blank=True, null=True, symmetrical=False)
    sharedcontent = models.ManyToManyField('Content', through='Share', related_name='sharers', blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % self.user
        
    def shuffle(self, connections = 15, getrandom=False, verbose=False):
        """ note: newconnections must be < total users """
        self.purge()
        self.populate(connections, getrandom, verbose=verbose)    
    shuffle.alters_data = True
        
    def purge(self):
        self.senders.clear()
    purge.alters_data = True
    
    def populate(self, newconnections=15, getrandom=False, verbose=False): 
        if verbose: print '\nPopulating %s' % self
        ### get population ###
        content = self.sharedcontent.all()
        if newconnections > len(Node.objects.exclude(pk=self.pk)):  # make sure enough nodes exist to satisfy connections
            if verbose: print 'Connecting to all node objects...'
            population = Node.objects.exclude(pk=self.pk)           
        elif getrandom or not content:                              # random population
            if verbose: print 'Random search; getting sample...'
            population = random.sample(Node.objects.exclude(pk=self.pk), newconnections)
        else:                                                       # adaptive population
            if verbose: print 'Checking intersections...'
            population = adaptive.populate(self, content, newconnections, getrandom, verbose)    
        need = newconnections - len(population)
        if need:
            # need to account for error when remainder < need
            remainder = set(Node.objects.exclude(pk=self.pk)).difference(population)
            population = set(population).union(random.sample(remainder, need))
        ### create connections ##
        for node in population:                       #42, 23, 16, 2
            c = Connection(sender=node,receiver=self) #35, 31, 29, 26, 17, 15, 12, 5, 0 cnn
            c.save()
    populate.alters_data = True
        
    def share(self, url):  
        if validate_url(url): 
            try:
                content = Content.objects.get(url=url)  
            except Content.DoesNotExist:               
                content = Content(url=url, image_type=None) 
                content.save()
            timestamp = timezone.now()
            if content.title:
                s = Share(content=content, user=self, timestamp=timestamp)
                s.save()
        else:
            print 'validation fail'
    share.alters_data = True
    
    def get_feed(self, maxlinks=40):        
        feed = Share.objects.filter(Q(user__pk__in = (node.pk for node in self.senders.all())) |  Q(user__pk = self.pk))
        return feed[:maxlinks]
        
def create_node(sender, instance, created, **kwargs):
    if created:
        node, created = Node.objects.get_or_create(user=instance)

post_save.connect(create_node, sender=User)
    
    
""" RELATIONSHIP CLASSES """

class Connection(models.Model):
    sender = models.ForeignKey(Node, related_name='outgoing')
    receiver = models.ForeignKey(Node, related_name='incoming')
    
    def __unicode__(self):
        return  "%s sends to %s" % (self.sender, self.receiver)
        
class Share(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    content = models.ForeignKey(Content)
    user = models.ForeignKey(Node)
    
    def __unicode__(self):
        return u"%s shared %s" % (self.user, self.content) 
    
    class Meta:
        ordering = ['-timestamp']
