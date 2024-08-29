from sys import platform
from os.path import exists
    
def set_path(path:str):
    
    try:
        exists(path)       
        
    except Exception as e:
        print(e)


def set_dump(code:str,path:str='') -> None:
    try:
        cd=bytes(code.encode()).hex()
        with open(path,'a') as file:
            file.write(str(chr(34))+cd+str(chr(34)))
    except:
        print('erorr')



