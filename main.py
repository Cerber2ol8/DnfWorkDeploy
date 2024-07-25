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

from Ui_main import Ui_MainWindow

os.environ['YOLO_VERBOSE'] = "false"
# import torch
from yolo import YOLOv8

from check_cuda import check_cuda_available
check_cuda_available()

from yolo import draw_detections, class_names
from ultralytics import YOLO
from control import ScrcpyControl
from game import GameAgent

import cv2


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

def read_config(filename):
    if not os.path.exists(filename):
        create_default_config(filename)
        print(f"默认配置文件 '{filename}' 已创建")
    
    with open(filename, 'r') as configfile:
        config = json.load(configfile)
        print(f"已读取配置文件 '{filename}'")

    for key, value in config.items():
        print(key, value)


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

class PrintLogger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        if message != '\n':
            self.text_edit.append(message)

    def flush(self):
        pass

class DetectionWorker(QObject):
    # finished = Signal()
    # bbox = Signal(list)
    # class_ids = Signal(list)
    ret = Signal(dict)

    def __init__(self, model, frame, window):
        super().__init__()

        self.model = model
        self.image = frame
        # self.window = window
        self._running = True

    def run(self):
        # TODO 控件绑定变量不起作用
        start = time.time()
        # _boxes, _scores, _class_ids = self.model(self.image)
        result = self.model(self.image)[0]
        # Process results list

        _boxes = result.boxes.xyxy.cpu().numpy()  # Boxes object for bounding box outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        # keypoints = result.keypoints  # Keypoints object for pose outputs
        _scores = result.boxes.conf.cpu().numpy()  # Probs object for classification outputs
        # obb = result.obb  # Oriented boxes object for OBB outputs
        _class_ids = result.boxes.cls.cpu().tolist()
        _class_ids = [int(value) for value in _class_ids]







        _time = time.time() - start

        ret_dict = {
            "start_time": start,
            "bbox": _boxes,
            "scores": _scores,
            "class_ids": _class_ids,
            "cost_time": _time
        }

        self.ret.emit(ret_dict)

        # self.bbox.emit(_boxes)
        # self.class_ids.emit(_class_ids)

        # self.window.busy = False

        # cls_object = self.window.game.get_cls_name(class_ids)
        # self.window.class_ids.var = cls_object
        # self.window.boxes.var = boxes

        # self.game.main_loop(self.boxes.var, cls_object)
        # info = f"[{cls_object, boxes}]:  detection cost {(time.time()-start) * 1000} ms"
        # self.finished.emit()

        # self.window.frame_time.var = info
        # print(info)

        # self.window.output_image = self.model.draw_detections(self.image)
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
        # 重定向print输出
        sys.stdout = PrintLogger(self.ui.textEdit)
        # sys.stderr = PrintLogger(self.ui.textEdit)

        self.config_file = "config.json"

        self.config = read_config(self.config_file)
        self.touch_map = self.config["touch_map"]

        self.test_config = None
        # print(self.touch_map)

        # self.model = YOLOv8("best.onnx", conf_thres=0.05)
        self.model = YOLO("best.onnx")
        self.model("test.png")
        self.bbox = []
        self.scores = []
        self.class_ids = []
        self.busy = False
        self.frame_time = ""
        self.info = ""


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
            max_fps=30
        )
        self.client.add_listener(scrcpy.EVENT_INIT, self.on_init)
        self.client.add_listener(scrcpy.EVENT_FRAME, self.on_frame)


        self.control = ScrcpyControl(self) 
        # TODO 添加控件输入
        self.game = GameAgent(self.touch_map, self.control, 15, "shanji", "maps/shanji", 10)
        self.worker = None
        self.output_image = None
        self.paused = True

        self.show_cursor = False







        # Bind controllers
        self.ui.button_reload.clicked.connect(self.on_click_reload_config)
        self.ui.button_back.clicked.connect(self.on_click_back)
        self.ui.button_move_up.clicked.connect(self.on_click_move_up)
        self.ui.button_move_down.clicked.connect(self.on_click_move_down)
        self.ui.button_move_left.clicked.connect(self.on_click_move_left)
        self.ui.button_move_right.clicked.connect(self.on_click_move_right)
        self.ui.button_move_stop.clicked.connect(self.on_click_test_stop)

        self.ui.button_cursor.clicked.connect(self.on_click_show_cursor)
        self.ui.button_test_skill.clicked.connect(self.on_click_test_skill)
        self.ui.button_attack.clicked.connect(self.on_click_attack)

        self.ui.button_start.clicked.connect(self.on_click_start)
        self.ui.button_stop.clicked.connect(self.on_click_stop)

        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        self.mouse_down = False

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

    def on_click_attack(self):
        self.game.normal_attack()

    def on_mouse_event(self, action=scrcpy.ACTION_DOWN):

        def handler(evt: QMouseEvent):
            focused_widget = QApplication.focusWidget()
            widget = focused_widget is not None

            ratio = self.max_width / max(self.client.resolution)
            px, py = evt.position().x() / ratio, evt.position().y() / ratio

            if action == scrcpy.ACTION_DOWN:
                self.mouse_down = True
                if widget:
                    self.control.touch_start(px, py, self.control.move_touch_id)

            elif action == scrcpy.ACTION_UP:
                self.mouse_down = False
                if widget:
                    self.control.touch_end(px, py, self.control.move_touch_id)
            elif action == scrcpy.ACTION_MOVE:
                if self.mouse_down == True and widget:
                    self.control.touch_move(px, py, self.control.move_touch_id)

            if self.show_cursor:
                print(px, py)



            



        return handler
    
    def move_test_worker(self, direction:str):
        self.control.move_start([direction])
        time.sleep(1)
        self.control.move_stop()


    def on_click_move_up(self):
        t = threading.Thread(
            target=self.move_test_worker, args=("UP",)
        )
        t.start()


    def on_click_move_down(self):
        t = threading.Thread(
            target=self.move_test_worker, args=("DOWN",)
        )
        t.start()

    def on_click_move_left(self):
        t = threading.Thread(
            target=self.move_test_worker, args=("LEFT",)
        )
        t.start()

    def on_click_move_right(self):
        t = threading.Thread(
            target=self.move_test_worker, args=("RIGHT",)
        )
        t.start()

    def on_click_show_cursor(self):
        self.show_cursor = not self.show_cursor 

    def on_click_reload_config(self):
        self.config = read_config(self.config_file)
        self.touch_map = self.config["touch_map"]
        self.game.touch_map = self.touch_map
        self.game.parse_skills()
        

    def on_click_test_stop(self):
        self.game.move_stop()


    def on_click_test_skill(self):
        if self.test_config is None:
            t = threading.Thread(target=self.skill_test_worker)
            t.start()
            
    def skill_test_worker(self):

        n_buff = len(self.game.buff_list)
        n_skills = len(self.game.skill_list)
        n_sp_skills = len(self.game.sp_skills_list)
        print(f"buff count:{n_buff}, skill count:{n_skills}, sp skill count:{n_sp_skills}")

        self.game.release_buff()
        

        for id in range(len(self.game.skill_list)):
            time.sleep(2)
            self.game.release_skill(id)

        for id in range(len(self.game.sp_skills_list)):
            time.sleep(2)
            self.game.release_skill(id,is_sp=True)

        self.game.normal_attack()
        time.sleep(0.5)
        self.game.normal_attack()
        time.sleep(0.5)
        self.game.normal_attack()
        time.sleep(0.5)
        self.game.normal_attack()

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

        print(f"Unknown keycode: {code}")
        return -1

    def on_init(self):
        self.setWindowTitle(f"Serial: {self.client.device_name}")

    def start_detect(self, frame):
        self.worker = DetectionWorker(self.model, frame, self)
        self.worker_thread = threading.Thread(target=self.worker.run)
        self.worker.ret.connect(self.on_worker_data_update)
        # self.worker.finished.connect(self.on_worker_finished)

        self.worker_thread.start()

    
    def on_worker_data_update(self, ret_dict):
        self.bbox = ret_dict["bbox"]
        self.scores = ret_dict["scores"]
        self.class_ids = ret_dict["class_ids"]
        cost_time = ret_dict["cost_time"]
        self.frame_time = f"{int(cost_time * 1000) } ms"
        cls_objects = []

        for cls in self.class_ids:
            label_text = class_names[cls]
            cls_objects.append(label_text)
        self.labels = cls_objects


        self.busy = False



        last_action, direction = self.game.actions(self.bbox, self.labels)
        ct = time.time()
        local_time = time.localtime(ct)
        time_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%01d" % (time_head, data_secs)
        if self.info != last_action:
            print(f"""[{time_stamp}] [{self.frame_time}] 
                [ROOM_ID:{self.game.game_map.last_id}][PATH_ID:{self.game.game_map.game_path.curPathId}]
                {last_action} moving: {direction}""")

        self.info = last_action
        # print(self.control.direct_tick)
        # self.control.update_direction(direction)
        self.control.move_to_direction(direction)


    def on_click_start(self):
        self.paused = False

    def on_click_stop(self):
        self.paused = True



    def on_frame(self, frame, fx=0.4, fy=0.4):
        app.processEvents()
        if frame is not None:
            map_id, _ = self.game.game_map.get_room_id(frame)


            self.game.frame += 1
            shape = frame.shape[0],frame.shape[1]

            ratio = self.max_width / max(self.client.resolution)
            if not self.paused:

                frame = cv2.resize(frame, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
                # if self.busy:
                #     print(f"[{time.time()}] dropped")

                if not self.busy and self.game.frame // self.game.frame_freq:
                    self.busy = True
                    self.start_detect(frame)
                    # print(self.game.frame)

                if len(self.bbox) > 0:
                    self.output_image = draw_detections(frame, self.bbox, self.scores, self.class_ids)
                    frame = self.output_image

                frame = cv2.resize(frame, (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)

            # self.game.main_loop(self.bbox, self.labels)
            image = QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                frame.shape[1] * 3,
                QImage.Format_BGR888,
            )
            self.ui.label_fps.setText(self.frame_time)



            # self.output_image = self.model.draw_detections(frame)

            # output_image = QImage(
            #     output_image,
            #     frame.shape[1],
            #     frame.shape[0],
            #     frame.shape[1] * 3,
            #     QImage.Format_BGR888,
            # )
            maplist = self.game.game_map.maplist
            map_img = maplist[map_id]

            map_qimg = QImage(
                map_img,
                map_img.shape[1],
                map_img.shape[0],
                map_img.shape[1] * 3,
                QImage.Format_BGR888,
            )
            # pix = QPixmap(output_image)
            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / ratio)
            self.ui.label.setPixmap(pix)

            self.ui.label_map.setPixmap(QPixmap(map_qimg))
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