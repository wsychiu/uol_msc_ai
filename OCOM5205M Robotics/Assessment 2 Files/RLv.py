from RL import *
from math import floor

class MRP(MRP):
        
    # set up the weights, must be done whenever we train
    def init(self):
        self.w = np.ones(self.env.nF)*self.v0
        self.V = self.V_ # this allows us to use a very similar syntax for our updates
        self.S_= None
        
    #-------------------------------------------buffer related-------------------------------------
    # allocate a suitable buffer
    def allocate(self): 
        super().allocate()
        self.s = np.ones ((self.max_t, self.env.nF), dtype=np.uint32) *(self.env.nS+10)    
    
    #---------------------------------------- retrieve Vs ------------------------------------------
    def V_(self, s=None):
        return self.w.dot(s) if s is not None else self.w.dot(self.env.S_()) 
        
    def ΔV(self,s): # gradient: we should have used ∇ but jupyter does not like it
        return s

class TD(MRP):
    # ----------------------------- 🌖 online learning ----------------------    
    def online(self, s, rn,sn, done, *args): 
        self.w += self.α*(rn + (1-done)*self.γ*self.V(sn) - self.V(s))*self.ΔV(s)

class MDP(MDP(MRP)):

    def init(self):
        super().init()
        self.W = np.ones((self.env.nA, self.env.nF))*self.q0
        self.Q = self.Q_

    def Q_(self, s=None, a=None):
        #print(s.shape)
        W = self.W if a is None else self.W[a]
        return W.dot(s) if s is not None else np.matmul(W, self.env.S_()).T 

    # we should have used ∇ but python does not like it
    def ΔQ(self,s): 
        return s

class MCC(MDP):
    
    def init(self):
        super().init()
        self.store = True
        
    # ---------------------------- 🌘 offline, MC learning: end-of-episode learning-----------------------    
    def offline(self):  
        # obtain the return for the latest episode
        Gt = 0
        for t in range(self.t, -1, -1):
            s = self.s[t]
            a = self.a[t]
            rn = self.r[t+1]
            
            Gt = self.γ*Gt + rn
            self.W[a] += self.α*(Gt - self.Q(s,a))*self.ΔQ(s)

class Sarsa(MDP):

    def init(self): #α=.8
        super().init()
        self.step = self.step_an # for Sarsa we want to decide the next action in time step t

    # ----------------------------------------🌖 online learning ----------------------------------------
    def online(self, s, rn,sn, done, a,an):
        self.W[a] += self.α*(rn + (1-done)*self.γ*self.Q(sn,an) - self.Q(s,a))*self.ΔQ(s)
 
class Qlearn(MDP):

    #--------------------------------------🌖 online learning --------------------------------------
    def online(self, s, rn,sn, done, a,_):
        self.W[a] += self.α*(rn + (1-done)*self.γ*self.Q(sn).max() - self.Q(s,a))*self.ΔQ(s)
    
class XSarsa(MDP):

    # ------------------------------------- 🌖 online learning --------------------------------------
    def online(self, s, rn,sn, done, a,_):      
        # obtain the ε-greedy policy probabilities, then obtain the expecation via a dot product for efficiency
        π = self.π(sn)
        v = self.Q(sn).dot(π)
        self.W[a] += self.α*(rn + (1-done)*self.γ*v - self.Q(s,a))*self.ΔQ(s)

class Actor_Critic(PG(MDP)):

    def step0(self):
        self.γt = 1 # powers of γ
        
    # -------------------------------------- 🌖 online learning ------------------------------
    def online(self, s, rn,sn, done, a,_): 
        π, γ, γt, α, τ, t, ΔV, ΔQ = self.π, self.γ, self.γt, self.α, self.τ, self.t, self.ΔV, self.ΔQ
        
        δ = (1- done)*γ*self.V(sn) + rn - self.V(s)    # TD error is based on the critic estimate
        
        self.w    += α*δ*ΔV(s)                         # critic
        self.W[a] += α*δ*ΔQ(s)*(1 - π(s,a))*γt/τ       # actor
        self.γt *= γ  
        
