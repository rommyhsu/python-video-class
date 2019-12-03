# Video module
import ctypes
import datetime
import os
import queue
import sys
import time

import cv2
import numpy as np
import vlc
from PIL import Image

# 設置VLC庫路徑，需在import vlc之前
# os.environ['PYTHON_VLC_MODULE_PATH'] = "C:/Users/Rommy/python/vlc-3.0.6-win64"
# os.environ['PYTHON_VLC_MODULE_PATH'] = 'C:/Program Files/VideoLAN/VLC'
os.environ['PYTHON_VLC_MODULE_PATH'] = '../vlc-3.0.6-win64'

class Camera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.width = 640
        self.height = 480
        self.last_frame = np.zeros((1, 1))
        self.ifRun = True
        self.initFrame = None
        self.ret = False
        # self.frame_queue = queue.Queue()

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        self.get_capture_size()
        self.ret, self.initFrame = self.get_frame()
        self.ifRun = True

    def get_frame(self):
        self.ret, self.last_frame = self.cap.read()
        # self.frame_queue.put(self.last_frame)
        return self.ret, self.last_frame

    # def get_frames(self):
    #     ret, self.last_f

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            self.ret, frame = self.get_frame()
            movie.append(frame)
        return movie

    def acquire_movie(self):
        # movie = []
        # for _ in range(num_frames):
        #     movie.append(self.get_frame())
        while (self.ifRun):
            # movie.append(self.get_frame())
            self.ret, frame = self.get_frame()
            self.last_frame = frame
            if (self.ret != True):
                break
        # return movie

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

    def close_camera(self):
        self.ifRun = False
        self.cap.release()

    # decode fourcc
    def decode_fourcc(self):
        fourcc = self.cap.get(cv2.CAP_PROP_FOURCC)
        fourcc = int(fourcc)
        return 'codec:' + "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

    def get_capture_size(self):
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return "Image Size: %d x %d" % (self.width, self.height)

    def set_capture_size(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

class Video:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self.cap = None
        self.width = 640
        self.height = 480
        self.last_frame = np.zeros((1, 1))
        self.ifRun = True
        self.frames = 0
        # self.frame_queue = queue.Queue()
        self.initFrame = None
        self.ret = False
        self.ifCameraInitial = False
        self.ifLoop = False

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        self.get_capture_size()
        self.frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.ifRun = True
        # self.frame_queue = queue.Queue()
        self.ret, self.initFrame = self.get_frame()

    def get_frame(self):
        self.ret, _frame = self.cap.read()
        if self.ret:
            self.last_frame = cv2.resize(_frame, (640, 480))
            # cv2.waitKey(30)
            # self.frame_queue.put(self.last_frame)
            return self.ret, self.last_frame
        # if( ret == True):
        # cv2.waitKey(30)
        # self.last_frame = np.zeros((1, 1))
        return self.ret, self.last_frame

    # def get_frames(self):
    #     ret, self.last_f

    def acquire_movie(self, num_frames):
        movie = []
        for _ in range(num_frames):
            _ret, _frame = self.get_frame()
            if _ret:
                movie.append(_frame)

        return movie

    def acquire_movie(self):
        # movie = []
        # for _ in range(num_frames):
        #     movie.append(self.get_frame())
        # while (self.cap.get(cv2.CAP_PROP_POS_FRAMES) <= self.frames):
        #     # movie.append(self.get_frame())
        #     self.get_frame()
        # framerate = 10000
        # # frame_counter = 0
        # pretime = time.time()
        # next_time = pretime
        while self.ifRun:
            # movie.append(self.get_frame())
            # if(frame_counter % framerate == 0):
            if True:
                self.ret, _frame = self.get_frame()
                if not self.ret:
                    if self.ifLoop:

                        # self.ifRun = False
                        # self.last_frame = np.zeros((1, 1))
                        # self.frame_queue.put(self.last_frame)
                        print("movie rerun")
                        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 1)
                        continue
                    else:
                        self.ifRun = False
                        print("movie end")
                        self.cap.release()
                        break

                    # break
            # frame_counter+= 1
            time.sleep(0.030)
            # cv2.waitKey(1)
        # self.ifRun = False

        # if(self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.frames):
        # self.ifRun = False
        # self.last_frame = np.zeros((1, 1))
        # return movie

    def set_brightness(self, value):
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, value)

    def get_brightness(self):
        return self.cap.get(cv2.CAP_PROP_BRIGHTNESS)

    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)

    def close_camera(self):
        self.ifRun = False
        self.cap.release()

    # decode fourcc
    def decode_fourcc(self):
        fourcc = self.cap.get(cv2.CAP_PROP_FOURCC)
        fourcc = int(fourcc)
        return 'codec:' + "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

    def get_capture_size(self):
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        return "Image Size: %d x %d" % (self.width, self.height)

    def set_capture_size(self, width, height):
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

