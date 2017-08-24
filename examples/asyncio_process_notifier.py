import pyinotify
import asyncio
import sys 


import psutil
import time


class HandleEvent(pyinotify.ProcessEvent):
    def my_init(self):
        self.known = set([x for x in psutil.process_iter()])
        return None

    def process_default(self, event):
        latest = set([x for x in psutil.process_iter()])
        if len(latest-self.known) > 0:
            for proc in latest-self.known:
                try:
                    print(proc.parent(), 'spawned', proc.exe(), 'at', proc.pid)
                except psutil.NoSuchProcess:
                    print('process exited')
            self.known = latest
        else:
            print("something happened but wasn't represented by psutil (transient process)")                                                                                                                                                   

wm = pyinotify.WatchManager()
loop = asyncio.get_event_loop()
notifier = pyinotify.AsyncioNotifier(wm, loop, callback=None, default_proc_fun=HandleEvent())
wm.add_watch('/lib/ld-linux*', pyinotify.IN_ACCESS, do_glob=True)
loop.run_forever()
notifier.stop()
