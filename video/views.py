from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

from video.video import VideoCamera


def hello():
    import time
    i = 0
    while True:
        time.sleep(1)
        yield f'Hello,{i}'


cam = VideoCamera()


def gen():
    """

    :return:
    """
    i = 0
    while True:
        frame = cam.get_frame()
        if i >= 10:
            break
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def video_feed(request):
    print('request:{}'.format(request))
    try:
        return StreamingHttpResponse(
            gen(),
            content_type="multipart/x-mixed-replace;boundary=frame"
        )
    except Exception as e:
        print(e)


def video_index(request):
    return render(request, 'video/index.html', {
    })

