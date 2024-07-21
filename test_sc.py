from adbutils import adb
import scrcpy
import cv2 as cv
import time


class ScrcpyADB:
    def __init__(self):
        devices = adb.device_list()
        client = scrcpy.Client(device=devices[0])
        # You can also pass an ADBClient instance to it
        adb.connect("127.0.0.1:5555")
        print(devices, client)
        client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)
        client.start(threaded=True)
        self.client = client

        self.last_screen = None

    def on_frame(self, frame: cv.Mat):
        if frame is not None:
            self.last_screen = frame


    def touch_start(self, x: float, y: float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_DOWN)

    def touch_move(self, x: float, y: float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_MOVE)

    def touch_end(self, x: float, y: float):
        self.client.control.touch(int(x), int(y), scrcpy.ACTION_UP)

    def tap(self, x: float, y: float):
        self.touch_start(x, y)
        time.sleep(0.01)
        self.touch_end(x, y)


if __name__ == '__main__':
    sadb = ScrcpyADB()
    time.sleep(5)
    sadb.tap(1568 / 1.25, 166 / 1.25)
    time.sleep(999)