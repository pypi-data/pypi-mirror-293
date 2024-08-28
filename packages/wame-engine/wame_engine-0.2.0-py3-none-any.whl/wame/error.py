class RendererNotRecognized(Exception):
    '''Raised when an engine tries to run with a set renderer that does not exist or is not recognized'''
    ...

class RendererNotSet(Exception):
    '''Raised when an engine tries to run without a renderer set/configured'''
    ...

class SceneAlreadyExists(Exception):
    '''Raised when an engine tries to register a scene when the scene name already exists'''
    ...

class SceneAlreadySet(Exception):
    '''Raised when an engine tries to set a scene that is already used by the engine'''
    ...

class SceneFolderNotFound(Exception):
    '''Raised when an engine tries to register scenes in a folder that does not exist or the path destination is not a folder'''
    ...

class SceneNotFound(Exception):
    '''Raised when an engine tries to access a scene that does not exist'''
    ...

class SceneNotSet(Exception):
    '''Raised when an engine tries to run without a scene set/configured'''
    ...