class IPcam:
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()

        self.frameQueue = queue.Queue(10)
        self.width = 640
        self.height = 480
        self.last_frame = np.zeros((1, 1))
        self.ifRun = True
        self.frames = 0
        self.initFrame = None
        self.ret = False
        self.ifCameraInitial = False
        self.ifLoop = False
        self.rtsp_url = ''
        self.CorrectVideoLockCb = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_void_p))

    '''
        args:設置 options
    '''

    def initialize(self, rtsp_url):
        self.rtsp_url = rtsp_url
        self.VIDEOWIDTH = 640
        self.VIDEOHEIGHT = 480

        # # size in bytes when RV32
        self.size = self.VIDEOWIDTH * self.VIDEOHEIGHT * 4
        # # allocate buffer
        self.buf = (ctypes.c_ubyte * self.size)()
        # # get pointer to buffer
        self.buf_p = ctypes.cast(self.buf, ctypes.c_void_p)

        self.video_set_format("BGRA", self.VIDEOWIDTH,
                              self.VIDEOHEIGHT, self.VIDEOWIDTH * 4)

    # 設置待播放的url地址或本地文件路徑，每次調用都會重新加載資源

    def set_uri(self, uri):
        self.media.set_mrl(uri)

    # 播放 成功返回0，失敗返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()

    # 暫停
    def pause(self):
        self.media.pause()

    # 恢復
    def resume(self):
        self.media.set_pause(0)

    # 停止
    def stop(self):
        self.media.stop()

    # 釋放資源
    def release(self):
        return self.media.release()

    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()

    # 已播放時間，返回毫秒值
    def get_time(self):
        return self.media.get_time()

    # 拖動指定的毫秒值處播放。成功返回0，失敗返回-1 (需要注意，只有當前多媒體格式或流媒體協議支持纔會生效)
    def set_time(self, ms):
        return self.media.get_time()

    # 音視頻總長度，返回毫秒值
    def get_length(self):
        return self.media.get_length()

    # 獲取當前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()

    # 設置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)

    # 返回當前狀態：正在播放；暫停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1

    # 當前播放進度情況。返回0.0~1.0之間的浮點數
    def get_position(self):
        return self.media.get_position()

    # 拖動當前進度，傳入0.0~1.0之間的浮點數(需要注意，只有當前多媒體格式或流媒體協議支持纔會生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)

    # 獲取當前文件播放速率
    def get_rate(self):
        return self.media.get_rate()

    # 設置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)

    # 設置寬高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必須設置爲0，否則無法修改屏幕寬高
        self.media.video_set_aspect_ratio(ratio)

    # 註冊監聽器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)

    # 移除監聽器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)

    def libvlc_video_set_callbacks(self, _lockcb, _display, _unLockcb=None, _opaque=None):
        vlc.libvlc_video_set_callbacks(
            self.media, _lockcb, _unLockcb, _display, None)

    def video_set_format(self, codec, videowidth, videoheight, datasize):
        self.media.video_set_format(codec, videowidth, videoheight, datasize)

    def enqueue(self, _frame):
        self.frameQueue.put(_frame)

    def dequeue(self):
        if not self.frameQueue.empty():
            return True, self.frameQueue.get()
        else:
            return False, None

    def get_frame(self):
        # _frame = self.last_frame
        # ret, _frame = self.dequeue()
        # ret, _frame = self.last_frame
        ret = self.is_playing()
        if ret:
            _frame = self.last_frame
            self.last_frame = cv2.resize(_frame, (640, 480))
            # cv2.waitKey(30)
            # self.frame_queue.put(self.last_frame)
            self.ret = True
            print("dequeue")
            return self.ret, self.last_frame
        # if( ret == True):
        # cv2.waitKey(30)
        # self.last_frame = np.zeros((1, 1))
        self.ret = False
        return self.ret, self.last_frame

    def acquire_movie(self, num_frames):
        pass

    def acquire_movie(self):
    #callback 存取 1 frame
        @self.CorrectVideoLockCb
        def _lockcb(opaque, planes):
            time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')
            # time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
            print("lock " + time_str, file=sys.stderr)
            planes[0] = self.buf_p

        @vlc.CallbackDecorators.VideoDisplayCb
        def _display(opaque, picture):
            if True:  # framenr % 24 == 0:
                # shouldn't do this here! copy buffer fast and process in our own thread, or maybe cycle
                # through a couple of buffers, passing one of them in _lockcb while we read from the other(s).
                img = Image.frombuffer(
                    "RGBA", (self.VIDEOWIDTH, self.VIDEOHEIGHT), self.buf, "raw", "BGRA", 0, 1)
                cv_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
                # cv2.putText(cv_img, "Time:" + str(time_str), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                #             cv2.LINE_AA)
                # self.enqueue(cv_img)
                self.last_frame = cv_img.copy()
                print('enqueue')
                self.get_frame()

        self.libvlc_video_set_callbacks(_lockcb, _display, None, None)
        self.play(self.rtsp_url)
        time.sleep(10)
        # print('Brightness:' + str(cam.get_brightness()))
        while True:
            # ret, frame = self.get_frame()
            # cv2.waitKey(30)

            if self.is_playing():
                cv2.waitKey(30)
            else:
                print('vlc end')
                self.ret = False
                break
            # if ret:
            #     # cv2.imshow('VideoSourceTest  ' + caminfo, frame)
            #     # cv2.imshow('IPcamSourceTest  ', frame)
            #     # print(frame)
            #     # if cv2.waitKey(30) & 0xFF == ord('q'):
            #     #     break
            # else:
            #     pass
        # cv2.destroyAllWindows()
        self.close_camera()

    def close_camera(self):
        self.ifRun = False
        self.stop()


