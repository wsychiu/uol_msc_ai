import numpy as np
import random
import time
import math
import io
import sys
import os

from IPython.display import clear_output
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib import colors
from numpy.random import rand, seed, randint, choice
from random import choices, sample
from tqdm import trange, tqdm

class Grid:
    def __init__(self, gridsize=[6,9], nA=4, s0=3*9, goals=None, Vstar=None):
        self.rows = gridsize[0]
        self.cols = gridsize[1]
        self.nS = self.cols*self.rows # we assume cells IDs go left to right and top down
        self.goals = [self.nS-1, self.nS-1] if goals is None else ([goals[0], goals[0]] if len(goals)==1 else goals)
        self.Vstar = Vstar # optimal state value, needed for some of the environments
        self.s0 = s0
        self.s = s0
        self.trace = [self.s0]
        
        # actions ---------------------------------------------------------------------       
        cols = self.cols
        self.actions_2 = [-1, +1]
        self.actions_4 = [-1, +1, -cols, +cols]     # left, right, down and up
        self.actions_8 = [-1, +1, -cols, +cols, -1-cols, -1+cols, 1-cols, 1+cols] # left-down, left-up, right-down, right-up

        self.nA = nA
        if nA==2: self.actions = self.actions_2
        if nA==4: self.actions = self.actions_4
        if nA==8: self.actions = self.actions_8
        
        # rewards types-----------------------------------------------------------------
        self.nR = 4
        self.rewards = [0, 1, 0, -100] # intermediate, goal1, goal2, cliff
        self.obstacles, self.cliffs = [], [] # lists that will be checked when doing actions
        
        
    def reset(self, withtrace=True):
        self.s = self.s0
        if withtrace: self.trace = [self.s0]
        return self.s_()
    #-----------------------------------------rewards related-------------------------------------------
    def rewards_set(self):
        return np.array(list(set(self.rewards)))
        
    def reward(self):
        stype = self.stype()
        reward = self.rewards[stype]
        if stype==3: self.reset(False)    # s in cliffs
        return reward, 2>=stype>=1        # either at goal1 or goal2
    
    #-----------------------------------------actions related-------------------------------------------
    def invalid(self, s,a):
        cols = self.cols
        # invalid moves are 
        # 1. off grid boundaries
        # 2. off the right edge (last and is for right up and down diagonal actions)
        # 3. off the left edge  (last and is for left  up and down diagonal actions)
        # 4. into an obstacle
        return      not(0<=(s+a)<self.nS) \
                    or (s%cols!=0 and (s+a)%cols==0 and (a==1 or a==cols+1 or a==-cols+1))  \
                    or (s%cols==0 and (s+a)%cols!=0 and (a==-1 or a==cols-1 or a==-cols-1)) \
                    or (s+a) in self.obstacles

    def step(self, a, *args):
        a = self.actions[a]
        if not self.invalid(self.s,a): self.s += a
        
        self.trace.append(self.s)
        reward, done = self.reward()       # must be done in this order for the cliff reset to work properly
        return self.s_(), reward, done, {} # empty dict for compatibility
    
    #-----------------------------------------state related-------------------------------------------
    # useful for inheritance, observation can be a state (index) or a state representation (vector or image)
    def s_(self):
        return self.s
    
    # returns the number of states that are available for the agent to occupy
    def nS_available(self):
        return self.nS - len(self.obstacles)
    
    #-----------------------------------------goals related-------------------------------------------
    # returns the type of the current state (0: intermediate, 1 or 2 at goal1 or goal2, 3:off cliff)
    def stype(self):
        s, goals, cliffs = self.s, self.goals, self.cliffs
        # the order is significant and must not be changed
        return [s not in goals+cliffs, s==goals[0], s==goals[1], s in cliffs].index(True)
    
    def isatgoal(self):
        return self.stype() in [1,2] # either at goal1 or goal2

