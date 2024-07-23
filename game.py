import random
import time

import cv2
import numpy as np
import os
from utils import *
from control import ScrcpyControl
from map import GameMap
from map import PathGraph

names = [ 
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


            # 枪炮师   阿修罗
players = ["launcher", "asura"]

monsters = [  # 战士  冰奈斯 寒冰虎 狮子头 玩具兵
  "enemy_zs",  "enemy_bns","enemy_hbh", "enemy_szt", "enemy_wjb", 
  # 冤魂，蜘蛛，僵尸，歌利亚，无头骑士
  "enemy_yuanhun", "enemy_zhizhu", "enemy_jiangshi","enemy_gly",
  # 暗精灵，举盾精英怪，无头骑士，木乃伊
  "enemy_anjingling","enemy_tinggao", "enemy_boss_wutou", "enemy_munaiyi",
  # 黑骑士，亚德炎， 雷沃斯，黑色的精灵
  "enemy_boss_black_knight", "enemy_yadeyan", "enemy_leiwosi", "enemy_blackmonster",
  # 封印石，刹那影，骨兵，邪龙
  "enemy_stone", "enemy_boss_chaying","enemy_gubing", "enemy_boss_xielong"]

# 地图方向提示
# # 地上箭头
hints = ["arrow"]
# 房间箭头
direct_hints = ["arrow_up", "arrow_left", "arrow_right", "arrow_down"]

awards = ["card", "glod_card"] # 卡牌 黄金卡牌

items = ["money", "item"] # 掉落物

buddings = ["open_door", "close_door"]  # 地图大门



class GameAgent:
    def __init__(self, touch_map:dict, control:ScrcpyControl, map_name:str="", map_dir:str="") -> None:
        self.frame = 0
        self.frame_freq = 4 # 每隔 frame_freq 帧处理一次


        self.banzhuan = True # 搬砖模式/升级模式（寻路路逻辑不同）
        self.mode = "banzhuan" #  "levelup"
        self.avaialbe_mode = ["banzhuan", "levelup"]
        self.touch_map = touch_map

        self.skill_list = []
        self.buff_list = []
        self.sp_skills_list = []
        self.parse_skills()


        self.last_action = ""
        self.get_buff = False
        self.completed = False
        self.now_action = ""

        self.control = control
        self.game_map = GameMap(map_name, map_dir)



    def get_cls_name(self, cls_ids):
        cls_name = []
        for cls_id in cls_ids:
            cls_name.append(names[cls_id])

        return cls_name



    def parse_skills(self):

        for key, value in self.touch_map.items():
            prefix = key.split("_")[0]
            n_skill = 0
            n_buff = 0
            n_sp = 0
            
            if prefix == "skill":
                self.skill_list.append(self.touch_map[prefix+"_"+str(n_skill)])
                n_skill += 1
            elif prefix == "buff":
                self.skill_list.append(self.touch_map[prefix+"_"+str(n_buff)])
                n_buff += 1
            elif prefix == "sp":
                self.skill_list.append(self.touch_map[prefix+"_"+str(n_sp)])
                n_sp += 1





    def change_mode(self, mode):
        assert mode in self.avaialbe_mode
        self.mode = mode

    def main_loop(self, img_object, cls_object) -> None:
        if self.frame % self.frame_freq == 0:
            self.actions()
        pass

    def release_skill(self, skill_id):
        pass

    def release_buff(self, buff_id):
        pass

    def normal_attack(self):

        pass

    def flip_card(self):
        pass

    def move_stop(self):
        self.control.move_stop()






    # 控制角色执行操作
    def actions(self, img_object, cls_object, action_attack:list, 
                path:PathGraph, directkeys, control:ScrcpyControl, to_release):
        # 目标框:xywh,目标类别:str，当前房间id:int，buff动作:list[str]，攻击动作:list[str]
        global now_action, last_action, player_xywh, get_reward
        completed = False
        details = ""
        info = None

        if img_object is not None and len(img_object):

            # 方向阈值
            thx = 30  # 捡东西时，x方向的阈值
            thy = 30  # 捡东西时，y方向的阈值
            attx = 60  # 攻击时，x方向的阈值
            atty = 30  # 攻击时，y方向的阈值

            monsters_seen = [] #  [{cls_name: bbox}]
            items_seen = []

            open_door_seen = []

            card_seem = []
            hints_seen = []
            direct_hints_seen = []

            directs = [0,0,0,0] # left, right, up, down


            # 扫描角色和怪物的位置
            for i in range(len(cls_object)):
                if cls_object[i] in players:
                    player_xywh = img_object[i]

                if cls_object[i] in monsters:
                    monsters_seen.append([cls_object[i], img_object[i]])

                if cls_object[i] in items:
                    items_seen.append([cls_object[i], img_object[i]])

                if cls_object[i] == "open_door":
                    open_door_seen.append([cls_object[i], img_object[i]])

                if cls_object[i] in awards:
                    card_seem.append([cls_object[i], img_object[i]])

                if cls_object[i] in hints:
                    hints_seen.append([cls_object[i], img_object[i]])
                    
                if cls_object[i] in direct_hints:
                    direct_hints_seen.append([cls_object[i], img_object[i]])

            # 遇怪优先打怪
            # 捡东西
            # 根据房间id 和方位进下一个门
            if player_xywh is None and not get_reward:
                now_action = "PLAYER NOT FOUND"
                return now_action, get_reward, info

            if len(monsters_seen) > 0:
                get_reward = False
                now_action = "ATTACKING MONSTERS"
                monster_name = ""

                min_distance = float("inf")
                # 遍历怪物 寻找距离最近的怪
                for i in range(len(monsters_seen)):
                    cls_name, monster_xywh = monsters_seen[i]
                    dis = cal_distance_bottom(player_xywh, monster_xywh)
                    if dis < min_distance:
                        monster_box = monster_xywh
                        monster_name = cls_name
                        min_idx = i
                        min_distance = dis

                monster_x = cal_bottom_x(monster_box)
                monster_y = cal_bottom_y(monster_box)
                player_x = cal_bottom_x(player_xywh)
                player_y = cal_bottom_y(player_xywh)    

                # 处于攻击距离
                if abs(player_x - monster_x) < attx and abs(player_y - monster_y) < atty:
                    # zhuanshen
                    if monster_x - player_x > 0 : # 右侧
                        control.turn("RIGHT")
                    else:
                        control.turn("LEFT")

                    if len(action_attack)>0:
                        idx = random.randint(0,len(action_attack)-1)
                        # key = action_attack[idx]
                        x, y = action_attack[idx]
                        # directkeys.key_press(key)
                        control.tap(x, y)
                        
                        details = f"SKILL {idx} RELEASED"

                    # clear_action(action_cache, directkeys)


                    # break
                else:
                    if monster_x - player_x > attx : # 右侧
                        directs[1] = 1
                    elif monster_x - player_x < -attx :
                        directs[0] = 1
                    if monster_y - player_y > atty: # 下侧
                        directs[3] = 1
                    elif monster_y - player_y < -atty:
                        directs[2] = 1

                    d = direct(directs)

                    details = f"GO {d} TO ATTACK {monster_name}"
                    now_action += f" [{details}]"
                    key_status, directions = control.direction_move(direct=d, to_release=to_release)
                
                
            elif len(items_seen) > 0:
                now_action = "COLLECTING ITEMS"

                min_distance = float("inf")
                # 遍历物品
                for i in range(len(items_seen)):
                    cls_name, item_xywh = items_seen[i]
                    dis = cal_distance_bottom(player_xywh, item_xywh)
                    if dis < min_distance:
                        item_box = item_xywh
                        item_name = cls_name
                        min_idx = i
                        min_distance = dis
                
                if abs(item_box[1] - player_xywh[1]) > 0 or abs(item_box[0] - player_xywh[0]) > 0:

                    # directs = [0,0,0,0] # left, right, up, down

                    if item_box[0] - player_xywh[0] > thx:
                        # 右侧
                        directs[1] = 1
                    else:
                        # 左侧
                        directs[0] = 1

                    if item_box[1] - player_xywh[1] > thy:
                        # 下侧
                        directs[3] = 1
                    else:
                        # 上侧
                        directs[2] = 1


                    d = direct(directs)
                    
                    details = f"GO {d} TO COLLECT {item_name}"
                    now_action += f" [{details}]"
                    key_status, directions = control.direction_move(direct=d, to_release=to_release)
            
            elif len(card_seem) > 0:

                for k in ["W", "A", "S", "D"]:
                    directkeys.key_up(k)
                
                now_action = "CHECKING AWARD CARDS"
                time.sleep(1)
                directkeys.key_press("X")
                time.sleep(1)
                directkeys.key_press("X")
                time.sleep(1)
                directkeys.key_press("X")
                time.sleep(1)
                # directkeys.key_press("E")
                # directkeys.key_press("E")
                get_reward = True
            # 跟随提示
            else:
                if get_reward:
                    completed = True



                elif path:
                    self.where_to_go(open_door_seen, player_xywh, path, control, hint_xywh=None)

                elif len(direct_hints_seen) > 0:
                    now_action = "FOLLOWING ROOM HINTS"
                    cls_name, hint_xywh = direct_hints_seen[0]
                    direct_hint = cls_name.split("_")[1] if len(cls_name.split("_")) > 1 else None

                    hint_x = cal_center_x(hint_xywh)
                    hint_y = cal_center_y(hint_xywh)
                    player_x = cal_center_x(player_xywh)
                    player_y = cal_center_y(player_xywh)

                    if abs(hint_x - player_x) > 0 or abs(hint_y - player_y) > 0: 
                        # directs = [0,0,0,0] # left, right, up, down
                        if hint_x - player_x > thx:
                            # 右侧
                            directs[1] = 1
                        else:
                            # 左侧
                            directs[0] = 1

                        if hint_y - player_y > thy:
                            # 下侧
                            directs[3] = 1
                        else:
                            # 上侧
                            directs[2] = 1
                        d = direct(directs)
                        
                    details = f"MOVING {direct_hint} TO ENTRY DOOR"
                    now_action += f" [{details}]"
                    key_status, directions = control.direction_move(direct=d, to_release=to_release)


                #     if direct_hint:
                #         where_to_go(open_door_seen, player_xywh, action_cache, path,directkeys,hint_xywh=hint_xywh)

                # # 跟随提示
                elif len(hints_seen) > 3:
                    now_action = "FOLLOWING HINTS"
                    min_distance = float("inf")
                    min_sec_distance = float("inf")
                    direct_hint = None

                    distance_list = []


                    for i in range(len(hints_seen)):
                        cls_name, hint_xywh = hints_seen[i]
                        distance = cal_distance_bottom(player_xywh, hint_xywh)
                        distance_list.append((i, distance))
                    sorted_distance = sorted(distance_list, key=lambda x: x[1])

                    min_sec_distance_id = sorted_distance[1][0]
                    hint_name, hint_box = hints_seen[min_sec_distance_id]
                    

                    hint_x = cal_center_x(hint_box)
                    hint_y = cal_center_y(hint_box)
                    player_x = cal_bottom_x(player_xywh)
                    player_y = cal_bottom_y(player_xywh)


                    if abs(hint_x - player_x) > 0 or abs(hint_y - player_y) > 0: 
                        # directs = [0,0,0,0] # left, right, up, down
                        if hint_x - player_x > thx:
                            # 右侧
                            directs[1] = 1
                        else:
                            # 左侧
                            directs[0] = 1

                        if hint_y - player_y > thy:
                            # 下侧
                            directs[3] = 1
                        else:
                            # 上侧
                            directs[2] = 1
                        d = direct(directs)
                        
                    details = f"REMAIN {len(hints_seen)} HINTS"
                    now_action += f" [{details}]"
                    key_status, directions = control.direction_move(direct=d, to_release=to_release)

                else:
                    control.direction_move(direct=d, to_release=to_release)


                # where_to_go(open_door_seen, player_xywh, action_cache, path,directkeys)

            if last_action != now_action:
                # print(now_action)
                last_action = now_action

                
        else:
            # 随机移动以找到角色位置
            pass
            # action = [direct_dic[key] for key in direct_dic.keys()][random.randint(0,len(direct_dic)-1)]
            # directkeys.key_press(action)
        info = [key_status, directions]
        return last_action, completed, info


    # 获取地图中门的相对方位
    def get_door_direction(self, door_xywh:list, player_xywh):
        directs = [0, 0, 0, 0]
        ret = []
        if door_xywh[1] - player_xywh[1] > 0:
            directs[3] = 1
            ret.append("DOWN")
        else:
            directs[2] = 1
            ret.append("UP")

        if door_xywh[0] - player_xywh[0] > 0:
            directs[1] = 1
            ret.append("RIGHT")
        else:
            directs[0] = 1
            ret.append("LEFT")
        return ret

    def where_to_go(self, door_seen, player_xywh, path:PathGraph, control:ScrcpyControl, hint_xywh=None):
            
            global now_action
            now_action = "FINDING WAY"
            details = ""
            door_directions = []
            doors_xywh = []

            thx = 50
            thy = 30
            # doors = []
            directs = [0,0,0,0] # left, right, up, down
            
            if len(door_seen) > 0:
                # 看见多个门 记录门的方位信息
                for i in range(len(door_seen)):
                    cls_name, door_xywh = door_seen[i]
                    doors_xywh.append(door_xywh)
                    # door_direction = get_door_direction(door_xywh, player_xywh)
                    # if d in door_direction:
                    #     door_directions.append(d)
                    #     doors_xywh.append(door_xywh)
            else:
                directs = path.path_fit(path)

                details += "NO_DOOR_FOUND"

            # # 选择要进入的门
            # if hint_xywh is not None: # 有箭头提示
            #     target_door_xywh = get_min_distance_center(doors_xywh, hint_xywh)
            #     # room_direction = get_door_direction(target_door_xywh, player_xywh)
            #     door_x = cal_bottom_x(target_door_xywh)
            #     door_y = cal_bottom_y(target_door_xywh)
            #     hint_x = cal_center_y(hint_xywh)
            #     hint_y = cal_center_y(hint_xywh)

            #     player_x = cal_center_x(player_xywh)
            #     player_y = cal_center_y(player_xywh)

            #     if abs(hint_y - player_y) > 0 or abs(hint_x - player_x) > 0: 
            #         # directs = [0,0,0,0] # left, right, up, down
            #         if hint_x - player_x > thx:
            #             # 右侧
            #             directs[1] = 1
            #         else:
            #             # 左侧
            #             directs[0] = 1

            #         if hint_y - player_y > thy:
            #             # 下侧
            #             directs[3] = 1
            #         else:
            #             # 上侧
            #             directs[2] = 1
            #         d = direct(directs)

            # else:
            room_direction = self.game_map.get_direction(path)
            target_directtion = direct(self.game_map.path_fit(path)).split("_")

            if len(doors_xywh) > 0 and room_direction in target_directtion:

                if room_direction == "UP":
                    # 上侧门
                    door_xywh = cal_min_y(doors_xywh)
                    dx, dy = cal_bottom_x(door_xywh), cal_bottom_y(door_xywh)
                    px, py = cal_bottom_x(player_xywh), cal_center_y(player_xywh)
                    if dx - px >= thx: # 门在右边
                        directs[1] = 1
                        pass
                    elif px - dx >= thx:# 门在左边
                        directs[0] = 1
                    else: # 在范围内
                        directs[2] = 1


                elif room_direction == "DOWN":
                    # 下侧门
                    door_xywh = cal_max_y(doors_xywh)
                    dx, dy = cal_bottom_x(door_xywh), cal_bottom_y(door_xywh)
                    px, py = cal_bottom_x(player_xywh), cal_bottom_y(player_xywh)
                    if dx - px >= thx and dy > py: # 门在右边
                        directs[1] = 1
                        pass
                    elif px - dx >= thx and dy > py:# 门在左边
                        directs[0] = 1
                    else: # 在范围内
                        directs[3] = 1


                elif room_direction == "LEFT":
                    # 左侧门
                    door_xywh = cal_min_x(doors_xywh)
                    dx, dy = cal_bottom_x(door_xywh), cal_bottom_y(door_xywh)
                    px, py = cal_bottom_x(player_xywh), cal_bottom_y(player_xywh)

                    if dy - py >= thy: # 门在下边
                        directs[3] = 1
                        pass
                    elif py - dy >= thy:# 门在上边
                        directs[2] = 1
                    else: # 在范围内
                        directs[0] = 1
                elif room_direction == "RIGHT":
                    # 右侧门
                    door_xywh = cal_max_x(doors_xywh)

                    dx, dy = cal_bottom_x(door_xywh), cal_bottom_y(door_xywh)
                    px, py = cal_bottom_x(player_xywh), cal_bottom_y(player_xywh)

                    if dy - py >= thy and dx > px: # 门在下边
                        directs[3] = 1
                        pass
                    elif py - dy >= thy and dx > px:# 门在上边
                        directs[2] = 1
                    else: # 在范围内
                        directs[1] = 1


            else:
                directs = self.game_map.path_fit(path)

                # if room_direction == "UP":
                #     directs[2] = 1
                # elif room_direction == "DOWN":
                #     directs[3] = 1
                # elif room_direction == "LEFT":
                #     directs[0] = 1
                # elif room_direction == "RIGHT":
                #     directs[1] = 1
                details += "NO_DOOR_FOUND"

            
            d = direct(directs)
            if d:
                details += f" IN PATH NODE {path.curPathId if path else -1} MOVING {d}"
                control.direction_move(direct=d)
            else:
                details += f" STOPPED"
            now_action += f" [{details}]]"
        



    