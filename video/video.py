#!/usr/bin/env python
import threading
import time

import cv2

from django.core.cache import cache


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
        self.frame_data = None

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_frame_from_cache(self):
        return cache.get('frame')

    def update(self):
        while True:
            time.sleep(1)
            (self.grabbed, self.frame) = self.video.read()
            ret, jpeg = cv2.imencode('.jpg', self.frame)
            data = jpeg.tobytes()
            now = time.time()
            cache.set('frame'.format(now), data, timeout=100)


cam = VideoCamera()


def generate_video():
    cap = cv2.VideoCapture(0)
    i = 0
    while True:
        ret, frame = cap.read()
        k = cv2.waitKey(1)
        if k == 27:
            break
        # elif k == ord('s'):
        cv2.imwrite('./static/images/' + str(i) + '.jpg', frame)
        i += 1
        # yield i, ret, frame
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        yield i
        cv2.imshow("capture", frame)
    cap.release()
    cv2.destroyAllWindows()


def main():
    for i in generate_video():
        print(i)
    pass


if __name__ == '__main__':
    main()
