import os
from typing import List
import time
import cv2
import threading
class RoomNode:
    # 地图房间
    def __init__(self, room_id, neighbors=[-1,-1,-1,-1], 
                 left=None, right=None, up=None, down=None) -> None:
        self.room_id = room_id # 全地图唯一房间id
        self.neighbors = neighbors
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.is_entry = False
        self.is_boss = False

class RoomGraph:
    # 地图数据拓扑图
    def __init__(self, rooms:RoomNode, start_room:RoomNode, boss_room:RoomNode) -> None:
        self.rooms = rooms
        self.startRoom = start_room
        self.boosRoom = boss_room


class PathNode:
    # 路径节点
    def __init__(self, room=None, last=None, next=None) -> None:
        self.room = room
        self.last = last
        self.next = next
        self.visited = False # 已经过


class PathGraph:
    # 路径规划图
    def __init__(self, name, nodes:List[PathNode], path=None) -> None:
        self.nodes = nodes if nodes else []
        self.name = name
        self.direction = None
        self.begin = False
        self.locker = threading.Lock()
        self.inertia = False


        if len(nodes)>0:
            self.startNode = nodes[0]
            self.tailNode = nodes[-1]
            self.startNode.is_entry = True
            self.tailNode.is_boss = True

            self.curRoomId = 0 # 当前位置的room id
            self.curPathId = 0 # 当前位置的path id

        else:
            self.startNode = None
            self.tailNode = None
            self.curRoomId = -1
            self.curPathId = -1

        self.path = path # 地图遍历顺序
        rooms = [node.room.room_id for node in self.nodes]
        self.rooms = []
        for room in rooms:
            if room not in self.rooms:
                self.rooms.append(room)



    """获取当前位置节点"""
    def get_current_node(self)->PathNode:
        return self.nodes[self.curPathId]
        
    def get_path(self):
        return self.path
    

    # """
    # 获取当前节点的下一个节点
    # """
    # def next(self)->PathNode:
    #     if len(self.nodes) > 0 and self.tailNode.next != None:
    #         return self.tailNode.next
    #     else:
    #         return None
        
    # """
    # 返回目标节点的下一个节点
    # """
    # def next_node(self, node:PathNode)->PathNode:
    #     if node in self.nodes:
    #         if not node.is_boss:
    #             return self.node.next
    #     return None

    """从房间id获取当前path id"""
    def get_pathId_from_roomId(self, room_id:int)->int:

        for i in range(len(self.nodes)):
            node = self.nodes[i]
            if node.room.room_id == room_id:
                return i
        return -1

    """从房间id获取当前path node"""
    def get_node_from_roomId(self, room_id:int)->PathNode:
        for node in self.nodes:
            if node.room.room_id == room_id:
                return node
        return None

    """
    进入下一个节点
    """
    def step(self, start_room_id=-1)->bool:
        if not self.begin:
            self.begin = True
            self.curRoomId = start_room_id
            self.curPathId = self.get_pathId_from_roomId(start_room_id)
            print(f"进入地图，当前地图id:{self.curRoomId}，路径id:{self.curPathId}")
            time.sleep(0.3)
            return True

        if self.curPathId < len(self.path):
            self.curPathId += 1
            self.curRoomId = self.path[self.curPathId]
            self.nodes[self.curPathId].visited = True
            print(f"进入地图，当前地图id:{self.curRoomId}，路径id:{self.curPathId}")
            t = threading.Thread(
                target=self.wait_stop_worker
            )
            t.start()
            return True
        else:
            return False
    """
    进入上一个节点
    """
    def unstep(self, start_room_id=-1)->bool:
        if not self.begin:
            return False

        if self.curPathId < len(self.path):
            self.curPathId -= 1
            self.curRoomId = self.path[self.curPathId]
            self.nodes[self.curPathId].visited = True
            print(f"进入地图，当前地图id:{self.curRoomId}，路径id:{self.curPathId}")
            t = threading.Thread(
                target=self.wait_stop_worker
            )
            t.start()
            return True
        else:
            return False
        
    def is_waiting(self):
        with self.locker:
           inertia = self.inertia
        return inertia



    def wait_stop_worker(self):
        with self.locker:
            self.inertia = True
        time.sleep(1)
        with self.locker:
            self.inertia = False




def set_room(room:RoomNode, left:RoomNode, right:RoomNode, up:RoomNode, down:RoomNode):
    room.left = left
    room.right = right
    room.up = up
    room.down = down
    room.neighbors = [left.room_id if left else -1, right.room_id if right else -1, 
                      up.room_id if up else -1, down.room_id if down else -1]
    return room


def shanji(room_count=9)->PathGraph:
    # 山脊地图数据

    # 构建地图数据 9个房间：0-8
    rooms:List[RoomNode] = []
    for idx in range(room_count):
        rooms.append(RoomNode(idx))
    entry_room = rooms[0]
    entry_room.is_entry = True
    room1 = rooms[1]
    room2 = rooms[2]
    room3 = rooms[3]
    room4 = rooms[4]
    room5 = rooms[5]
    room6 = rooms[6]
    room7 = rooms[7]
    boss_room = rooms[-1]
    boss_room.is_boss = True

    entry_room = set_room(entry_room, None, None, room1, None)
    room1 = set_room(room1, None, room2, None, entry_room)
    room2 = set_room(room2, room1, room3, None, None)
    room3 = set_room(room3, room2, None, None, room4)
    room4 = set_room(room4, None, room5, room3, None)
    room5 = set_room(room5, room4, room6, room7, None)
    room6 = set_room(room6, room5, None, None, None)
    room7 = set_room(room7, None, boss_room, None, room5)
    boss_room = set_room(boss_room, room7, None, None, None)
    
    room_graph = RoomGraph(rooms, entry_room, boss_room)


    # 构建路径图
    path = [0, 1, 2, 3, 4, 5, 6, 5, 7, 8] # 进图顺序

    nodes:List[PathNode] = []
    for roomId in path:
        node = PathNode(room=rooms[roomId])
        nodes.append(node)

    for i in range(len(nodes)):
        node = nodes[i]
        node.last = nodes[i-1] if i>0 else None
        node.next = nodes[i+1] if i+1 < len(nodes) else None


    path_graph = PathGraph(name="shanji", nodes=nodes, path=path)
    special_room = 6
    return path_graph, special_room



