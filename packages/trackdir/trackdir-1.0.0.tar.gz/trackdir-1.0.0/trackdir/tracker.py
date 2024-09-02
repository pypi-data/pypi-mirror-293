import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_event = None
        self.change_info = None

    def on_any_event(self, event):
        current_event = (event.event_type, event.src_path)
        if current_event != self.last_event:
            self.last_event = current_event
            self.change_info = {"type": event.event_type, "path": event.src_path}

def track_changes(directory, verbose=False):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    if verbose:
        print(f"Tracking changes in : {directory}")

    try:
        while True:
            time.sleep(1)
            if event_handler.change_info:
                if verbose:
                    event_type = event_handler.change_info["type"]
                    event_path = event_handler.change_info["path"]
                    if event_type == 'modified':
                        print(f"File modified : {event_path}")
                    elif event_type == 'created':
                        print(f"File created : {event_path}")
                    elif event_type == 'deleted':
                        print(f"File deleted : {event_path}")
                return event_handler.change_info  
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    return None  

def main():
    if len(sys.argv) != 2:
        print("Usage : trackdir <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    track_changes(directory, verbose=True)

if __name__ == "__main__":
    main()
