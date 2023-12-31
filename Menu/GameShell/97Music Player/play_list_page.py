# -*- coding: utf-8 -*- 
import os
import pygame
import gobject

from libs.roundrects import aa_round_rect

## local UI import
from UI.constants import Width,Height,ICON_TYPES
from UI.page   import Page,PageSelector
from UI.icon_item import IconItem
from UI.label  import Label
from UI.util_funcs import midRect
from UI.keys_def   import CurKeys, IsKeyStartOrA, IsKeyMenuOrB
from UI.icon_pool  import MyIconPool
from UI.skin_manager import MySkinManager
from UI.lang_manager import MyLangManager

from UI.scroller   import ListScroller

from list_item  import ListItem

import Menu.GameShell.10Settings.myvars

class ListPageSelector(PageSelector):
    _BackgroundColor = MySkinManager.GiveColor('Front')

    def __init__(self):
        self._PosX = 0
        self._PosY = 0
        self._Height = 0
        self._Width  = Width 

    def AnimateDraw(self,x2,y2):
        pass

    def Draw(self):
        idx = self._Parent._PsIndex
        if idx > (len(self._Parent._MyList)-1):
            idx = len(self._Parent._MyList)
            if idx > 0:
                idx -=1
            elif idx == 0: #Nothing
                return

        x = self._Parent._MyList[idx]._PosX+2
        y = self._Parent._MyList[idx]._PosY+1
        h = self._Parent._MyList[idx]._Height -3
        
        self._PosX = x
        self._PosY = y
        self._Height = h

        aa_round_rect(self._Parent._CanvasHWND,  
                      (x,y,self._Width-4,h),self._BackgroundColor,4,0,self._BackgroundColor)
        