def preprocess_image(image):
    # 转为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊降噪
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    # Setting parameter values 
    t_lower = 50  # Lower Threshold 
    t_upper = 150  # Upper threshold 
    
    # Applying the Canny Edge filter 
    edge = cv2.Canny(blurred_image, t_lower, t_upper) 

    # 应用自适应阈值处理
    processed_image = cv2.adaptiveThreshold(edge, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return processed_image


class GameMap:
    def __init__(self, name="", img_dir="") -> None:

        self.name = name
        self.img_dir = img_dir
        self.game_path = None
        self.maplist = self.load_map(img_dir=img_dir)
        self.last_id = -1
        self.special_room = -1


    def load_map(self, img_dir):
        exists = False
        # TODO map选择

        if self.name == "shanji":
            self.game_path, self.special_room = shanji()
            exists = True
        
        maplist = []
        if exists:
            try:

                for file in sorted(os.listdir(img_dir)):
                    img = cv2.imread(os.path.join(img_dir,file))
                    img = preprocess_image(img)
                    # img = cv2.resize(img, (50,50))
                    maplist.append(img)

            except Exception as e:
                print(e)
                exit()

        return maplist



    def get_map(self, img:cv2.Mat, ratio=(0.844,0.045,0.14))->cv2.Mat:
        # ratio: x y a

        shape = img.shape # h,w

        x = int(ratio[0] * shape[1])
        y = int(ratio[1] * shape[0])
        a = int(ratio[2] * shape[0])

        ret = img[y:y+a, x:x+a]
        ret = cv2.resize(ret, (200,200))

        return ret
    
    def is_special_room(self):
        return self.game_path.curPathId == self.special_room
            


    def mark_map(self, screenshot:cv2.Mat):

        best_match_score = -1
        best_match_map = None
        threshold = 0.35

        processed_img = preprocess_image(screenshot) 

        for i in range(len(self.maplist)):
            map_gray = self.maplist[i]
            result = cv2.matchTemplate(processed_img, map_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # print(i, max_val)


            # 更新最佳匹配
            if max_val > best_match_score:
                best_match_score = max_val
                best_match_map = i
        # print(best_match_map, best_match_score)
        if best_match_score > threshold:
            # print(best_match_map, best_match_score)

            h, w = self.maplist[i].shape[:2]
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            ret = screenshot.copy()
            ret = cv2.rectangle(ret, top_left, bottom_right, (255, 0, 0), 5)

            return best_match_map, ret
        else:
            # print(best_match_map, best_match_score)
            return -1, screenshot

    def get_room_id(self, img, _path:PathGraph=None):
        if _path is None:
            path = self.game_path
        else:
            path = _path

        map_img = self.get_map(img)
        id, res = self.mark_map(map_img)
        if id == -1:
            return id, res
        else:
            # 房间id改变了
            if self.last_id != id:
                # 避免识别错误导致的room id跳变
                last_node = path.get_current_node()
                if self.last_id >= 0 and last_node.next and last_node.next.room.room_id == id: 
                    path.step(id)
                    self.last_id = id
                    
                elif self.last_id >= 0 and last_node.last and last_node.last.room.room_id == id: 
                    path.unstep(id)
                    self.last_id = id
                elif self.last_id == -1 and path.begin == False:
                    path.step(id)
                    self.last_id = id


            return self.last_id, res


    def path_fit(self, path:PathGraph):
        directs = [0,0,0,0]

        if path:
            if path.name == "shanji":
                if path.curPathId == 0: # 第3张图要往shang靠
                    directs[2] = 1
                elif path.curPathId == 2: # 第2张图要往右靠
                    directs[1] = 1        
                elif path.curPathId == 3: # 第3张图要往右靠
                    directs[1] = 1
                elif path.curPathId == 4: # 第4张图要往右靠
                    directs[1] = 1
                elif path.curPathId == 5: # 第5张图要往右靠
                    directs[1] = 1
                elif path.curPathId == 6: # 第6张图要往左靠
                    directs[0] = 1
                elif path.curPathId == 7: # 第7张图要往左上
                    directs[0] = 1
                    directs[2] = 1
                else:
                    directs[1] = 1
        else:
            directs[1] = 1


        return directs

    def get_direction(self, path:PathGraph):
        node = path.get_current_node()
        next_node = node.next if node else None
        if next_node is None:
            return "STOP"
        if next_node.room == node.room.up:
            return "UP"
        elif next_node.room == node.room.down:
            return "DOWN"
        elif next_node.room == node.room.left:
            return "LEFT"
        elif next_node.room == node.room.right:
            return "RIGHT"
        else:
            # print(next_node.room_id)
            return "STOP"
        

class MapMaker:
    def __init__(self, path, name) -> None:
        import cv2
        self.path = path
        self.name = name
        self.imgs = []

    def capture(self):
        pass
    
    def undo(self):
        pass

    def preview(self):
        pass
    
