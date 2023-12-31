# -*- coding: utf-8 -*-

import pygame
import base64
## local package import
from UI.full_screen import FullScreen
from UI.skin_manager import MySkinManager
from UI.createby_clockworkpi import createby_clockworkpi_b64

from UI.constants   import Width,Height

class CreateByScreen(FullScreen):

    _BG = None
    _BGColor = MySkinManager.GiveColor('Black')
    
    def Init(self):
        #self._BG = pygame.image.frombuffer(base64.b64decode(createby_clockworkpi_b64 ),(400,240),"P")
        self._CanvasHWND = pygame.Surface((self._Width,self._Height))
        
    
    def Draw(self):
        self._CanvasHWND.fill( self._BGColor )
        
        self._CanvasHWND.blit(self._BG,(0,0,Width,Height))
