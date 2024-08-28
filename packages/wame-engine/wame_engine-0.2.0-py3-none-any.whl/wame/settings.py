class Settings:
    '''Engine Global Settings'''

    def __init__(self, data:dict[str]) -> None:
        '''
        Initialize the engine settings
        
        Note
        ----
        This should only be instantiated by the engine internally.
        Avoid calling this yourself.
        
        Parameters
        ----------
        data : `dict[str, Any]`
            The raw settings contents from the known settings persistence file
        '''
        
        self._antialiasing:bool = data["antialiasing"] if "antialiasing" in data else True
        self._max_fps:int = data["max_fps"] if "max_fps" in data else 0
        self._tabbed_fps:int = data["tabbed_fps"] if "tabbed_fps" in data else 30
    
    @property
    def antialiasing(self) -> bool:
        '''If antialiasing should be enabled'''

        return self._antialiasing
    
    @antialiasing.setter
    def antialiasing(self, antialiasing:bool) -> None:
        self._antialiasing = antialiasing
    
    @property
    def max_fps(self) -> int:
        '''The maximum framerate allowed to be rendered'''

        return self._max_fps
    
    @max_fps.setter
    def max_fps(self, fps:int) -> None:
        self._max_fps = fps
    
    @property
    def tabbed_fps(self) -> int:
        '''The maximum framerate allowed to be rendered while the user is tabbed out of the engine'''

        return self._tabbed_fps

    @tabbed_fps.setter
    def tabbed_fps(self, fps:int) -> None:
        self._tabbed_fps = fps

    def export(self) -> dict[str]:
        '''
        Export the class instance to a raw, storable type
        
        Returns
        -------
        rawSettings : `dict[str, Any]`
            The raw class instance data
        '''
        
        return {
            "antialiasing": self._antialiasing,
            "max_fps": self._max_fps,
            "tabbed_fps": self._tabbed_fps
        }