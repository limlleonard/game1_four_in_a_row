import pygame as pg
import random
import numpy as np
import time
R=6
C=7
W=4
SQ=80
def line1(l1,n=4,c=1): # number in a line, color of player
  cnt=0
  def cw(l4): # check window
    if list(l4).count(c)==n and list(l4).count(0)==W-n:
      return True # and the rest is empty
  for k1 in range(R): # win horizontal
    for k2 in range(C-W+1):
      if cw(l1[k1,k2:k2+W]): cnt+=1
  for k1 in range(R-W+1): # win vertical
    for k2 in range(C):
      if cw(l1[k1:k1+W,k2]): cnt+=1
  for k1 in range(R-W+1): # diagnol
    for k2 in range(C-W+1):
      lt1=[] #list temp 1
      lt2=[]
      for k3 in range(W):
        lt1.append(l1[k1+k3,k2+k3])
        lt2.append(l1[k1+W-k3-1,k2+k3])
      if cw(lt1): cnt+=1
      if cw(lt2): cnt+=1
  return cnt
def moveb(l1,pos,c):
  for k1 in range(R):
    if not l1[R-k1-1][pos]:
      #check from the bottom row, if it is empty
      l1[R-k1-1][pos]=c # drop the piece to the bottom
      return True #move success
  return False
class Robot():
  def __init__(self,c):
    self.c=c # color
    self.l1=[]
    self.mp=[]
  def score1(self,l1,i,c):
    lt=l1.copy()
    moveb(lt,i,c)
    i4=line1(lt,4,c) #i would get a 4
    i3=line1(lt,3,c)
    i2=line1(lt,2,c)
    lt=l1.copy()    
    moveb(lt,i,c%2+1) # fantacy move by opponent
    y4=line1(lt,4,c%2+1)
    y3=line1(lt,3,c%2+1)
    y2=line1(lt,2,c%2+1)
    return i4*10**4+y4*10**3+i3*10**2+y3*10+i2*5+y2*2
  def scores(self,l1,c):
    dict1={}
    for i in range(C):
      if l1[0][i]==0:
        dict1[i]=self.score1(l1,i,c)
    return dict1
  def mover(self,l1,_=0): #move random
    # it takes a parameter it doesn't need, because human mover need this parameter
    dict1=self.scores(l1.copy(),self.c)
    print(dict1)
    for k in dict1:
      l2=l1.copy()
      moveb(l2,k,self.c) # make fantacy move myself, to calculate opponent
      dict2=self.scores(l2,self.c%2+1)
      dict1[k]-=max(dict2.values())//2
    print(dict1)
    if -5<max(dict1.values())<5:
      return random.randint(0,C-1)
    return max(dict1, key=dict1.get)
class Human():
  def __init__(self,c):
    self.c=c
  def mover(self,_,a1): # human doesn't need the list
    return a1 #just return the number you get
class Game():
  def __init__(self,a1):
    if a1==1:
      self.p1=Human(1)
      self.p2=Human(2)
    elif a1==2:
      self.p1=Human(1)
      self.p2=Robot(2)
    elif a1==3:
      self.p1=Robot(1)
      self.p2=Human(2)
    elif a1==4:
      self.p1=Robot(1)
      self.p2=Robot(2)
    self.l1=np.zeros((R,C),dtype=int)
    self.p1v=self.p2v=self.turn=True #valid move
  def move1(self,a1=7):
    if self.turn:
      mt=self.p1.mover(self.l1,a1)
      if mt in range(C):
        self.p1v=moveb(self.l1,mt,self.p1.c)
        self.turn=not self.turn # only switch, if make a valid move
    else:
      mt=self.p2.mover(self.l1,a1)
      if mt in range(C):
        self.p2v=moveb(self.l1,mt,self.p2.c)
        self.turn=not self.turn
  def winc(self):
    r1=line1(self.l1,W,1)
    r2=line1(self.l1,W,2)
    #time.sleep(1)
    if r1>0 or not self.p2v:
      print(r1)
      print(self.p2v)
      return 'P1 wins'
    elif r2>0 or not self.p1v:
      print(r2)
      print(self.p1v)
      return 'P2 wins'
    elif np.count_nonzero(self.l1==0)==0: return 'Tie'
    else: return False
go=True
ns={pg.K_0:0, pg.K_1:1, pg.K_2:2, pg.K_3:3, pg.K_4:4, pg.K_5:5, pg.K_6:6}
text1='1: human vs human  2: human vs robot'
text2='3: robot vs human  4: robot vs robot'
clock = pg.time.Clock()
pg.init()
pg.display.set_caption('Four in a row')
screen = pg.display.set_mode((SQ*C, SQ*(R+1)))
stage=1
while go:
  clock.tick(40)
  screen.fill((0,0,0))
  if stage==2:
    wc=g1.winc()
    if wc: stage=3
    else: g1.move1()
  for e in pg.event.get():
    if e.type == pg.QUIT: go = False
    if e.type == pg.KEYDOWN and e.key in ns:
      a1=ns[e.key]
      if stage==1 and ns[e.key] in range(1,5):
        g1=Game(ns[e.key])
        stage=2
      elif stage==2:
        g1.move1(ns[e.key])
      elif stage==3:
        if ns[e.key]==0: go=False
        elif ns[e.key]==1: stage=1
    elif e.type==pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
      if stage==2:
        mx, my = pg.mouse.get_pos()
        g1.move1(mx//SQ)
      pass
  for x in range(C): #Brett
    for y in range(R):
      pg.draw.circle(screen, '#CDC0B4', (x*SQ+SQ//2, y*SQ+SQ//2),SQ//3,4)
      if stage>1: #still shows the result 
        if g1.l1[y][x]==1:
          pg.draw.circle(screen,(200,0,0),(x*SQ+SQ//2, y*SQ+SQ//2),SQ//3)
        if g1.l1[y][x]==2:
          pg.draw.circle(screen,(0,200,200),(x*SQ+SQ//2,y*SQ+SQ//2),SQ//3)
  if stage==1:
    guide1=pg.font.SysFont('Arial',30).render(text1,False,(0,255,0))
    screen.blit(guide1,(SQ//4,SQ*R))
    guide1=pg.font.SysFont('Arial',30).render(text2,False,(0,255,0))
    screen.blit(guide1,(SQ//4,SQ*R+SQ//2))
  elif stage==2:
    pass
  elif stage==3:
    guide1=pg.font.SysFont('Arial',30).render(wc,False,(0,255,0))
    screen.blit(guide1,(SQ//4,SQ*R))
    guide1=pg.font.SysFont('Arial',30).render('Again?(0/1)',False,(0,255,0))
    screen.blit(guide1,(SQ//4,SQ*R+SQ//2))
  pg.display.flip()
  