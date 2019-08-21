import sys
import os
import time
import logging
from utils.log import log
from makingsystem.settings import config
from .uploadaliyun import Xfer
log.initLogConf()
LOG = logging.getLogger(__file__)


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):

    def __init__(self):
        self.xfer = Xfer()

    def on_any_event(self, event):
        if event.is_directory:
            is_d = 'directory'
        else:
            is_d = 'file'
        log_s = f'{event.event_type, is_d, event.src_path}'
        LOG.info(log_s)

    def on_created(self, event):
        if event.is_directory:
            return
        self.xfer.upload(event.src_path)

    def on_modified(self, event):
        self.on_created(event)

    def on_deleted(self, event):
        pass

    def on_moved(self, event):
        pass


if __name__ == "__main__":
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = "."
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
