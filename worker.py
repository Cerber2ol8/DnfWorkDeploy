import random
import time

import cv2
import numpy as np
import torch
import os
os.environ['YOLO_VERBOSE'] = "false"

from ultralytics import YOLO

# import directkeys
# from direction_move import move
# from directkeys import ReleaseKey
# from getkeys import key_check

from grabber import Grabber
from inputs import KeyboardInput


# from skill_recgnize import skill_rec
# from small_recgonize import current_door


from agent import actions
from map import get_room_id
import map, agent
# 设置参数

print("LOADING YOLO MODEL...")
model = YOLO('ckpt/best.pt')
print("LOAD YOLO MODEL COMPLETE.")

paused = False

view_img = False  # 是否观看目标检测结果


skill_buff = "3,4"
actions_buff = skill_buff.split(",")



action_cache = None  # 动作标记

frame = 0  # 帧

fs = 4  # 每n帧处理一次


banzhuan = True # 搬砖模式/升级模式（寻路路逻辑不同）
mode = "banzhuan" if banzhuan else "levelup"




# 指定窗口标题
window_title = "PCT-AL10"  # 窗口标题
g = Grabber(window_title) # 要捕获的窗口

uhid_control = KeyboardInput(window_title=window_title) # 键盘输入
# move_key = KeyboardInput(sc_control=True)  # sc模拟点击
move_key = uhid_control
action_cache = []

last_action = ""

get_buff = False

completed = False

now_action = ""



def cal_bottom_x(xywh:list)->float:
    return xywh[0] + xywh[2] * 0.5

def cal_bottom_y(xywh:list)->float:
    return xywh[1] + xywh[3]

def get_bottom(x1, y1, x2, y2)->list[int]:
    return (x1+x2)//2, y2


def play(img, img_objects, cls_objects, game_path=None):
    global get_buff, now_action, last_action, action_cache
    global g,k

    if game_path:
        current_room, _ = get_room_id(img, game_path)
    else:
        current_room = 0


    if current_room == 6:
        action_attack = [char for char in "FFFFFQQQEERRTHTTGGHHYYY"]
    else:
        action_attack = [char for char in "XXXXXXXFFFQQQEERRTTTHHHGGG"]




    if current_room >= 0:
        if not get_buff:
            if "asura" in cls_objects or "launcher" in cls_objects:
                while len(actions_buff)>0:
                    buff = actions_buff.pop()
                    now_action += f"[ADD BUFF {buff}]"
                    time.sleep(0.1)
                    uhid_control.key_press(buff)
                get_buff = True

    action_cache, action_log, completed, info = actions(img_objects, cls_objects, current_room, 
                                    action_cache, action_attack, game_path, 
                                    directkeys=move_key, skill_input=uhid_control, to_release=fs)
    if result:
        now_action += action_log
    path_id = game_path.curPathId if game_path else 0
    room_id = game_path.curRoomId  if game_path else 0
    now_action = f"NOW:[PATH NODE:{path_id}][ROOM:{room_id}] {now_action}"
    if last_action != now_action:
        print(now_action)
        last_action = now_action

    return completed, info


def detect():
    pass

if __name__ == "__main__":
    names = model.names
    now_action = ""

    boxes = []
    confidences = []
    classes = []

    img_objects = []
    cls_objects = []

    game_path = map.shanji() if mode == "banzhuan" else None
    info = None


    # 捕捉画面+目标检测+玩游戏

    while True:
        if not paused:
            
            img = g.frame()
            frame += 1
            img2show = img

            names = model.names
            if frame % fs == 0:
                t_start = time.time()
                now_action = ""

                results = model(img)
                det = results[0]
                result = results[0]

                boxes = result.boxes.xyxy
                confidences = result.boxes.conf
                classes = result.boxes.cls
                img_objects.clear()
                cls_objects.clear()

                for box in boxes:
                    x1, y1, x2, y2 = [int(coord) for coord in box]
                    xywh = torch.tensor([x1,y1,x2-x1,y2-y1])
                    img_objects.append(xywh)
                    
                for cls in classes:
                    label_text = names[cls.cpu().item()]
                    cls_objects.append(label_text)


     
                completed, info = play(img, img_objects, cls_objects, game_path=game_path)
                # print(cls_object)

                
                if completed:
                    time.sleep(6)
                    completed = False
                    get_buff = False
                    actions_buff = skill_buff.split(",")


                    del game_path
                    game_path = map.shanji() if mode == "banzhuan" else None
                    time.sleep(2)
                    print("[CHOOSE START NEXT GAME]")
                    uhid_control.key_press("Tab")
                    time.sleep(2)
                    uhid_control.key_press("Tab")
                    uhid_control.key_press("Tab")
                    time.sleep(5)
       

                t_end = time.time()
                # print(f"TICK TIME:{1000 * (t_end - t_start) / fs} ms")
            for (box, label_text) in zip(boxes, cls_objects):
                x1, y1, x2, y2 = [int(coord) for coord in box]

                center = get_bottom(x1, y1, x2, y2)
                cv2.rectangle(img2show, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(img2show, center, 20, (0, 255, 0), 2)
                cv2.putText(img2show, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(img2show, str(info), (0, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            if img2show is not None and view_img:
                w,h = img2show.shape[0],img2show.shape[1]
                img2show = cv2.resize(img2show,(h//3, w//3))
                cv2.imshow("YOLO Detection", img2show)
                # 按 'q' 键退出
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break


                
                