def main():
    filename = "D:/movie/WIN_20191023_14_28_01_Pro.mp4"
    cam = Video(filename)
    cam.initialize()
    # cam.acquire_movie()
    # while(True):
    #     # if (cam.last_frame.Size ==1):
    #     #     break
    #
    #     cv2.imshow('VideoSourceTest  ', cam.last_frame)
    #     #         # print(frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cam.play(filename)
    # time.sleep(10)
    # cam = Camera(0)
    # cam.initialize()
    # cam.set_brightness(1)
    # print(cam.get_brightness())
    # cam.set_brightness(0.5)
    # print(cam.get_brightness())
    # print(cam)
    # print(cam.decode_fourcc())
    # camStr = str(cam.width) + 'x' + str(cam.height)
    # caminfo = camsource + '  ' + camdecode + '  ' + cam_size
    # caminfo = str(cam.__str__()) + '  ' + str(cam.decode_fourcc()) + '  ' + str(cam.get_capture_size())
    print('Brightness:' + str(cam.get_brightness()))
    while True:
        ret, frame = cam.get_frame()
        if ret:
            # cv2.imshow('VideoSourceTest  ' + caminfo, frame)
            cv2.imshow('VideoSourceTest  ', frame)
            # print(frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break

    cv2.destroyAllWindows()
    cam.close_camera()

