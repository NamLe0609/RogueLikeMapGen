import random

from numpy import tile

from entity import Entity
from room_management import *
import tile_types
from game_map import GameMap 

class Node:
    def __init__(self, x: int, y: int, width: int, height: int, room_min_dimension: int):
        self._left = None
        self._right = None
        
        self._x = x
        self._y = y
        self._x2 = x + width
        self._y2 = y + height
        self._width = width
        self._height = height
        self._room_min_dimension = room_min_dimension
        self.__room = None
        
    #Public
    def create_room(self, dungeon: GameMap, standalone: bool) -> None:
        #Recursively call function until node with no children found
        if (self._left != None) or (self._right != None):
            if (self._left != None):
                self._left.create_room(dungeon, standalone)
            if (self._right != None):
                self._right.create_room(dungeon, standalone)
            
            #Connect left and right children's dungeon
            if (self._left != None) and (self._right != None):
                for x, y in tunnel_between((self._left.__get_room().center), (self._right.__get_room().center)):
                    dungeon.tiles[x, y] = tile_types.floor
        
        #Generate a room based on the node size and place them
        #in an appropriate place within the room
        else:
            room_width = random.randint(self._room_min_dimension - 1, self._width - 1)
            room_height = random.randint(self._room_min_dimension - 1, self._height - 1)
            room_x = random.randint(self._x, self._x2 - room_width - 1)
            room_y = random.randint(self._y, self._y2 - room_height - 1)
            self.__room = RectangularRoom(room_x, room_y, room_width, room_height)
            if (standalone):
                dungeon.tiles[self.__room.inner] = tile_types.floor
            else:
                dungeon.tiles[self.__room.inner] = tile_types.wall
                
    #Public
    def create_subnode(self) -> None:
        #If node has dimensions greater than twice the minimum size, split
        #call this function onto the children
        if self.__split():
            self._left.create_subnode()
            self._right.create_subnode()
            
    #Public
    def place_character(self, player: Entity) -> None:
        #Place character in the center of a random room
        room = self.__get_room()
        if room != None:
            player.x, player.y = room.center
            print(f"Coordinate: {player.x}, {player.y}")
            print(f"Room center: {room.center}")
            print(f"Room top left and right: {room.x1}, {room.y1}")

    #Private
    def __split(self) -> bool:
        #Logic: Room size must be > min size =>
        #See which amount * constant dimension is enough for size,
        #then pick that as limit for cutting from both ends
        
        #Randomly choose direction for split
        splitVertical = bool(random.randint(0,1))
        
        #Check if ratio of room size is appropriate
        if (self._width > self._height) and (self._width / self._height >= 1.25):
            #If ratio of width to height is too big, split vertically
            splitVertical = True
        elif (self._height > self._width) and (self._height / self._width >= 1.25):
            #If ratio of height to width is too big, split width
            splitVertical = False
            
        #Calculate maximum coordinate which can be split at
        max = (self._width if splitVertical else self._height) - self._room_min_dimension
        if max <= self._room_min_dimension:
            return False
        split_at = random.randint(self._room_min_dimension, max)
            
        if splitVertical:
            #Split vertically
            self._left = Node(self._x, self._y ,split_at, self._height, self._room_min_dimension)
            self._right= Node(self._x + split_at, self._y ,self._width - split_at, self._height, self._room_min_dimension)
        else:
            #Split horizontally
            self._left = Node(self._x, self._y, self._width, split_at, self._room_min_dimension)
            self._right = Node(self._x, self._y + split_at, self._width, self._height - split_at, self._room_min_dimension)
        return True

    #Private
    def __get_room(self) -> RectangularRoom:
        #Dig in all nodes down to their leaf to get a room
        #If two room are available, pick one randomly
        #Else return nothing
        if (self.__room != None):
            return self.__room
        else:
            if (self._left != None):
                left_room = self._left.__get_room()
            
            if (self._right != None):
                right_room = self._right.__get_room()
                
            if (left_room == None) and (right_room == None):
                return None
            elif left_room == None:
                return right_room
            elif right_room == None:
                return left_room
            elif random.randint(1,2) == 1:
                return left_room
            else:
                return right_room
            