class Sarsan(MDP):

    def init(self):
        super().init()
        self.store = True        # although online but we need to access *some* of earlier steps,
        self.step = self.step_an # for Sarsa we want to decide the next action in time step t

    # ----------------------------- 🌖 online learning ----------------------    
    def online(self, *args):
        τ = self.t - (self.n-1);  n=self.n
        if τ<0: return
        
        # we take the min so that we do not exceed the episode limit (last step+1)
        τ1 = τ+1
        τn = τ+n ; τn=min(τn, self.t+1 - self.skipstep)
        
        sτ = self.s[τ];  aτ = self.a[τ]
        sn = self.s[τn]; an = self.a[τn]
        done = self.done[τn]
        
        # n steps τ+1,..., τ+n inclusive of both ends
        self.W[aτ] += self.α*(self.G(τ1,τn) + (1-done)*self.γ**n *self.Q(sn,an) - self.Q(sτ,aτ))*self.ΔQ(sτ)

class TDλ(MRP):
    def __init__(self, λ=.5, **kw):
        super().__init__(**kw)
        self.λ = λ
    
    def step0(self):
        self.z = self.w*0

    # ----------------------------- 🌖 online learning ----------------------    
    def online(self, s, rn,sn, done, *args): 
        α, γ, λ = self.α, self.γ, self.λ
        self.z = λ*γ*self.z + self.ΔV(s)
        self.w += α*(rn + (1-done)*γ*self.V(sn) - self.V(s))*self.z
        
class trueTDλ(MRP):
    def __init__(self, λ=.5, **kw):
        super().__init__(**kw)
        self.λ = λ

    def step0(self):
        self.z = self.w*0
        self.vo = 0
    # ----------------------------- 🌖 online learning ----------------------    
    def online(self, s, rn,sn, done, *args): 
        α, γ, λ = self.α, self.γ, self.λ
        
        self.v = self.V(s)
        self.vn= self.V(sn)*(1-done)
        δ = rn + γ*self.vn - self.v
        self.z = λ*γ*self.z + (1-α*λ*γ*self.z.dot(s))*s
        
        self.w += α*(δ + self.v - self.vo )*self.z - α*(self.v - self.vo)*s
        self.vo = self.vn
        
class Sarsaλ(MDP):
    def __init__(self, λ=.5, **kw):
        super().__init__(**kw)
        self.λ = λ
        self.step = self.step_an # for Sarsa we want to decide the next action in time step t
    
    def step0(self):
        self.Z = self.W*0
    # ----------------------------------------🌖 online learning ----------------------------------------
    def online(self, s, rn,sn, done, a,an):
        self.Z[a] = self.λ*self.γ*self.Z[a] + self.ΔQ(s)
        self.W[a] += self.α*(rn + (1-done)*self.γ*self.Q(sn,an)- self.Q(s,a))*self.Z[a]

class trueSarsaλ(MDP):
    def __init__(self, λ=.5, **kw):
        super().__init__(**kw)
        self.λ = λ
        self.step = self.step_an # for Sarsa we want to decide the next action in time step t
        self.actions_list = {-2:'stop (for reset)'
                        , -1:'reverse'
                        , 0:'forward'
                        , 1:'turn left'
                        , 2:'turn right'}
    def step0(self):
        self.Z = self.W*0
        self.qo = 0
    # ----------------------------------------🌖 online learning ----------------------------------------
    def online(self, s, rn,sn, done, a,an):
        
        α, γ, λ = self.α, self.γ, self.λ
        
        self.q = self.Q(s,a)
        self.qn= self.Q(sn,an)*(1-done)
        δ = rn + γ*self.qn - self.q
        self.Z[a] = λ*γ*self.Z[a] + (1-α*λ*γ*self.Z[a].dot(s))*s
        
        self.W[a] += α*(δ + self.q - self.qo )*self.Z[a] - α*(self.q - self.qo)*s
        
        #best_action = choices(np.where(self.Q(sn)==max(self.Q(sn)))[0])[0]
        #best_action = self.actions_list[best_action]
        #print(f'Best next action: {best_action}')

        self.qo = self.qn
