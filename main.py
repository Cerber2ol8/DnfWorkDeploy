from argparse import ArgumentParser
from typing import Optional, Tuple
import os
current_path = os.environ.get('PATH', '')
new_path = os.path.abspath(os.getcwd())
os.environ['PATH'] = current_path + os.pathsep + new_path

from adbutils import adb
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap, QTextCursor, QKeySequence
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QObject, Signal, Qt

import threading
import scrcpy

import json
import numpy as np
import time

from Ui_main import Ui_MainWindow

# os.environ['YOLO_VERBOSE'] = "false"


from check_cuda import check_cuda_available
check_cuda_available()

from utils import draw_detections, class_names
# from ultralytics import YOLO
import yolo
from yolo import YOLOv8
from control import ScrcpyControl
from game import GameAgent, GameConfig

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

class Logger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def __call__(self, *message):
        for arg in message:
            self.write(str(arg).replace("\n", "\r\n"))


    def write(self, message):
        if message != '\n':
            print(message)
            self.text_edit.append(message)
            self.text_edit.moveCursor(QTextCursor.End)

    def flush(self):
        self.text_edit.setText("")




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
        _boxes, _scores, _class_ids = self.model(self.image)
        # result = self.model(self.image)[0]
        # Process results list

        # _boxes = result.boxes.xyxy.cpu().numpy()  # Boxes object for bounding box outputs
        # masks = result.masks  # Masks object for segmentation masks outputs
        # keypoints = result.keypoints  # Keypoints object for pose outputs
        # _scores = result.boxes.conf.cpu().numpy()  # Probs object for classification outputs
        # obb = result.obb  # Oriented boxes object for OBB outputs
        # _class_ids = result.boxes.cls.cpu().tolist()
        # _class_ids = [int(value) for value in _class_ids]

        # _output_image = draw_detections(self.image, _boxes, _scores, _class_ids)

        # _output_image = result.plot()







        _time = time.time() - start

        ret_dict = {
            "start_time": start,
            "bbox": _boxes,
            "scores": _scores,
            "class_ids": _class_ids,
            "cost_time": _time,
            # "out_image": _output_image
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
        # sys.stdout = PrintLogger(self.ui.textEdit)
        # sys.stderr = PrintLogger(self.ui.textEdit)
        self.logger = Logger(self.ui.textEdit)


        self.config_file = "config.json"

        self.config = read_config(self.config_file)
        self.touch_map = self.config["touch_map"]
        self.keyboard_map = self.config["keyboard_map"]

        self.test_config = None
        # print(self.touch_map)

        # self.model = YOLOv8("best.onnx", conf_thres=0.05)
        self.model = YOLOv8("best.onnx", conf_thres=0.35, iou_thres=0.75)
        # self.model("test.png")
        self.bbox = []
        self.scores = []
        self.class_ids = []
        self.busy = False
        self.busy_locker = threading.Lock()
        self.frame_time = ""
        self.info = ""
        self.current_frame = None


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
        
        self.game = GameAgent(
            self.touch_map, self.control, 8, "shanji",
              "maps/shanji", 10,
              GameConfig()
              )
        self.worker = None
        self.output_image = None
        self.paused = True

        self.show_cursor = False

        self.map_save_count = 0
        self.setting_map = False

        self.keyboard_mode = self.ui.keyboard_mode.isChecked()







        # Bind controllers
        self.ui.button_reload.clicked.connect(self.on_click_reload_config)
        self.ui.button_back.clicked.connect(self.on_click_reset)
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

        self.ui.button_save_map.clicked.connect(self.on_click_save_map)

        self.ui.button_get_map.clicked.connect(self.on_click_get_map)

        self.ui.slider_frame_req.valueChanged.connect(self.on_slider_frame_freq_changed)
        self.ui.slider_attx.valueChanged.connect(self.on_slider_attx_changed)
        self.ui.slider_atty.valueChanged.connect(self.on_slider_atty_changed)




        # Bind config
        self.ui.combo_device.currentTextChanged.connect(self.choose_device)
        self.ui.flip.stateChanged.connect(self.on_flip)

        self.mouse_down = False
        self.setFocusPolicy(Qt.StrongFocus)

        # 设置控件初值
        self.ui.slider_frame_req.setValue(self.game.frame_freq)
        self.ui.slider_attx.setValue(self.game.conf.enemy_x)
        self.ui.slider_atty.setValue(self.game.conf.enemy_y)

        # Bind mouse event
        self.ui.label.mousePressEvent = self.on_mouse_event(scrcpy.ACTION_DOWN)
        self.ui.label.mouseMoveEvent = self.on_mouse_event(scrcpy.ACTION_MOVE)
        self.ui.label.mouseReleaseEvent = self.on_mouse_event(scrcpy.ACTION_UP)

        # Keyboard event
        self.keyPressEvent = self.on_key_down()
        self.keyReleaseEvent = self.on_key_up()


    def on_slider_frame_freq_changed(self, value):
        self.game.frame_freq = value
        self.logger(f"change frame_freq to { value }")
        self.ui.label_info_frame_freq.setText(str(value))

    def on_slider_attx_changed(self, value):
        self.game.conf.enemy_x = value
        self.logger(f"change enemy_x to { value }")
        self.ui.label_attx.setText(str(value))



    def on_slider_atty_changed(self, value):
        self.game.conf.enemy_y = value
        self.logger(f"change enemy_y to { value }")
        self.ui.label_atty.setText(str(value))


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




    def on_click_get_map(self):

        self.setting_map = True

        img = self.game.game_map.get_map(self.current_frame)

        # shape = img.shape

        # image = QImage(
        #     img,
        #     shape[1],
        #     shape[0],
        #     shape[1] * 3,
        #     QImage.Format_BGR888,
        # )

        # pix = QPixmap(image)

        # self.ui.label_map.setPixmap(pix)

    def on_click_reset_map(self):
        self.map_save_count = 0



    def on_click_save_map(self):

        if not os.path.exists("maps"):
            os.mkdir("maps")


        dir = os.path.join(os.path.abspath(os.getcwd()), "maps","shanji")
        if not os.path.exists(dir):
            os.mkdir(dir)

        img_path = os.path.join(dir, str(self.map_save_count) + ".png")

        img = self.game.game_map.get_map(self.current_frame)

        if os.path.exists(img_path):
            reply = QMessageBox.question(self, "地图图片已存在", "要覆盖这个图片吗？",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                cv2.imwrite(img_path, img)
                self.map_save_count += 1
        else:
            cv2.imwrite(img_path, img)
            self.map_save_count += 1





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
                # print(px, py)
                self.logger(px, py)

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
        # print(f"buff count:{n_buff}, skill count:{n_skills}, sp skill count:{n_sp_skills}")
        self.logger(f"buff count:{n_buff}, skill count:{n_skills}, sp skill count:{n_sp_skills}")

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

    def on_key_down(self):
        action=scrcpy.ACTION_DOWN
        def handler(evt: QKeyEvent):
            if self.ui.keyboard_mode.isChecked():
                code = self.map_code(evt.key())
                if code != -1:
                    self.client.control.keycode(code, action)
            else:
                auto_repeate = evt.isAutoRepeat()
                evt_type = evt.type()
                self.map_keyboard(evt.key(), action, auto_repeate)

        return handler
    def on_key_up(self, action=scrcpy.ACTION_UP):
        action=scrcpy.ACTION_UP
        def handler(evt: QKeyEvent):
            if self.ui.keyboard_mode.isChecked():
                code = self.map_code(evt.key())
                if code != -1:
                    self.client.control.keycode(code, action)
            else:
                auto_repeate = evt.isAutoRepeat()
                evt_type = evt.type()
                self.map_keyboard(evt.key(), action, auto_repeate)
        return handler
    
    
    def map_keyboard(self, code, action=scrcpy.ACTION_DOWN, auto_repeate=False):
        # ← ↑ → ↓ 16777234 16777235 16777236 16777237
        # 
        if auto_repeate:
            return

        # x, y = self.keyboard_map[""]
        direction = ""
        directions = self.control.directions
        if code == 16777234:
            direction = "LEFT"
        elif code == Qt.Key_Up:
            direction = "UP"
        elif code == 16777236:
            direction = "RIGHT"
        elif code == Qt.Key_Down:
            direction = "DOWN"
        else:
            pass



        if action == scrcpy.ACTION_UP and not auto_repeate:
            if direction in directions:
                self.control.directions.remove(direction)
            else:
                keys = list(self.keyboard_map.values())
                keys = list(filter(None, keys))

                for key_str in keys:
                    keycode = QKeySequence(key_str)[0].key()
                    if keycode == code:
                        acion_name = self.get_keys_by_value(self.keyboard_map, key_str)
                        x, y = self.touch_map[acion_name]
                        self.control.touch_end(x, y, self.control.skill_touch_id)

                        self.logger(f"skill key released {acion_name}")




            self.logger(f"KEY {code} UP")
        elif action == scrcpy.ACTION_DOWN and not auto_repeate:
            if len(direction) > 0 and direction not in directions:
                self.control.directions.append(direction)
            else:
                keys = list(self.keyboard_map.values())
                keys = list(filter(None, keys))

                for key_str in keys:
                    keycode = QKeySequence(key_str)[0].key()
                    if keycode == code:
                        acion_name = self.get_keys_by_value(self.keyboard_map, key_str)
                        x, y = self.touch_map[acion_name]
                        self.control.touch_start(x, y, self.control.skill_touch_id)
                        self.logger(f"skill key pressed {acion_name}")


            self.logger(f"KEY {code} DOWN")



        target = "_".join(self.control.directions) if len(self.control.directions)>0 else "STOP"
        self.control.move_to_direction(target)

        self.logger(f"move_to_direction {target}")


    def get_keys_by_value(self, d, target_value):
        return [k for k, v in d.items() if v == target_value][0]

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

        # print(f"Unknown keycode: {code}")
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
        self.frame_time = f"latency {int(cost_time * 1000) } ms"
        # self.output_image = ret_dict["out_image"]
        
        cls_objects = []

        for cls in self.class_ids:
            label_text = class_names[cls]
            cls_objects.append(label_text)
        self.labels = cls_objects


        last_action, direction = self.game.actions(self.bbox, self.labels)
        ct = time.time()
        local_time = time.localtime(ct)
        time_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000
        time_stamp = "%s.%01d" % (time_head, data_secs)
        if self.info != last_action:
            # print(f"""[{time_stamp}] [{self.frame_time}] 
            #     [ROOM_ID:{self.game.game_map.last_id}][PATH_ID:{self.game.game_map.game_path.curPathId}]
            #     {last_action} moving: {direction}""")
            self.logger(f"""[{time_stamp}] [{self.frame_time}] 
                [ROOM_ID:{self.game.game_map.last_id}][PATH_ID:{self.game.game_map.game_path.curPathId}]
                {last_action} moving: {direction}""")
        self.info = last_action
        self.frame_time += f"\r\n[ROOM_ID:{self.game.game_map.last_id}][PATH_ID:{self.game.game_map.game_path.curPathId}]"
        # print(self.control.direct_tick)
        # self.control.update_direction(direction)
        self.control.move_to_direction(direction)
        with self.busy_locker:
            self.busy = False


    def on_click_start(self):
        self.paused = False

    def on_click_stop(self):
        self.paused = True
    def on_click_reset(self):
        self.game.reset()
        with self.busy_locker:
            self.busy = False




    def on_frame(self, frame, fx=1.0, fy=1.0):
        app.processEvents()
        if frame is not None:
            self.current_frame = frame.copy()
            map_id, _ = self.game.game_map.get_room_id(frame)


            self.game.frame += 1
            shape = frame.shape[0],frame.shape[1]

            ratio = self.max_width / max(self.client.resolution)
            image = QImage(
                frame,
                shape[1],
                shape[0],
                shape[1] * 3,
                QImage.Format_BGR888,
            )

            if not self.paused:
                if self.game.frame % self.game.frame_freq == 0:

                    input_img = cv2.resize(frame, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
                    if self.busy:
                        # print(f"frame [{self.game.frame}] dropped")
                        self.logger(f"frame [{self.game.frame}] dropped")
                    else:
                        with self.busy_locker:
                            self.busy = True
                        self.start_detect(input_img)
                        # print(self.game.frame)


                # self.game.main_loop(self.bbox, self.labels)
                if len(self.bbox)>0:
                    # frame = cv2.resize(frame, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
                    bbox = []
                    for box in self.bbox:
                        x1,y1,x2,y2 = box
                        bbox.append([x1 // fx, y1 // fy, x2 // fx, y2 // fy])
                    bbox = np.array(bbox)

                    frame = draw_detections(frame, bbox, self.scores, self.class_ids)
                    # frame = cv2.resize(frame, (shape[1], shape[0]), interpolation=cv2.INTER_LINEAR)
                    image = QImage(
                        frame,
                        shape[1],
                        shape[0],
                        shape[1] * 3,
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
            # maplist = self.game.game_map.maplist
            # map_img = maplist[map_id]

            # map_qimg = QImage(
            #     map_img,
            #     map_img.shape[1],
            #     map_img.shape[0],
            #     map_img.shape[1] * 3,
            #     QImage.Format_BGR888,
            # )
            # pix = QPixmap(output_image)
            pix = QPixmap(image)
            pix.setDevicePixelRatio(1 / ratio)
            self.ui.label.setPixmap(pix)

            # if not self.setting_map:
            #     self.ui.label_map.setPixmap(QPixmap(map_qimg))
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