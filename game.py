import random
import time
import math
import cv2
import numpy as np
import os
from utils import *
from control import ScrcpyControl
from map import GameMap
from map import PathGraph
import threading

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
    def __init__(self, touch_map:dict, control:ScrcpyControl, 
                 frame_freq = 5,
                 map_name:str="", map_dir:str="",
                 to_release = 20) -> None:
        self.frame = 0
        self.frame_freq = frame_freq # 每隔 frame_freq 帧处理一次


        self.banzhuan = True # 搬砖模式/升级模式（寻路路逻辑不同）
        self.mode = "banzhuan" #  "levelup"
        self.avaialbe_mode = ["banzhuan", "levelup"]
        self.touch_map = touch_map

        self.skill_list = []
        self.buff_list = []
        self.sp_skills_list = []
        self.parse_skills()
         
        self.map_name = map_name
        self.map_dir = map_dir  

        self.control = control
        self.to_release = to_release



        self.last_action = ""
        self.get_buff = False
        self.round_completed = False
        self.get_reward = False
        self.operation_locker = threading.Lock()
        self.operation_finshed = True


        self.player_xywh = [200,500,100,100]

        self.last_player_xywh = self.player_xywh
        self.stop_count = 0


        self.now_action = ""
        self.game_map = GameMap(map_name, map_dir)


    def reset(self):
        self.last_action = ""
        self.get_buff = False
        self.round_completed = False
        self.now_action = ""
        self.get_reward = False
        self.player_xywh = [200,500,100,100]
        self.game_map = GameMap(self.map_name, self.map_dir)
        self.round_completed = False
        

    def get_cls_name(self, cls_ids):
        cls_name = []
        for cls_id in cls_ids:
            cls_name.append(names[cls_id])

        return cls_name



    def parse_skills(self):
        n_skill = 0
        n_buff = 0
        n_sp = 0
        self.skill_list = []
        self.buff_list = []
        self.sp_skills_list = []
        for key, value in self.touch_map.items():
            prefix = key.split("_")[0]

            
            if prefix == "skill":
                pos = self.touch_map[prefix+"_"+str(n_skill)]
                if pos[0] != 0 or pos[1] != 0:
                    self.skill_list.append(pos)
                    n_skill += 1
            elif prefix == "buff":
                pos = self.touch_map[prefix+"_"+str(n_buff)]
                if pos[0] != 0 or pos[1] != 0:
                    self.buff_list.append(pos)
                    n_buff += 1
            elif prefix == "sp":
                pos = self.touch_map[prefix+"_"+str(n_sp)]
                if pos[0] != 0 or pos[1] != 0:
                    self.sp_skills_list.append(pos)
                    n_sp += 1





    def change_mode(self, mode):
        assert mode in self.avaialbe_mode
        self.mode = mode

    def main_loop(self, img_object, cls_object) -> None:
        # self.control.on_frame()
        pass


    def release_skill(self, skill_id, is_sp=False):
        # self.control.move_stop()
        t = threading.Thread(
            target=self.release_skill_worker, args=(skill_id, is_sp)
        )
        t.start()
        
            
    def release_skill_worker(self, skill_id, is_sp):
        if not is_sp:
            x, y = self.skill_list[skill_id]
        else:
            x, y = self.sp_skills_list[skill_id]
        self.control.tap(x, y, self.control.skill_touch_id)


    def release_buff(self):
        # self.control.move_stop()
        t = threading.Thread(
            target=self.release_buff_worker
        )
        t.start()

    def release_buff_worker(self):
        if not self.get_buff:
            for buff_id in range(len(self.buff_list)):
                x, y = self.buff_list[buff_id]
                self.control.tap(x, y, self.control.skill_touch_id)
                time.sleep(0.1)
            self.get_buff = True


    def normal_attack(self):
        self.control.attack()



    def move_stop(self):
        self.control.move_stop()


    def flip_card(self):
        t = threading.Thread(
            target=self.flip_card_worker
        )

        if self.operation_finshed:
            t.start()

    def flip_card_worker(self):

        with self.operation_locker:
            self.operation_finshed = False

        self.control.tap(100,100)
        time.sleep(0.5)
        self.control.tap(100,100)
        time.sleep(0.5)
        self.control.tap(100,100)
        time.sleep(0.5)
        
        with self.operation_locker:
            self.get_reward = True
            self.operation_finshed = True
            

    def choose_next_game(self):
        t = threading.Thread(
            target=self.choose_next_game_worker
        )

        if self.operation_finshed:
            t.start()

    def choose_next_game_worker(self):
        with self.operation_locker:
            self.operation_finshed = False
        self.control.tap_pos(self.touch_map["options_0"])
        time.sleep(0.5)
        self.control.tap_pos(self.touch_map["options_0"])
        time.sleep(0.5)
        self.control.tap_pos(self.touch_map["options_0"])
        time.sleep(0.5)
        print("=====NEXT GAME START=====")
        
        with self.operation_locker:
            self.operation_finshed = True


    def check_stop(self, max=5, thre=0.5):
        x1, y1, w1, h1 = self.last_player_xywh
        x2, y2, w2, h2 = self.player_xywh

        center1 = [(2 * x1 + w1) / 2, (2 * y1 + h1) / 2]
        center2 = [(2 * x2 + w2) / 2, (2 * y2 + h2) / 2]
        w = (w1 + w2) / 2
        h = (h1 + h2) / 2
        hypotenuse = math.sqrt(w ** 2 + h ** 2)


        diff_x = (center2[0] - center1[0])
        diff_y = (center2[1] - center1[1])

        distance = (diff_x ** 2 + diff_y ** 2)

        is_move = distance / hypotenuse >= thre 

        if not is_move:
            self.stop_count += 1
        else:
            self.stop_count = 0
        self.last_player_xywh = self.player_xywh
        
        if self.stop_count >= max:
            return True
        else:
            return False


        
        





    # 控制角色执行操作
    def actions(self, img_object, cls_object, thx=50, thy=50, attx=200, atty=100):
        # 方向阈值
        # thx = 30  # 捡东西时，x方向的阈值
        # thy = 30  # 捡东西时，y方向的阈值
        # attx = 60  # 攻击时，x方向的阈值
        # atty = 30  # 攻击时，y方向的阈值
        # 目标框:xywh,目标类别:str，当前房间id:int，buff动作:list[str]，攻击动作:list[str]

        direction = "STOP"

        round_completed = False

        details = ""

        if self.game_map.game_path.is_waiting():

            self.last_action = "WAITING FOR CROSSING ROOM DOOR"
            directs = self.game_map.path_fit(self.game_map.game_path)
            direction = direct(directs)

            return self.last_action, direction
        elif not self.operation_finshed:

            self.last_action = "WAITING FOR OPERATION"
            direction = "STOP"
            return self.last_action, direction

        if img_object is not None and len(img_object):

 

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
                    self.player_xywh = img_object[i]
                    self.release_buff()

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


            if len(card_seem) > 0:

                self.control.stop_all()
                self.now_action = "CHECKING AWARD CARDS"
                # time.sleep(1)
                self.flip_card()
                direction = "STOP"
                self.now_action = "GET REWARD CARD"
                self.last_action = self.now_action
                return self.last_action, direction
            
            elif self.get_reward and len(items_seen) == 0:
                self.choose_next_game()
                self.reset()
                direction = "STOP"
                self.now_action = "CHOOSE NEXT GAME"
                self.last_action = self.now_action
                return self.last_action, direction

            # 遇怪优先打怪
            # 捡东西
            # 根据房间id 和方位进下一个门
            elif self.player_xywh is None and not self.get_reward:
                self.now_action = "PLAYER NOT FOUND"

                direction = "STOP" # 默认往右走
            
            elif self.check_stop():
                # 判断角色是否连续不动
                self.now_action = "PLAYER STOP DETECTED"
                self.control.move_to_direction("STOP")
                direction = "RIGHT"
                self.last_action = self.now_action

                
            elif len(monsters_seen) > 0:
                self.get_reward = False
                self.now_action = "ATTACKING MONSTERS"
                monster_name = ""

                min_distance = float("inf")
                # 遍历怪物 寻找距离最近的怪
                for i in range(len(monsters_seen)):
                    cls_name, monster_xywh = monsters_seen[i]
                    dis = cal_distance_bottom(self.player_xywh, monster_xywh)
                    if dis < min_distance:
                        monster_box = monster_xywh
                        monster_name = cls_name
                        min_idx = i
                        min_distance = dis

                monster_x = cal_bottom_x(monster_box)
                monster_y = cal_bottom_y(monster_box)
                player_x = cal_bottom_x(self.player_xywh)
                player_y = cal_bottom_y(self.player_xywh)    

                # 处于攻击距离
                if abs(player_x - monster_x) < attx and abs(player_y - monster_y) < atty:
                    # zhuanshen
                    if monster_x - player_x > 0 : # 右侧
                        self.control.turn("RIGHT")
                    else:
                        self.control.turn("LEFT")

                    prob = random.randint(0,10)
                    if prob < 8:
                        self.normal_attack()

                    if self.game_map.is_special_room():
                        idx = random.randint(0,len(self.skill_list)-1)
                        self.release_skill(idx)
                        details = f"RELEASED sp skill"
                        self.now_action += f" [{details}]"

                    if len(self.skill_list)>0:
                        idx = random.randint(0,len(self.skill_list)-1)
                        self.release_skill(idx)
                        details = f"RELEASED {idx} SKILL ATTACK MONSTER {monster_name}"
                        self.now_action += f" [{details}]"


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

                    direction = direct(directs)

                    details = f"GO {direction} TO FIND {monster_name}"
                    self.now_action += f" [{details}]"
                    # key_status, directions = self.control.direction_move(direct=d, to_release=self.to_release)
                
                
            elif len(items_seen) > 0:
                self.now_action = "COLLECTING ITEMS"

                min_distance = float("inf")
                # 遍历物品
                for i in range(len(items_seen)):
                    cls_name, item_xywh = items_seen[i]
                    dis = cal_distance_bottom(self.player_xywh, item_xywh)
                    if dis < min_distance:
                        item_box = item_xywh
                        item_name = cls_name
                        min_idx = i
                        min_distance = dis
                
                if abs(item_box[1] - self.player_xywh[1]) > 0 or abs(item_box[0] - self.player_xywh[0]) > 0:

                    # directs = [0,0,0,0] # left, right, up, down

                    if item_box[0] - self.player_xywh[0] > thx:
                        # 右侧
                        directs[1] = 1
                    else:
                        # 左侧
                        directs[0] = 1

                    if item_box[1] - self.player_xywh[1] > thy:
                        # 下侧
                        directs[3] = 1
                    else:
                        # 上侧
                        directs[2] = 1


                    direction = direct(directs)
                    
                    details = f"GO {direction} TO COLLECT {item_name}"
                    self.now_action += f" [{details}]"
                    # key_status, directions = self.control.direction_move(direct=d, to_release=self.to_release)
            


            # 跟随提示
            else:
                if self.get_reward:
                    round_completed = True
  
                elif self.game_map:
                    direction = self.where_to_go(open_door_seen, self.player_xywh)

                elif len(direct_hints_seen) > 0:
                    self.now_action = "FOLLOWING ROOM HINTS"
                    cls_name, hint_xywh = direct_hints_seen[0]
                    direct_hint = cls_name.split("_")[1] if len(cls_name.split("_")) > 1 else None

                    hint_x = cal_center_x(hint_xywh)
                    hint_y = cal_center_y(hint_xywh)
                    player_x = cal_center_x(self.player_xywh)
                    player_y = cal_center_y(self.player_xywh)

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
                        direction = direct(directs)
                        
                    details = f"MOVING {direct_hint} TO ENTRY DOOR"
                    self.now_action += f" [{details}]"
                    # key_status, directions = self.control.direction_move(direct=d, to_release=self.to_release)



                #     if direct_hint:
                #         where_to_go(open_door_seen, self.player_xywh, action_cache, path,directkeys,hint_xywh=hint_xywh)

                # # 跟随提示
                elif len(hints_seen) > 3:
                    self.now_action = "FOLLOWING HINTS"
                    min_distance = float("inf")
                    min_sec_distance = float("inf")
                    direct_hint = None

                    distance_list = []


                    for i in range(len(hints_seen)):
                        cls_name, hint_xywh = hints_seen[i]
                        distance = cal_distance_bottom(self.player_xywh, hint_xywh)
                        distance_list.append((i, distance))
                    sorted_distance = sorted(distance_list, key=lambda x: x[1])

                    min_sec_distance_id = sorted_distance[1][0]
                    hint_name, hint_box = hints_seen[min_sec_distance_id]
                    

                    hint_x = cal_center_x(hint_box)
                    hint_y = cal_center_y(hint_box)
                    player_x = cal_bottom_x(self.player_xywh)
                    player_y = cal_bottom_y(self.player_xywh)


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
                        direction = direct(directs)
                        
                    details = f"REMAIN {len(hints_seen)} HINTS"
                    self.now_action += f" [{details}]"
                    # key_status, directions = self.control.direction_move(direct=d, to_release=self.to_release)

                # else:
                    # self.control.direction_move(direct=d, to_release=self.to_release)


                # where_to_go(open_door_seen, self.player_xywh, action_cache, path,directkeys)

            if self.last_action != self.now_action:
                self.last_action = self.now_action

                
        else:
            # 随机移动以找到角色位置
            pass
            # action = [direct_dic[key] for key in direct_dic.keys()][random.randint(0,len(direct_dic)-1)]
            # directkeys.key_press(action)

        return self.last_action + f"[special room: {self.game_map.is_special_room()}]", direction


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

    def where_to_go(self, door_seen, player_xywh, thx=100, thy=100):
            path = self.game_map.game_path

            self.now_action = "FINDING WAY"
            details = ""
            door_directions = []
            doors_xywh = []

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
                directs = self.game_map.path_fit(path)

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
                # control.direction_move(direct=d, to_release=self.to_release)
 
            else:
                details += f" STOPPED"
            self.now_action += f" [{details}]]"
            return d
        



    