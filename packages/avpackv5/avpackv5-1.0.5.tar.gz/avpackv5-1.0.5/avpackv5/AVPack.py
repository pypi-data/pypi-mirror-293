from random import *

class func:

    def __init__(self): ...
    def credits(): return f'AVPack with Functions by AVirus\nUses this projects: [random (random2)]'

    
    def FNC_token(self, t=32):
        ANSWR = ''
        for x in range(t):
            ANSWR += choice('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz')
        return ANSWR