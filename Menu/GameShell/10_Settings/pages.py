# -*- coding: utf-8 -*- 

from list_page import ListPage

import Menu.GameShell.10_Settings.myvars

def InitListPage(main_screen):

    myvars.ListPage = ListPage()
    
    myvars.ListPage._Screen = main_screen
    myvars.ListPage._Name = "Setting List"
    myvars.ListPage.Init()
