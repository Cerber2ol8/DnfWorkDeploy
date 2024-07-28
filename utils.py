#coding:utf-8

import cv2
import numpy as np
from typing import Tuple

class_names = [ 
  # 枪炮师，阿修罗
  "launcher", "asura",
  # 金币， 道具
  "money", "item",
  # 开启的门， 关闭的门
  "open_door", "close_door", 
  # 地上箭头， 房间箭头
  "arrow", "arrow_up", "arrow_left", "arrow_right", "arrow_down", 
  # 保留
  "monster", 
  # 战士  冰奈斯 寒冰虎 狮子头 玩具兵
  "enemy_zs",  "enemy_bns","enemy_hbh", "enemy_szt", "enemy_wjb", 
  # 冤魂，蜘蛛，僵尸，歌利亚，无头骑士
  "enemy_yuanhun", "enemy_zhizhu", "enemy_jiangshi","enemy_gly",
  # 暗精灵，举盾精英怪，无头骑士，木乃伊
  "enemy_anjingling","enemy_tinggao", "enemy_boss_wutou", "enemy_munaiyi",
  # 黑骑士，亚德炎， 雷沃斯，黑色的精灵
  "enemy_boss_black_knight", "enemy_yadeyan", "enemy_leiwosi", "enemy_blackmonster",
  # 封印石，刹那影，骨兵，邪龙
  "enemy_stone", "enemy_boss_chaying","enemy_gubing", "enemy_boss_xielong",
  # 普通卡牌，金牌
  "card", "glod_card"
  ]


rng = np.random.default_rng(3)
colors = rng.uniform(0, 255, size=(len(class_names), 3))


def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y


def draw_detections(image, boxes, scores, class_ids, mask_alpha=0.3):
    det_img = image.copy()

    img_height, img_width = image.shape[:2]
    font_size = min([img_height, img_width]) * 0.0006
    text_thickness = int(min([img_height, img_width]) * 0.001)

    det_img = draw_masks(det_img, boxes, class_ids, mask_alpha)

    # Draw bounding boxes and labels of detections
    for class_id, box, score in zip(class_ids, boxes, scores):
        color = colors[class_id]

        draw_box(det_img, box, color)

        label = class_names[class_id]
        caption = f'{label} {int(score * 100)}%'
        draw_text(det_img, caption, box, color, font_size, text_thickness)

    return det_img


def draw_box( image: np.ndarray, box: np.ndarray, color: Tuple[int, int, int] = (0, 0, 255),
             thickness: int = 2) -> np.ndarray:
    x1, y1, x2, y2 = box.astype(int)
    return cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)


def draw_text(image: np.ndarray, text: str, box: np.ndarray, color: Tuple[int, int, int] = (0, 0, 255),
              font_size: float = 0.001, text_thickness: int = 2) -> np.ndarray:
    x1, y1, x2, y2 = box.astype(int)
    (tw, th), _ = cv2.getTextSize(text=text, fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                  fontScale=font_size, thickness=text_thickness)
    th = int(th * 1.2)

    cv2.rectangle(image, (x1, y1),
                  (x1 + tw, y1 - th), color, -1)

    return cv2.putText(image, text, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), text_thickness, cv2.LINE_AA)

def draw_masks(image: np.ndarray, boxes: np.ndarray, classes: np.ndarray, mask_alpha: float = 0.3) -> np.ndarray:
    mask_img = image.copy()

    # Draw bounding boxes and labels of detections
    for box, class_id in zip(boxes, classes):
        color = colors[class_id]

        x1, y1, x2, y2 = box.astype(int)

        # Draw fill rectangle in mask image
        cv2.rectangle(mask_img, (x1, y1), (x2, y2), color, -1)

    return cv2.addWeighted(mask_img, mask_alpha, image, 1 - mask_alpha, 0)



def cal_distance(obj1_xywh, obj2_xywh):
    # 计算左上角坐标
    distance = ((obj1_xywh[0] - obj2_xywh[0]) ** 2 + (obj1_xywh[1] - obj2_xywh[1]) ** 2) ** 0.5
    return distance

def cal_distance_center(obj1_xywh, obj2_xywh):
    # 计算中心坐标
    cx1, cy1 = obj1_xywh[0] + obj1_xywh[2] * 0.5, obj1_xywh[1] + obj1_xywh[3] * 0.5
    cx2, cy2 = obj2_xywh[0] + obj2_xywh[2] * 0.5, obj2_xywh[1] + obj2_xywh[3] * 0.5
    
    distance = ((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2) ** 0.5
    return distance

def cal_distance_bottom(obj1_xywh, obj2_xywh):
    # 计算底部坐标
    cx1, cy1 = obj1_xywh[0] + obj1_xywh[2] * 0.5, obj1_xywh[1] + obj1_xywh[3]
    cx2, cy2 = obj2_xywh[0] + obj2_xywh[2] * 0.5, obj2_xywh[1] + obj2_xywh[3]
    
    distance = ((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2) ** 0.5
    return distance

def cal_min_x(xywh_list:list)->list:
    min = float("inf")
    ret = None
    for xywh in xywh_list:
        x_center = xywh[0] + xywh[2] * 0.5
        if x_center < min:
            min = x_center
            ret = xywh
    return ret
def cal_max_x(xywh_list:list)->list:
    max = 0.
    ret = None
    for xywh in xywh_list:
        x_center = xywh[0] + xywh[2] * 0.5
        if x_center > max:
            max = x_center
            ret = xywh
    return ret

def cal_min_y(xywh_list:list)->list:
    min = float("inf")
    ret = None
    for xywh in xywh_list:
        y_center = xywh[1] + xywh[3] * 0.5
        if y_center < min:
            min = y_center
            ret = xywh
    return ret

def cal_max_y(xywh_list:list)->list:
    max = 0.
    ret = None
    for xywh in xywh_list:
        y_center = xywh[1] + xywh[3] * 0.5
        if y_center > max:
            max = y_center
            ret = xywh
    return ret

def cal_center_x(xywh:list)->float:
    return xywh[0] + xywh[2] * 0.5

def cal_center_y(xywh:list)->float:
    return xywh[1] + xywh[3] * 0.5

def cal_bottom_x(xywh:list)->float:
    return xywh[0] + xywh[2] * 0.5

def cal_bottom_y(xywh:list)->float:
    return xywh[1] + xywh[3]

def get_min_distance_center(objects:list, target:list):
    min_distance = float("inf")
    box = objects[0]
    for xywh in objects:
        dis = cal_distance_center(xywh, target)
        if dis < min_distance:
            dis = min_distance
            box = xywh
    return box




def direct(directs):
    if sum(d for d in directs) > 0:
        if directs == [1,0,0,0]:
            direct = "LEFT"
        elif directs == [0,1,0,0]:
            direct = "RIGHT"
        elif directs == [0,0,1,0]:
            direct = "UP"
        elif directs == [0,0,0,1]:
            direct = "DOWN"
        elif directs == [1,0,1,0]:
            direct = "LEFT_UP"
        elif directs == [1,0,0,1]:
            direct = "LEFT_DOWN"
        elif directs == [0,1,1,0]:
            direct = "RIGHT_UP"
        elif directs == [0,1,0,1]:
            direct = "RIGHT_DOWN"
        else:
            direct = "STOP"

        return direct
    else:
        return "STOP"
