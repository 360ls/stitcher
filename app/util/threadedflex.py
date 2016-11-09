""" Module responsible for demonstrating a threaded video feed flex. """

import threading
from .feed import VideoFeed





def main():
    stop_event = threading.Event()
    thread = threading.Thread(target=video_loop, args=())
    thread.start()

def video_loop():
    naive_video = VideoFeed("app/storage/naive_flex.mp4")
    

if __name__ == "__main__":
    main()