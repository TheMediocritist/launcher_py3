# -*- coding: utf-8 -*- 

## local UI import
import Menu.GameShell.10_Settings.pages
import Menu.GameShell.10_Settings.myvars

def Init(main_screen):
    pages.InitSoundPage(main_screen)

def API(main_screen):
    
    if main_screen !=None:
        main_screen.PushCurPage()
        main_screen.SetCurPage(myvars.SoundPage)
        main_screen.Draw()
        main_screen.SwapAndShow()
        
