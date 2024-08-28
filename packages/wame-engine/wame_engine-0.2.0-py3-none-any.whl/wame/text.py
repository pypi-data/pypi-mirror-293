from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wame.scene import Scene

from wame.vector import IntVector2, IntVector3
from wame.render import Renderer

from OpenGL.GL import *

import pygame

class Text:
    '''UI Text'''

    def __init__(self, scene:'Scene', text:str, font:pygame.font.Font, color:IntVector3 | tuple[int, int, int]) -> None:
        '''
        Initialize a new text instance
        
        Parameters
        ----------
        scene : `wame.Scene`
            The scene to hook this instance to
        text : `str`
            The characters to be rendered
        font : `wame.Font`
            The font that is rendered
        color : `wame.IntVector3 | tuple[int, int, int]`
            The color of the text
        '''
        
        self._scene:'Scene' = scene

        self._font:pygame.font.Font = font
        self._text:str = text
        self._color:IntVector3 = color if isinstance(color, IntVector3) else IntVector3.from_tuple(color)
    
        self._textRender:pygame.Surface = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

        self._position:IntVector2 = None
    
    def render(self) -> None:
        '''
        Render the text to the screen
        
        Raises
        ------
        `ValueError`
            If the position was not set before rendering
        '''
        
        if self._position is None:
            error:str = "Position must be defined before the text can be rendered. Please use the Text.set_position() method"
            raise ValueError(error)

        if self._scene.engine._renderer == Renderer.PYGAME:
            self._scene.engine.screen.blit(self._textRender, self._position.to_tuple())
        else:
            screenHeight:int = self._scene.engine.screen.get_height()
            textHeight:int = self._textRender.get_height()

            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, self._scene.engine.screen.get_width(), 0, screenHeight, -1, 1)

            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            glRasterPos2d(self._position.x, screenHeight - self._position.y - textHeight)
            glDrawPixels(self._textRender.get_width(), textHeight, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(self._textRender, "RGBA", True))

            glDisable(GL_BLEND)

            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

    def set_color(self, color:IntVector3 | tuple[int, int, int]) -> None:
        '''
        Set the color of the text
        
        Parameters
        ----------
        color : `wame.IntVector3 | tuple[int, int, int]`
            The RGB values for the color
        '''

        if self._color == color:
            return

        self._color = color if isinstance(color, IntVector3) else IntVector3.from_tuple(color)

        self._textRender = self._font.render(self._text, self._scene.engine.settings.antialiasing, self._color.to_tuple())

    def set_position(self, position:IntVector2 | tuple[int, int]) -> None:
        '''
        Set the position of the text from the top left corner
        
        Parameters
        ----------
        position : `wame.IntVector2 | tuple[int, int]`
            The X, Y position values of the text
        '''
        
        self._position = position if isinstance(position, IntVector2) else IntVector2.from_tuple(position)
    
    def set_text(self, text:str) -> None:
        '''
        Set the text of the instance
        
        Parameters
        ----------
        text : `str`
            The characters to render
        '''
        
        self._text = text

        self._textRender = self._font.render(text, self._scene.engine.settings.antialiasing, self._color.to_tuple())