import threading

from pyparsing import Iterable



wildMutex = threading.Lock()

def mutexify_ButAllowUIUpdates(action, args):
    """Prevents other UI actions from happening until the action is completed, but allows the UI to redraw."""  
    #Take no action if another thread is already taking an action 
    # #(don't want to go backward and forward at the same time, but do want UI to keep drawing)
    if not wildMutex.acquire(blocking=False):
        return 

    #This needs to thread and return, so that the UI can continue updating. 
    # Otherwise the app will freeze between rapid clicks and not show photo updates or flash icons
    thread = threading.Thread(target=_takeActionThenRelease,args=[action, args])
    thread.start()

def _takeActionThenRelease(action, args):
    t = threading.Thread(target=action, args=args)
    t.run()
    wildMutex.release()