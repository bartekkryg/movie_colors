from threading import Thread
from queue import Queue
import cv2 as cv


class FileVideoStream:
    def __init__(self, path, queue_size=128):
        self.stream = cv.VideoCapture(path)
        self.stopped = False

        self.Q = Queue(maxsize=queue_size)

    def start(self):
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:

            if self.stopped:
                return

            if not self.Q.full():
                """
                grabbed = self.stream.grab()
                if grabbed:
                    time_s = self.stream.get(cv.CAP_PROP_POS_MSEC) / 500
                    if int(time_s) > int(prev_time):
                        frame = self.stream.retrieve()[1]
                        self.Q.put(frame)
                    prev_time = time_s
                """

                grabbed, frame = self.stream.read()

                if not grabbed:
                    self.stop()
                    return

                self.Q.put(frame)

    def read(self):
        return self.Q.get()

    def more(self):
        return self.Q.qsize() > 0

    def stop(self):
        self.stopped = True
