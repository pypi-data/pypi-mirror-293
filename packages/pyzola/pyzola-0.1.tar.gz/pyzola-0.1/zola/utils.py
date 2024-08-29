from zola.tools import (
    set_dump,
    set_path,
)

class Zencode(object):
    def __init__(self,source_code:str) -> None:
        
        self.source_code=source_code


    def save(self,path:str='file.path+file.name') -> None:
        set_path(path)
        open(path,'w').write('from zola.loads import *\nrunme(__file__)\n')
        set_dump(self.source_code,path)