class Grid(Grid):
    def __init__(self, reward='',  style='', **kw):
        super().__init__(**kw)
    
        # explicit rewards for[intermediate,goal0,goal1, cliff] states
        self.reward_    = [0,    1,   0, -100] # this is the default value for the rewards
        self.cliffwalk  = [-1,  -1,  -1, -100]
        self.randwalk   = [ 0,   0,   1,    0]
        self.randwalk_  = [ 0,  -1,   1,    0]
        self.reward0    = [-1,   0,   0,   -1]
        self.reward_1   = [-1,  -1,  -1,   -1]
        self.reward1    = [-1,   1,   1,   -1]
        self.reward10   = [-1,  10,  10,   -1]
        self.reward100  = [-1, 100, 100,   -1]
        self.my_reward  = [0, 1, 0, 0]
        

        if reward: self.rewards  = getattr(self, reward)
        self.style = style
        
        # accommodating grids styles -------------------------------------------------------------
        self.X, self.Y = None, None
        self.Obstacles = self.Cliffs = 0 # np arrays for display only, related to self.obstacles, self.cliffs
        self.wind = [0]*10               # [0,0,0,0,0,0,0,0,0,0]
        
        if self.style=='cliff':
            self.Cliffs = None           # for displaying only, to be filled when render() is called
            self.cliffs = list(range(1,self.cols-1))
            
        elif self.style=='maze':
            self.Obstacles = None        # for displaying only, to be filled when render() is called
            rows = self.rows
            cols = self.cols
            midc = int(cols/2)
            obstacles1 = list(range(2+2*cols, 2+(rows-1)*cols, cols))    # set of vertical obstacles near the start
            obstacles2 = list(range(5+cols, 2*cols-3))                   # set of horizontal obstacles
            obstacles3 = list(range(-2+4*cols,-2+(rows+1)*cols, cols))   # set of vertical obstacles near the end
            self.obstacles = obstacles1 + obstacles2 + obstacles3        # concatenate them all 

        # upward winds intensity for each column
        elif self.style=='windy':
            self.wind = [0,0,0,1,1,1,2,2,1,0] # as in example 6.5 of the book
    
    # override the step() function so that it can deal with wind
    def step(self, a, *args):
        a = self.actions[a]
        if not self.invalid(self.s,a): self.s += a
        
        if self.style=='windy':
            maxwind = self.wind[self.s%self.cols]
            for wind in range(maxwind, 0, -1): # we need to try apply all the wind or at least part of it
                if not self.invalid(self.s, wind*self.cols): self.s += wind*self.cols; break
        
        self.trace.append(self.s)
        reward, done = self.reward()       # must be done in this order for the cliff reset to work properly
        return self.s_(), reward, done, {} # empty dict for compatibility

