import random


def populate(node, content, newconnections=15, getrandom=False, verbose=False):   # populate new connections 
    """ to-do: check for presence of new candidates already in existing connections"""
    c_networks = sorted([set(c.sharers.exclude(pk=node.pk)) for c in content], key=len)
    if len(c_networks) > 1:
        population = intersect_recursion(None, c_networks, newconnections)
    else:
        population = c_networks[0]        
    if verbose: print 'Intersect population: ', population
    need = newconnections - len(population)
    if need:    #not enough intersections to fulfill requested connections
        if verbose: print 'Need %s more; getting share unions...' % need
        c_networks = [set(c.sharers.exclude(pk=node.pk)) for c in content]
        remainder = set.union(*c_networks).difference(population)
        if len(remainder) >= need:
            population = population.union(random.sample(remainder, need))
        else:
            need = newconnections - len(population)
            if verbose: print 'Still need %s more; getting random...' % need
            population = population.union(remainder) #still falls short; need true random for remainder
    return population
    
def intersect_recursion(current, remaining, threshold):
    if current:
        new = remaining.pop()
        intersect = current.intersection(new)
    else:
        intersect = remaining.pop()
    if len(intersect) < threshold: 
        return intersect
    elif not remaining:
        return random.sample(intersect, threshold)        
    else:
        result = intersect_recursion(intersect, remaining, threshold) # len(result) always less than threshold
        need = threshold - len(result)
        if need:
            remainder = intersect.difference(result)
            result = result.union(random.sample(remainder, need))
        return result

### original:
#~ def populate(node, newconnections=15, getrandom=False, verbose=False):         # populate new connections 
    #~ """ to-do: check for presence of new candidates already in existing connections"""
    #~ """ note: newconnections must be < total users """
    #~ content = node.sharedcontent.all()
    #~ if getrandom or not content:  
        #~ if verbose: print 'Random search; getting sample...'
        #~ population = random.sample(Node.objects.exclude(pk=node.pk), newconnections) #bottleneck 
        #~ enough = True
    #~ else:
        #~ if verbose: print 'checking intersections...'
        #~ c_networks = [set(c.sharers.exclude(pk=node.pk)) for c in content]
        #~ population = set.intersection(*c_networks)
        #~ if verbose: print 'intersect population: ', population
        #~ if len(population) >= newconnections:
            #~ population = random.sample(poplulation, newconnections)
            #~ enough = True
        #~ else:
            #~ enough = False
        #~ if verbose: print 'Building connections...'
    #~ for node in population:     
        #~ c = Connection(sender=node,receiver=node)
        #~ c.save()
    #~ if verbose: print 'Done.'
    #~ if not enough:
        #~ remaining = newconnections-len(population)
        #~ node.populate(newconnections=remaining, getrandom=True)    
