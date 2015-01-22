from __future__ import division
import urllib2
import ImageFile

def getsizes(url):
    # get file size *and* image size (None if not known)
    print type(url)
    file = urllib2.urlopen(url)
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
    return size, None

def scale_image(url, target_width, target_height):
    size, dimensions = getsizes(url)
    w, h = dimensions
    result = {'width':0, 'height':0, 'scaled_width':True}
    
    if w <= 0 or h <= 0:
        return result
        
    aspect_ratio = w/h
    target_ratio = target_width/target_height
        
    if aspect_ratio > target_ratio: # then height should be fit
        scaling = h/target_height
        result['height'] = target_height
        result['width'] = w/scaling
    else:                        # then width should be fit
        result['scaled_width'] = False
        scaling = w/target_width
        result['width'] = target_width
        result['height'] = h/scaling
    x0 = -(result['width']-target_width)/2.
    y0 = -(result['height'] - target_height)/2.
    
    result['x0'] = x0
    result['y0'] = y0
    
    return result
    
url = 'http://www.wheatbellyblog.com/wp-content/uploads/2013/04/Fettuchini-2-225x300.jpg'

for item in scale_image(url, 150, 150).items():
    print item
