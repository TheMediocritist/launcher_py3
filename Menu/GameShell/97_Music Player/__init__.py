# -*- coding: utf-8 -*- 

import pygame

## local UI import
import Menu.GameShell.10_Settings.pages
import Menu.GameShell.10_Settings.myvars

def Init(main_screen):
    pages.InitPoller()

    pages.InitListPage(main_screen)
    pages.InitMusicLibPage(main_screen)
    pages.InitSpectrumPage(main_screen)
    
def API(main_screen):
    
    if main_screen !=None:
        main_screen.PushCurPage()
        main_screen.SetCurPage(myvars.PlayListPage)
        main_screen.Draw()
        main_screen.SwapAndShow()


