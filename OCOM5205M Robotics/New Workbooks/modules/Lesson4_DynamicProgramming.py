import Lesson3_MDPsGridWorld

def P(nS):
    p = np.zeros(nS)
    for s in range(nS):
        p[s] = rand()
        
    return p/p.sum()

def P(nS,nA):
    p = np.zeros((nS,nA))
    for s in range(nS):
        for a in range(nA):
            p[s,a] = rand()
            
        
    # /p.sum() to make sure that this is a joint probability density, i.e. p.sum()==1
    return p/p.sum() 

def P(nS,nA):
    pr = np.zeros((nS,nA)) # joint
    p  = np.zeros((nS,nA)) # conditional
    
    # first create a joint probability
    for sn in range(nS):
        for a in range(nA):
            pr[sn,a] = rand()

    # to make sure that this is a joint probability density
    pr=pr/pr.sum() 
    
    # now create a conditional probability via Bayes rule
    for a in range(nA):
        p[:,a] = pr[:,a]/pr[:,a].sum()
            
            
    return p

def dynrand(nS, nA, nR): # states, actions, rewards dimensions 
    #first joint: p[sn,rn, s,a]
    p  = np.random.rand(nS,nR,  nS,nA)
    p /= p.sum()
    
    #convert it to conditional: p[sn,rn| s,a] 
    for s in range(nS):
        for a in range(nA):
            p[:,:, s,a] /= p[:,:, s,a].sum()
        
    return p