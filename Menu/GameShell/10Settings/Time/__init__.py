# -*- coding: utf-8 -*- 

import pygame

## local UI import
import Menu.GameShell.10Settings.pages
import Menu.GameShell.10Settings.myvars

def Init(main_screen):
    pages.InitTimezoneListPage(main_screen)
    
def API(main_screen):
    if main_screen !=None:
        main_screen.PushCurPage()
        main_screen.SetCurPage(myvars.TimezoneListPage)
        main_screen.Draw()
        main_screen.SwapAndShow()


