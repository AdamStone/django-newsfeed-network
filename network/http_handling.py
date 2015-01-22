from __future__ import division
import requests
from bs4 import BeautifulSoup
import urllib2
import ImageFile
from urlparse import urlparse, urlunparse


#~ def getsize(img_url):
    #~ try:
        #~ file = urllib2.urlopen(url)
        #~ size = file.headers.get("content-length")
        #~ file.close()
        #~ if size:
            #~ return int(size)
        #~ else:
            #~ return 0
    #~ except:
        #~ return 0
        
def getsizes(img_url):
    try:
        # get file size *and* image size (None if not known)
        file = urllib2.urlopen(str(img_url))
        size = file.headers.get("content-length")
        if size: size = int(size)
        else: size = 0
        p = ImageFile.Parser()
        while 1:
            data = file.read(1024)
            if not data:
                break
            p.feed(data)
            if p.image:
                return size, p.image.size
                break
        file.close()
        return size, (0, 0)
    except:
        return 0, (0, 0)

def standardize_url(url):
    if url and url[:7] != 'http://':
        url = 'http://' + url
    #~ if url[-1] != '/':
        #~ url += '/'
    return url
    
def validate_url(url):
    if url and url[:7] != 'http://':
        url = 'http://' + url
    try:
        connection = urllib2.urlopen(url)
        #~ if str(connection.getcode())[0] == '2':
            #~ print 'success'
        connection.close()
        return True
    except: 
        return False
    #~ except urllib2.HTTPError as e:
        #~ print e.code
        #~ return False
    #~ except urllib2.URLError as e:
        #~ print e.reason
        #~ return False
    #~ except ValueError as e:
        #~ print e
        #~ return False
    
def image_extractor(url, soup=None, limit=None, og=None):
    if not soup:
        s = requests.Session()
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.63 Safari/537.31'}
        req = requests.Request('GET', url, headers=hdr).prepare()
        resp = s.send(req)
        #~ print 'resp', resp
        soup = BeautifulSoup(resp.content, "lxml")
    img = soup.body.find_all('img')
    candidates = []
    for tag in img[:20]:
        # check each image, adding points for different tests
        score = 0
        try: 
            url = tag.attrs['src']
        except: 
            print 'no attribute src for tag ', tag
            try:
                url = tag.attrs['data-source-standard']
            except:
                print 'no attribute data-source-standard for tag'
                continue
        if url and url[0] == '/':
            parsed = urlparse(url)
            url = urlunparse((parsed.scheme, parsed.netloc, url, '', '', ''))   
        if 'gravatar' in url or '.gif' in url:
            continue
        if len(url) > limit or 'pagead' in url:
            continue
        
        # size check
        size, dimensions = getsizes(url)
        if not dimensions[1] or not dimensions[0]:
            continue
        aspect_ratio = dimensions[0]/dimensions[1]
        px_size = dimensions[0]*dimensions[1]
        print px_size
        
        if aspect_ratio > 0.25 and aspect_ratio < 4:
            score = px_size
        if dimensions[0] >= 570:
            img_type = True
        else:
            img_type = False
        
        if score > 2000:
            candidates.append((score, url, img_type))
    
    # consider og image
    if og:
        size, dimensions = getsizes(og)
        if not dimensions[1] or not dimensions[0]:
            pass
        else:
            score = 1000000 # bonus for being og image
            aspect_ratio = dimensions[0]/dimensions[1]
            px_size = dimensions[0]*dimensions[1]
            score += px_size
            if dimensions[0] > 450:
                img_type = True
            else:
                img_type = False
            candidates.append((score, og, img_type))
    
    candidates = sorted(candidates)
    if candidates:
        winner = candidates[-1]
        print 'winning score: ', winner[0]
        print 'type: ', winner[2]
        
        return winner[1], winner[2]
    else:
        return '', False
        
def scale_image(img_url, target_width, target_height):
    size, dimensions = getsizes(img_url)
    w, h = dimensions
    result = {'url':img_url, 'width':0, 'height':0, 'x0':0, 'y0':0, 
              'target_width':target_width, 'target_height':target_height, 
              'scaled_width':True}
    
    if w <= 0 or h <= 0:
        return result
        
    aspect_ratio = w/h
    target_ratio = target_width/target_height
        
    if aspect_ratio > target_ratio: # then height should be fit
        scaling = h/target_height
        result['height'] = target_height
        result['width'] = int(w/scaling)
    else:                        # then width should be fit
        result['scaled_width'] = False
        scaling = w/target_width
        result['width'] = target_width
        result['height'] = int(h/scaling)
    x0 = -(result['width']-target_width)/2.
    y0 = -(result['height'] - target_height)/2.
    
    result['x0'] = int(x0)
    result['y0'] = int(y0)
    
    return result
    
