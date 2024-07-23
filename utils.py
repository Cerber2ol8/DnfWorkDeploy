


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