def main_Webcam():
    cam = Camera(0)
    cam.initialize()
    print('Brightness:' + str(cam.get_brightness()))
    while True:
        ret, frame = cam.get_frame()
        if ret:
            # cv2.imshow('VideoSourceTest  ' + caminfo, frame)
            cv2.imshow('VideoSourceTest  ', frame)
            # print(frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            break
    cv2.destroyAllWindows()
    cam.close_camera()

def main_IPcam():
    rtsp_url = 'D:/movie/Pepper_short.mp4'
    IP_cam.initialize(rtsp_url)
    IP_cam.VIDEOWIDTH = 640
    IP_cam.VIDEOHEIGHT = 480
    IP_cam.play(rtsp_url)
    time.sleep(10)
    # print('Brightness:' + str(cam.get_brightness()))
    while True:
        ret, frame = IP_cam.get_frame()
        if ret:
            cv2.imshow('IPcamSourceTest  ', frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
        else:
            print('vlc end')
            break
    cv2.destroyAllWindows()
    IP_cam.close_camera()


# Unit Test
if __name__ == '__main__':
# mark
    # filename = "D:\movie\peper.mp4"
    # cam = Video(filename)
    # cam.initialize()
    # # cam.acquire_movie()
    # # while(True):
    # #     # if (cam.last_frame.Size ==1):
    # #     #     break
    # #
    # #     cv2.imshow('VideoSourceTest  ', cam.last_frame)
    # #     #         # print(frame)
    # #     if cv2.waitKey(1) & 0xFF == ord('q'):
    # #         break

    # # cam = Camera(0)
    # # cam.initialize()
    # # cam.set_brightness(1)
    # # print(cam.get_brightness())
    # # cam.set_brightness(0.5)
    # # print(cam.get_brightness())
    # # print(cam)
    # # print(cam.decode_fourcc())
    # # camStr = str(cam.width) + 'x' + str(cam.height)
    # # caminfo = camsource + '  ' + camdecode + '  ' + cam_size
    # # caminfo = str(cam.__str__()) + '  ' + str(cam.decode_fourcc()) + '  ' + str(cam.get_capture_size())
    # print('Brightness:' + str(cam.get_brightness()))
    # while True:
    #     ret, frame = cam.get_frame()
    #     if ret:
    #         # cv2.imshow('VideoSourceTest  ' + caminfo, frame)
    #         cv2.imshow('VideoSourceTest  ', frame)
    #         # print(frame)
    #         if cv2.waitKey(10) & 0xFF == ord('q'):
    #             break
    #     else:
    #         break
    # cv2.destroyAllWindows()
    # cam.close_camera()
    # main()
    # main_Webcam()
    # global cam

# mark
    global IP_cam
    IP_cam = IPcam()

    @IP_cam.CorrectVideoLockCb
    def _lockcb(opaque, planes):
        time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S.%f')
        # time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
        print("lock " + time_str, file=sys.stderr)
        planes[0] = IP_cam.buf_p

    @vlc.CallbackDecorators.VideoDisplayCb
    def _display(opaque, picture):
        if True:  # framenr % 24 == 0:
            # shouldn't do this here! copy buffer fast and process in our own thread, or maybe cycle
            # through a couple of buffers, passing one of them in _lockcb while we read from the other(s).
            img = Image.frombuffer(
                "RGBA", (IP_cam.VIDEOWIDTH, IP_cam.VIDEOHEIGHT), IP_cam.buf, "raw", "BGRA", 0, 1)
            cv_img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            # cv2.putText(cv_img, "Time:" + str(time_str), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
            #             cv2.LINE_AA)
            # IP_cam.enqueue(cv_img)
            IP_cam.last_frame = cv_img.copy()
            print('enqueue')

    IP_cam.libvlc_video_set_callbacks(_lockcb, _display, None, None)

    main_IPcam()
