from argparse import ArgumentParser
from typing import Optional, Tuple

from adbutils import adb
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QObject, Signal, QThread

import threading
import scrcpy
import sys, os
import json
import numpy as np
import time

import torch
from Ui_main import Ui_MainWindow

from yolo import YOLOv8

from control import ScrcpyControl
from game import GameAgent

import cv2

# os.environ["QT_DEBUG_PLUGINS"] = "1"

if not QApplication.instance():
    app = QApplication([])
else:
    app = QApplication.instance()


default_touch_map = {
        "pad_center":(430,965),


        "attack":(0,0),

        "buff_0":(0,0),
        "buff_1":(0,0),
        "buff_2":(0,0),
        "buff_3":(0,0),
        "buff_4":(0,0),

        "skill_0":(0,0),
        "skill_1":(0,0),
        "skill_2":(0,0),
        "skill_3":(0,0),
        "skill_4":(0,0),
        "skill_5":(0,0),
        "skill_6":(0,0),
        "skill_7":(0,0),
        "skill_8":(0,0),
        "skill_9":(0,0),

        "sp_0":(0,0),

        "options_0":(0,0),
        "options_1":(0,0),
        "options_2":(0,0),
        "options_3":(0,0),
        "options_4":(0,0),
        "options_5":(0,0),
        }

default_config = {
    'touch_map': default_touch_map
}


def create_default_config(filename):
    with open(filename, 'w') as configfile:
        json.dump(default_config, configfile, indent=4)

def read_config(filename, logger):
    if not os.path.exists(filename):
        create_default_config(filename)
        logger(f"默认配置文件 '{filename}' 已创建")
    
    with open(filename, 'r') as configfile:
        config = json.load(configfile)
        logger(f"已读取配置文件 '{filename}'")

    for key, value in config.items():
        logger((key, value))


    return config

class ControlVariable(QObject):
    valueChanged = Signal(str)

    def __init__(self, value=''):
        super().__init__()
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self.valueChanged.emit(self._value)


class Logger:
    def __init__(self, text_edit):
        self.text_edit = text_edit
        self.console = sys.stdout

    def __call__(self, message):
        message = str(message) + "\n"
        self.console.write(message)
        if message != '\n':
            self.text_edit.append(message)

    def flush(self):
        self.console.flush()
        self.text_edit.clear()



class DetectionWorker(QObject):
    finished = Signal()


    def __init__(self, model:YOLOv8, frame, window):
        super().__init__()

        # ptr = image.bits()
        # arr = np.array(ptr).reshape(frame.shape[1], frame.shape[0], 3)
        self.model = model
        self.image = frame
        self.window = window
        self._running = True
        # self.logger = logger


    def run(self):
        # TODO 控件绑定变量不起作用
        start = time.time()
        boxes, scores, class_ids = self.model(self.image)

        # cls_object = self.window.game.get_cls_name(class_ids)
        # self.window.class_ids.var = cls_object
        # self.window.boxes.var = boxes

        # self.game.main_loop(self.boxes.var, cls_object)
        info = f"[{boxes}]:  detection cost {(time.time()-start) * 1000} ms"

        # self.window.frame_time.var = info
        print(info)

        # self.window.output_image = self.model.draw_detections(self.image)

        # self.window.busy = False

        self.finished.emit()

    def stop(self):
        self._running = False



