from random import *
from pyautogui import * # type: ignore
from time import *

class func:

    def credits(): return f'AVPack with Functions by AVirus\nUses this projects: [random (random2)]'

    
    def FNC_token(t:int=32):
        ANSWR = ''
        for x in range(t):
            ANSWR += choice('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz')
        return ANSWR
    
    def FNC_sendMsg(m:list=["yo"]):
        typewrite(choice(m).strip())
        press('enter')