class PlayListPage(Page):

    _Icons = {}
    _Selector=None
    _FootMsg = ["Nav","Remove","RTA","Back","Play/Pause"]
    _MyList = []
    _ListFont = MyLangManager.TrFont("notosanscjk15")

    _Scroller = None
    _CurSongTime="0:0"
    
    _BGpng  = None
    _BGwidth = 75
    _BGheight = 70

    _Scrolled = 0

    _CurSongName = ""
    
    def __init__(self):
        self._Icons = {}
        Page.__init__(self)
        self._CanvasHWND = None
        self._MyList = []

    def SyncList(self):
        self._MyList = []
        start_x  = 0
        start_y  = 0
        if myvars.Poller == None:
            return
        
        play_list = myvars.Poller.playlist()
        for i,v in enumerate(play_list):
            li = ListItem()
            li._Parent = self
            li._PosX   = start_x
            li._PosY   = start_y + i*ListItem._Height
            li._Width  = Width
            li._Fonts["normal"] = self._ListFont

            if "title" in v:
                if isinstance(v["title"], (list,)):
                    li.Init(" | ".join(v["title"]))
                else:
                    li.Init( v["title"])
                
                if "file" in v:
                    li._Path = v["file"]
                
            elif "file" in v:
                li.Init(os.path.basename(v["file"]))
                li._Path = v["file"] 
            else:
                li.Init("NoName")

            li._Labels["Text"]._PosX = 7
            self._MyList.append(li)

            
        self.SyncPlaying()

    def GObjectInterval(self): ## 250 ms
        self.SyncPlaying()
        
        if self._Screen.CurPage() == self:
            self._Screen.Draw()
            self._Screen.SwapAndShow()
            
        return True
    
    def SyncPlaying(self):
        if myvars.Poller == None:
            return
        
        current_song = myvars.Poller.poll()
        
        
        for i ,v in enumerate(self._MyList):
            self._MyList[i]._Playing = False
            self._MyList[i]._PlayingProcess = 0
            
        if current_song != None:
            if "song" in current_song:
                posid = int(current_song["song"])
                if posid < len(self._MyList): # out of index
                    self._CurSongName = self._MyList[posid]._Text
                    
                    if "state" in current_song:
                        if current_song["state"] == "stop":
                            self._MyList[posid]._Playing = False
                        else:
                            self._MyList[posid]._Playing = True
                    if "time" in current_song:
                        self._CurSongTime = current_song["time"]
                        times_ = current_song["time"].split(":")
                        if len(times_)> 1:
                            cur = float(times_[0])
                            end = float(times_[1])
                            pros = int((cur/end)*100.0)
                            self._MyList[posid]._PlayingProcess = pros
                            
                
    def InPlayList(self,path):
        for i,v in enumerate(self._MyList):
            if v._Path == path:
                return True
    
    def Init(self):
        self._PosX = self._Index * self._Screen._Width
        self._Width = self._Screen._Width
        self._Height = self._Screen._Height

        self._CanvasHWND = self._Screen._CanvasHWND

        ps = ListPageSelector()
        ps._Parent = self
        self._Ps = ps
        self._PsIndex = 0

        self.SyncList()
        gobject.timeout_add(850,self.GObjectInterval)

        self._BGpng = IconItem()
        self._BGpng._ImgSurf = MyIconPool.GiveIconSurface("heart")
        self._BGpng._MyType = ICON_TYPES["STAT"]
        self._BGpng._Parent = self
        self._BGpng.AddLabel(MyLangManager.Tr("my favorite music"), MyLangManager.TrFont("varela18"))
        self._BGpng.SetLableColor(MySkinManager.GiveColor('Disabled'))
        self._BGpng.Adjust(0,0,self._BGwidth,self._BGheight,0)

        self._Scroller = ListScroller()
        self._Scroller._Parent = self
        self._Scroller._PosX = self._Width - 10
        self._Scroller._PosY = 2
        self._Scroller.Init()
        
        
    def ScrollUp(self):
        if len(self._MyList) == 0:
            return
        self._PsIndex -= 1
        if self._PsIndex < 0:
            self._PsIndex = 0
        cur_li = self._MyList[self._PsIndex]
        if cur_li._PosY < 0:
            for i in range(0, len(self._MyList)):
                self._MyList[i]._PosY += self._MyList[i]._Height
            self._Scrolled +=1

    def ScrollDown(self):
        if len(self._MyList) == 0:
            return
        self._PsIndex +=1
        if self._PsIndex >= len(self._MyList):
            self._PsIndex = len(self._MyList) -1

        cur_li = self._MyList[self._PsIndex]
        if cur_li._PosY +cur_li._Height > self._Height:
            for i in range(0,len(self._MyList)):
                self._MyList[i]._PosY -= self._MyList[i]._Height
            self._Scrolled -=1

    def SyncScroll(self):# show where it left
        if self._Scrolled == 0:
            return

        if self._PsIndex < len(self._MyList):
            cur_li = self._MyList[self._PsIndex]
            if self._Scrolled > 0:
                if cur_li._PosY < 0:
                    for i in range(0, len(self._MyList)):
                        self._MyList[i]._PosY += self._Scrolled * self._MyList[i]._Height
            elif self._Scrolled < 0:
                if cur_li._PosY +cur_li._Height > self._Height:
                    for i in range(0,len(self._MyList)):
                        self._MyList[i]._PosY += self._Scrolled * self._MyList[i]._Height
            
    def Click(self):
        self.RefreshPsIndex()
        if len(self._MyList) == 0:
            return
         
        cur_li = self._MyList[self._PsIndex]
        play_pos_id = myvars.Poller.play(self._PsIndex)

        self.SyncPlaying()

        self._Screen.Draw()
        self._Screen.SwapAndShow()
        
    def OnReturnBackCb(self): # return from music_lib_list_page
        self.SyncList()
        self.SyncScroll()
        
    def KeyDown(self,event):
        if IsKeyMenuOrB(event.key):
            if myvars.Poller != None:
                myvars.Poller.stop()
                self._CurSongTime=""
                self._CurSongName=""
            
            self.ReturnToUpLevelPage()
            self._Screen.Draw()
            self._Screen.SwapAndShow()
        
        if event.key == CurKeys["Up"]:
            self.ScrollUp()
            self._Screen.Draw()
            self._Screen.SwapAndShow()
        if event.key == CurKeys["Down"]:
            self.ScrollDown()
            self._Screen.Draw()
            self._Screen.SwapAndShow()
        
        if event.key == CurKeys["Right"]:#add
            self._Screen.PushCurPage()
            self._Screen.SetCurPage(myvars.MusicLibListPage)
            self._Screen.Draw()
            self._Screen.SwapAndShow()
        
        if event.key == CurKeys["Y"]:# del selected songs
            myvars.Poller.delete(self._PsIndex)
            self.SyncList()
            self._Screen.Draw()
            self._Screen.SwapAndShow()
            
        if IsKeyStartOrA(event.key):
            self.Click()

        if event.key == CurKeys["X"]: # start spectrum
            myvars.SpectrumPage._Neighbor = self
            self._Screen.PushPage(myvars.SpectrumPage)
            self._Screen.Draw()
            self._Screen.SwapAndShow()
            
    def Draw(self):
        self.ClearCanvas()

        if len(self._MyList) == 0:
            self._BGpng.NewCoord(self._Width/2,self._Height/2)
            self._BGpng.Draw()
            return
        else:
            if len(self._MyList) * ListItem._Height > self._Height:
                self._Ps._Width = self._Width - 11
                self._Ps.Draw()
                for i in self._MyList:
                    if i._PosY > self._Height + self._Height/2:
                        break

                    if i._PosY < 0:
                        continue
                    
                    i.Draw()
                self._Scroller.UpdateSize( len(self._MyList)*ListItem._Height, self._PsIndex*ListItem._Height)
                self._Scroller.Draw()
            else:
                self._Ps._Width = self._Width
                self._Ps.Draw()
                for i in self._MyList:
                    
                    if i._PosY > self._Height + self._Height/2:
                        break

                    if i._PosY < 0:
                        continue
                    
                    i.Draw()
                