class MainWindow(QMainWindow):
    def __init__(
        self,
        max_width: Optional[int],
        serial: Optional[str] = None,
        encoder_name: Optional[str] = None,
    ):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.max_width = max_width

        self.logger = Logger(self.ui.textEdit)

        
        self.config = read_config("config.json", self.logger)
        self.touch_map = self.config["touch_map"]
        # print(self.touch_map)

        self.model = YOLOv8("best.onnx", conf_thres=0.3)
        self.busy = False


        # Setup devices
        self.devices = self.list_devices()
        if serial:
            self.choose_device(serial)
        self.device = adb.device(serial=self.ui.combo_device.currentText())
        self.alive = True

        # Setup client
        self.client = scrcpy.Client(
            device=self.device,
            flip=self.ui.flip.isChecked(),
            encoder_name=encoder_name,
        )
        self.client.add_listener(scrcpy.EVENT_INIT, self.on_init)
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)


        self.control = ScrcpyControl(self)
        self.game = GameAgent(self.touch_map, self.control)
        self.worker = None
        self.output_image = None
        self.paused = False

        # 检测结果
        self.boxes = ControlVariable([])
        self.class_ids = ControlVariable([])
        self.frame_time = ControlVariable("")


        self.boxes.valueChanged.connect(self.ui.label_info1.setText)
        self.class_ids.valueChanged.connect(self.ui.label_info2.setText)
        self.frame_time.valueChanged.connect(self.ui.label_fps.setText)





        # Bind controllers
        self.ui.button_home.clicked.connect(self.on_click_home)
        self.ui.button_back.clicked.connect(self.on_click_back)
        self.ui.button_test_move.clicked.connect(self.on_click_test_move)
        self.ui.button_test_stop.clicked.connect(self.on_click_test_stop)

        self.ui.button_start.clicked.connect(self.on_click_start)
        self.ui.button_stop.clicked.connect(self.on_click_stop)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # Keyboard event
        self.keyPressEvent = self.on_key_event(scrcpy.ACTION_DOWN)
        self.keyReleaseEvent = self.on_key_event(scrcpy.ACTION_UP)


    def choose_device(self, device):
        if device not in self.devices:
            msgBox = QMessageBox()
            msgBox.setText(f"Device serial [{device}] not found!")
            msgBox.exec()
            return

        # Ensure text
        self.ui.combo_device.setCurrentText(device)
        # Restart service
        if getattr(self, "client", None):
            self.client.stop()
            self.client.device = adb.device(serial=device)

    def list_devices(self):
        self.ui.combo_device.clear()
        items = [i.serial for i in adb.device_list()]
        self.ui.combo_device.addItems(items)
        return items

    def on_flip(self, _):
        self.client.flip = self.ui.flip.isChecked()

    def on_click_home(self):
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_DOWN)
        self.client.control.keycode(scrcpy.KEYCODE_HOME, scrcpy.ACTION_UP)

    def on_click_back(self):
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_DOWN)
        self.client.control.back_or_turn_screen_on(scrcpy.ACTION_UP)

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            if focused_widget is not None:
                focused_widget.clearFocus()
            ratio = self.max_width / max(self.client.resolution)
            self.client.control.touch(
                evt.position().x() / ratio, evt.position().y() / ratio, action
            )

        return handler

    def on_click_test_move(self):
        self.control.direction_move("UP")


    def on_click_test_stop(self):
        centerx, centery = self.touch_map["pad_center"]

        self.control.touch_end(centerx, centery)
                
        


    def on_key_event(self, action=scrcpy.ACTION_DOWN):
        def handler(evt: QKeyEvent):
            code = self.map_code(evt.key())
            if code != -1:
                self.client.control.keycode(code, action)

        return handler

    def map_code(self, code):
        """
        Map qt keycode ti android keycode

        Args:
            code: qt keycode
            android keycode, -1 if not founded
        """

        if code == -1:
            return -1
        if 48 <= code <= 57:
            return code - 48 + 7
        if 65 <= code <= 90:
            return code - 65 + 29
        if 97 <= code <= 122:
            return code - 97 + 29

        hard_code = {
            32: scrcpy.KEYCODE_SPACE,
            16777219: scrcpy.KEYCODE_DEL,
            16777248: scrcpy.KEYCODE_SHIFT_LEFT,
            16777220: scrcpy.KEYCODE_ENTER,
            16777217: scrcpy.KEYCODE_TAB,
            16777249: scrcpy.KEYCODE_CTRL_LEFT,
        }
        if code in hard_code:
            return hard_code[code]

        self.logger(f"Unknown keycode: {code}")
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")

    def start_detect(self, frame):

        self.worker = DetectionWorker(self.model, frame, self)
        self.worker_thread = threading.Thread(target=self.worker.run)

        self.worker.finished.connect(self.on_worker_finished)

        self.worker_thread.start()

    def on_worker_finished(self):
        self.busy = False




    def on_click_start(self):
        self.paused = False

    def on_click_stop(self):
        self.paused = True



    def on_frame(self, frame, fx=0.4, fy=0.4):
        app.processEvents()
        if frame is not None:
            self.game.frame += 1
            shape = frame.shape[0],frame.shape[1]

            ratio = self.max_width / max(self.client.resolution)
            if not self.paused:

                frame = cv2.resize(frame, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)

                if not self.busy and self.game.frame // self.game.frame_freq:
                    self.busy = True
                    self.start_detect(frame)

                if len(self.model.boxes) > 0:
                    frame = self.model.draw_detections(frame)

                frame = cv2.resize(frame, (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)

            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )


            # self.output_image = self.model.draw_detections(frame)

            # output_image = QImage(
            #     output_image,
            #     frame.shape[1],
            #     frame.shape[0],
            #     frame.shape[1] * 3,
            #     QImage.Format_BGR888,
            # )


            # pix = QPixmap(output_image)
            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / ratio)
            self.ui.label.setPixmap(pix)
            self.resize(1, 1)

    def closeEvent(self, _):
        self.client.stop()
        self.alive = False



def main():
    parser = ArgumentParser(description="A simple scrcpy client")
    parser.add_argument(
        "-m",
        "--max_width",
        type=int,
        default=900,
        help="Set max width of the window, default 800",
    )
    parser.add_argument(
        "-d",
        "--device",
        type=str,
        help="Select device manually (device serial required)",
    )
    parser.add_argument("--encoder_name", type=str, help="Encoder name to use")
    args = parser.parse_args()

    m = MainWindow(args.max_width, args.device, args.encoder_name)
    m.show()

    m.client.start()


if __name__ == "__main__":
    main()
