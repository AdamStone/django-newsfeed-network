from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone

from http_handling import scale_image

def home(request):
    # if user is logged in, show user feed page
    if request.user.is_authenticated():
        user = request.user
        #~ user.node.shuffle()
        
        # handle forms            
        if 'q' in request.POST:
            url = request.POST['q']
            user.node.share(url) 
            """ need to add failsafes"""
            return HttpResponseRedirect('/')
            
        if 'shuffle' in request.POST:
            user.node.shuffle(verbose=True)
            return HttpResponseRedirect('/')
        
        # build feed
        """ still need to add user-shared links """
        feed = user.node.get_feed(maxlinks=20)
        sharers = {}
        contentlist = []
        for share in feed:
            if share.content not in contentlist:
                sharers[share.content] = [share.user]
                contentlist.append(share.content)
            else:
                sharers[share.content].append(share.user)
        left = []
        right = []
        for content in contentlist:
            if content.image:
                img_url = content.image
                img_type = content.image_type
                if img_type == False:
                    scaling = scale_image(img_url, 110, 110)
                    #~ left.append(content)
                else:
                    scaling = None
                    #~ right.append(content)
                content.scaling = scaling
            else:
                content.scaling = None
                
        #~ n = len(contents)
        #~ n = int(n/2)
        #~ left = contents[:n]
        #~ right = contents[n:]
        
        contentlist.reverse()
        while contentlist:
            col = (left, right)[len(contentlist) % 2]
            content = contentlist.pop()
            col.append((content, sharers[content]))
        
        
        # return context
        context = {'columns':(left, right)}
        return render(request, 'network/index.html', context)
    else:
        return render(request, 'network/home.html')
    
def meta(request):
    items = request.META.items()
    items.sort()
    return render(request, 'meta.html', {'items':items})    