class Grid(Grid):
    def __init__(self, pause=0, figsize=None, **kw):
        super().__init__(**kw)
        
        self.figsize = figsize # desired figure size        
        self.fig = None        # figure handle, may have several subplots        
        self.ax0 = None        # Grid subplot handle
        
        self.pause = pause     # pause to slow animaiton
        self.arrows = None     # policy arrows (direction of action with max value)
        
        # assuming env is not dynamic, otherwise should be moved to render() near self.to_pos(self.s)
        self.start = self.to_pos(self.s0)         
        self.goal1 = self.to_pos(self.goals[0])
        self.goal2 = self.to_pos(self.goals[1])
        self.cmap = colors.ListedColormap(['w', 'darkgray'])

    # state representation function that converts 1-d list of state representation into a 2-d coordinates
    def to_pos(self, s):
        return [s%self.cols + 1, s//self.cols + 1]

    #------------------------------------------initialise------------------------------------------------- 
    def init_cells(self, cells): 
        Cells = np.zeros((self.rows+1, self.cols+1),  dtype=bool)
        Cells[0,0] = True # to populate for drawing 
        poses = self.to_pos(np.array(cells))
        Cells[poses[1], poses[0]] = True
        return Cells[1:,1:]
    
    #------------------------------------------render ✍️-------------------------------------------------
    # this function is to protect render() called twice for Gridi
    def render(self, **kw):
        self.render__(**kw)

    # we have placed most of the render overhead in the render() function to keep the rest efficient.
    # this funciton must not be called directly instead render() is to be called
    def render__(self, underhood='', pause=None, label='', subplot=131, large=False, 
               animate=True, image=False, saveimg=False,  **kw):
        
        if self.figsize is None:
            if   self.rows==1:             self.figsize = (15,.5) 
            elif underhood=='Q':           self.figsize = (20, 10)
            elif underhood=='V' and large: self.figsize = (30, 25)
            else:                          self.figsize = (17, 3)
        if image: self.figsize = (17, 3) # changing the default figure size is dissallowed for games

        if self.fig is None: self.fig = plt.figure(1)
        #if self.ax0 is None: self.ax0 = plt.subplot(subplot)
        plt.gcf().set_size_inches(self.figsize[0], self.figsize[1])
            
        #if   animate: self.ax0 = plt.subplot(subplot)
        #elif image:   plt.cla() 
        self.ax0 = plt.subplot(subplot)
        if image and not animate: plt.cla()
        
        
        # get hooks for self properties
        rows, cols = self.rows, self.cols
        pos, start, goal1, goal2 = self.to_pos(self.s), self.start, self.goal1, self.goal2
        
        pause = self.pause if pause is None else pause
        
        # a set of properties for the grid subplot
        
        prop = {'xticks': np.linspace(0, cols, cols+1),     'xticklabels':[],
                'yticks': np.linspace(0, rows, rows+1)+.01, 'yticklabels':[],
                'xlim':(0, cols), 'ylim':(0, rows), 'xlabel': label} # useful info
        self.ax0.update(prop)
        self.ax0.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
        if self.style not in ['maze', 'cliff']: self.ax0.grid(True)

        # robot visuals :-)
        mrgn = .5
        eyes = '˚-˚' if underhood!='Q' else '' 
        body = 'ro'  if underhood!='Q' else 'co'
        
        # plot goals and start state
        for (x,y), s in zip([goal1, goal2, start], ['G', 'G', 'S']):
            self.ax0.text(x-mrgn, y-mrgn, s, fontsize=14)
        
        # plot robot
        self.ax0.text(pos[0]-mrgn-.2, pos[1]-mrgn-.15, eyes, fontsize=10)
        self.ax0.plot(pos[0]-mrgn,    pos[1]-mrgn,     body, markersize=15) 
        #self.ax0.plot(pos, body, markersize=15) # this causes the body not be up to date in later lessons

        # to reduce overhead, pre-store coordinates in the grid only when render is needed
        if self.X is None: 
            self.X, self.Y = np.array(self.to_pos(np.arange(self.nS))) 
            self.Ox, self.Oy = np.arange(cols+1), np.arange(rows+1)

        # underhood obstacles and a cliffs
        if self.style=='maze':  
            if self.Obstacles is None: self.Obstacles = self.init_cells(self.obstacles)
            self.ax0.pcolormesh(self.Ox, self.Oy, self.Obstacles, edgecolors='lightgray', cmap=self.cmap)
        
        if self.style=='cliff': 
            if self.Cliffs is None: self.Cliffs = self.init_cells(self.cliffs)
            self.ax0.pcolormesh(self.Ox, self.Oy, self.Cliffs, edgecolors='lightgray', cmap=self.cmap)

        # this means that the user wants to draw the policy arrows (actions)
        if 'Q' in kw and underhood=='': underhood='maxQ'
        
        # a placeholder function for extra rendering jobs
        render_ = getattr(self, 'render_'+ underhood)(**kw)
        # windy style needs a bespoke rendering
        if self.style =='windy': self.render_windy()

        if image: self.render_image(saveimg=saveimg)
            
        # to animate clear and plot the Grid
        if animate: clear_output(wait=True); plt.show(); time.sleep(pause)
        #else: plt.subplot(subplot)
    
    #-------------------------helper functions for rendering policies and value functions---------------------
    def render_(self, **kw):
        pass # a placeholder for a another drawing if needed
    
    def render_image(self, **kw):
        pass # a placeholder for capturing and saving Grid as images
    
    # renders all states numbers' reprsentation on the grid
    def render_states(self, **kw):
        X,Y  = self.X, self.Y
        for s in range(self.nS): 
            self.ax0.text(X[s]-.5,Y[s]-.5, s, fontsize=13, color='g')

def animate_right(gw=Grid(), pause=0):
    gw.s=gw.s0 # reset the agent position
    # let us go right
    for s in range(5):
        gw.step(1)
        gw.render(pause=pause)

def scan(env, animate=True, pause=0):
    env.s = 0 # env.s0 # reset the agent position

    # scan the whole env
    for s in range(env.s, env.nS):#env.s0,env.s0+1):
        if s in env.obstacles: continue
        for a in range(gw.nA):
            env.s = s
            env.render(animate=animate, pause=pause)
            env.step(a)
            env.render(animate=animate, pause=pause)
        env.s = s
        #plt.pause(.5)

def wander(gw, animate=True, pause=0):
    gw.s=gw.s0 # reset the agent position
    
    # let us go right
    for s in range(gw.cols):
        gw.step(1)
        gw.render(animate=animate, pause=pause)
    
    # let us go left
    for s in range(gw.rows):
        gw.step(0)
        gw.render(animate=animate, pause=pause)

    # scan the whole env
    for s in range(gw.s,gw.nS):#gw.s0,gw.s0+1):
        if s in gw.obstacles: continue
        for a in range(gw.nA):
            gw.s = s
            gw.render(animate=animate, pause=pause)
            gw.step(a)
            gw.render(animate=animate, pause=pause)
        gw.s = s
        #plt.pause(.5)

class Grid(Grid):
    def __init__(self, **kw):
        super().__init__(**kw)

    def init_arrows(self):       
        self._left,      self._right,   self._down,       self._up       = tuple(range(0,4))
        self._left_down, self._left_up, self._right_down, self._right_up = tuple(range(4,8))
        
        # works for quiver and pos, max action can potentially go upto 8! if we are dealing with a grid world
        self.arrows = np.zeros((self.nA,2), dtype=int)
        
        self.arrows[self._left ] =[-1, 0]  # '←'
        self.arrows[self._right] =[ 1, 0]  # '→'
        
        if self.nA>2:
            self.arrows[self._down ] =[ 0,-1]  # '↓'
            self.arrows[self._up   ] =[ 0, 1]  # '↑'

        if self.nA>4:
            self.arrows[self._left_down ]=[-1,-1]  # '↓←'
            self.arrows[self._left_up   ]=[-1, 1]  # '↑←'
            self.arrows[self._right_down]=[ 1,-1]  # '→↓'
            self.arrows[self._right_up  ]=[ 1, 1]  # '→↑'
    

    # renders a policy
    def render_π(self, π=None, **kw): 
        if π is None: π=np.ones(self.nS, dtype=int)
        if self.arrows is None: self.init_arrows()
        X, Y = self.X, self.Y
        U, Z = self.arrows[π].T
        ind = [s for s in range(self.nS) if s not in self.goals and s not in self.obstacles + self.cliffs]
        ind = np.array(ind)
        if ind.any()==False: return
        plt.quiver(X[ind]-.5,Y[ind]-.5,  U[ind],Z[ind],color='b')
  
    # renders a policy deduced from a Q function
    def render_maxQ(self, Q=None, **kw): 
        if Q is None: Q=np.ones((self.nS, self.nA ))
        X, Y = self.X, self.Y
        if self.arrows is None: self.init_arrows()
        U, Z = self.arrows[np.argmax(Q,1)].T
        ind  = np.sum(Q,1)!=0
        if ind.any()==False: return
        plt.quiver(X[ind]-.5,Y[ind]-.5,  U[ind],Z[ind],color='b')
    
    # renders state value function
    def render_V(self, V=None, **kw):
        if V is None: V=np.ones(self.nS)
        X,Y  = self.X, self.Y
        fntsz, clr = 14 - int(self.cols/5), 'b'
        for s in range(self.nS):
            if s in self.obstacles or s in self.goals: continue
            plt.text(X[s]-.7,Y[s]-.7, '%.1f  '% V[s], fontsize=fntsz, color=clr) 
    
    # renders action-state value function
    def render_Q(self, Q=None, **kw):
        if Q is None: Q=np.ones((self.nS, self.nA ))
        X,Y  = self.X, self.Y
        fntsz, mrgn, clr = 12 - (5-self.nA) - int(self.cols/5), 0.4, 'b'
        for s in range(self.nS):
            if s in self.obstacles: continue        
            #  '→', '←', '↑', '↓'
            plt.text(X[s]-mrgn,Y[s]-mrgn, '←%.2f, '% Q[s,0], ha='right', va='bottom', fontsize=fntsz, color=clr) 
            plt.text(X[s]-mrgn,Y[s]-mrgn, '%.2f→  '% Q[s,1], ha='left' , va='bottom', fontsize=fntsz, color=clr)
            if self.nA==2: continue
            plt.text(X[s]-mrgn,Y[s]-mrgn, '↓%.2f, '% Q[s,2], ha='right', va='top'   , fontsize=fntsz, color=clr) 
            plt.text(X[s]-mrgn,Y[s]-mrgn, '%.2f↑  '% Q[s,3], ha='left' , va='top'   , fontsize=fntsz, color=clr) 

class Grid(Grid):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        # randwalk related
        self.letters = None                    # letter rep. for states
        
    #---------------------------------helper functions specific for some env and exercises----------------------
    # renders winds values on a grid
    def render_windy(self, **kw):
        for col in range(self.cols): # skipping the first and final states
            plt.text(col+.2,-.5, self.wind[col], fontsize=13, color='k')
        plt.text(6.15,1, '⬆',fontsize=60, color='lightgray')
        plt.text(6.15,4, '⬆',fontsize=60, color='lightgray')
    
    # renders a trace path on a grid
    def render_trace(self, **kw):
        poses = self.to_pos(np.array(self.trace))
        plt.plot(poses[0]-.5, poses[1]-.5, '->c')

    def render_V(self, **kw):
        super().render_V(**kw)
        if self.rows==1: self.render_letters()

    # renders all states letters' reprsentation on the grid
    def render_letters(self, **kw): # for drawing states numbers on the grid
        if self.nS>26: return
        X,Y  = self.X, self.Y
        # to reduce overhead, create the list only when render_letters is needed
        if self.letters is None: self.letters = self.letters_list() 
        for s in range(1,self.nS-1): # skipping the first and final states
            plt.text(X[s]-.5,Y[s]+.02, self.letters[s], fontsize=13, color='g')
    
    def letters_list(self, **kw):
        letters = [chr(letter) for letter in range(ord('A'),ord('A')+(self.nS-2))]
        letters.insert(0, 'G1')
        letters.append('G2')
        return letters

# jumping grid !
class Grid(Grid):
    def __init__(self, jump=1, randjump=True, **kw):
        super().__init__(**kw)
        self.jump = jump
        self.randjump = randjump
        
    #-----------------------------------------actions related-------------------------------------------
    def step(self, a):
        jump = randint(1, min(self.jump, self.nS - self.s) +1) if self.randjump else self.jump
        if self.jump==1: return super().step(a)
            
        a = self.actions[a]*jump
        if not self.invalid(self.s, a):  
            #print('valid jump')
            self.s += a
        else: 
            #print('invalid jump')
            self.s = max(min(self.s+a, self.nS-1),0)
        
        self.trace.append(self.s)
        reward, done = self.reward() 
        return self.s_(), reward, done, {}

import cv2
class Gridi(Grid):
    
    def __init__(self, animate=False, saveimg=False, resize=True, size=(50,84), **kw):
        super().__init__(**kw)
        self.i = 0                  # snapshot counter
        self.img = None             # snapshot image
        self.io = None              # snapshot io buffer
        self.animate = animate
        self.saveimg = saveimg
        self.resize = resize
        self.size = size

        
    # calling render__() directly is not a good idea for Gridi because s_() is calling it as well
    # calling render() allows us to turn animation/saveimg on/off
    def render(self, animate=None, saveimg=None, **kw):  
        if animate is not None: self.animate = animate 
        if saveimg is not None: self.saveimg = saveimg


    def render_image(self, saveimg):
       # prepare and scale the area that will be captured 
        if self.io is None: self.io = io.BytesIO()
        
        # scale = 0.0138888 # use this if you are using Jupyter notebooks
        scale = 0.01      # use this if you are using Jupyter Lab
        box = self.ax0.get_window_extent().transformed(mtransforms.Affine2D().scale(scale))
        
        # place frame in memory buffer then save to disk if you want
        plt.savefig(self.io, format='raw', bbox_inches=box)
        if saveimg or self.img is None:
            os.makedirs('img') if not os.path.exists('img') else None
            plt.savefig('img/img%d.png'%self.i, bbox_inches=box); self.i+=1 
            if self.img is None: 
                self.newshape = plt.imread('img/img0.png').shape
        #try:
        # reshape the image and store current image 
        self.img = np.reshape(np.frombuffer(self.io.getvalue(), dtype=np.uint8), newshape=self.newshape)[:,:,:3]
        #except:
            #self.img = np.frombuffer(self.io.getvalue(), dtype=np.uint8)[:,:,:3]
            #print('could not convert the image')
        if self.resize:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.img = cv2.resize(self.img , dsize=(self.size[1],self.size[0]), interpolation=cv2.INTER_CUBIC)/255
            self.img = np.expand_dims(self.img, -1)# slightly better than  self.img = self.img[:,:,np.newaxis]
        # save only latest image to buffer and not accumulate
        self.io.seek(0) 

        
    def s_(self):
        self.render__(image=True, animate=self.animate, saveimg=self.saveimg)#, animate=self.animate)
        return self.img

def play(env, steps=5):
    
    img = [env.s_()]*steps                                             # initialise and declare
    # img = np.ones((steps,*env.s_().shape),dtype=int);img[0]=env.s_() # more efficent for large steps
    for i in range(steps):
        img[i], reward, done,_ = env.step(randint(3))
        env.render()                                                   # makes no effect since s_() calls render()
    return img

def test():
    gw=Gridi()#animate=False)
    for s in range(100): 
        gw.step(1)
        gw.render(image=True, animate=True)

def test_efficiency(test, n=100):
    gw=Gridi()
    gw.s=gw.s0 # reset the agent position
    # let us go right
    for s in range(n):
        gw.step(1)
        if test==0: gw.render(image=True,  animate=True)
        if test==1: gw.render(image=False, animate=True)
        if test==2: gw.render(image=True,  animate=False)
        if test==3: gw.render(image=False, animate=False)
    
    return gw

#-------------------------------suitable for control------------------------------------------------
def grid(Grid=Grid, **kw):
    return Grid(gridsize=[8, 10], s0=31, goals=[36], **kw)

def grid8(Grid=Grid, **kw): 
    return grid(Grid=Grid, nA=8, **kw)

def windy(Grid=Grid,  **kw):
    return Grid(gridsize=[7, 10], s0=30, goals=[37], style='windy', **kw)

def cliffwalk(Grid=Grid, **kw):
    return Grid(gridsize=[4, 12], s0=0,  goals=[11], style='cliff', reward='cliffwalk', **kw)

def maze(Grid=Grid, r=6, c=9, **kw):
    return Grid(gridsize=[r,c], s0=r//2*c, goals=[r*c-1], style='maze', **kw)

def maze_large(Grid=Grid, **kw):
    return maze(Grid=Grid, r=16, c=26, figsize=[25,4],**kw)

def maze8(Grid=Grid, **kw): 
    return maze(Grid=Grid, nA=8, **kw)

def mazei(Grid=Gridi, r=6, c=9, **kw):
    return Gridi(gridsize=[r,c], s0=r//2*c, goals=[r*c-1], style='maze', **kw)#figsize is made ineffective

#-------------------------------suitable for prediction------------------------------------------------
def randwalk(Grid=Grid, nS=5+2, Vstar=None, **kw):
    if Vstar is None: Vstar = np.arange(0,nS)/(nS-1)
    return Grid(gridsize=(1,nS), reward='randwalk', nA=2, goals=[0,nS-1], s0=nS//2, Vstar=Vstar, **kw)


def randwalk_(Grid=Grid, nS=19+2, Vstar=None, **kw):
    if Vstar is None: Vstar = np.arange(-(nS-1),nS,2)/(nS-1)
    return Grid(gridsize=(1,nS), reward='randwalk_', nA=2, goals=[0,nS-1], s0=nS//2, Vstar=Vstar,**kw)