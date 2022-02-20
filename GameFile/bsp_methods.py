import math
from posixpath import split
import random
from turtle import right, width
from typing import List
from room_management import RectangularRoom
from room_management import *
import tile_types
from game_map import GameMap

class Node:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.left = None
        self.right = None
        
        self.x = x
        self.y = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.room = None
        
    def create_room(self, dungeon: GameMap, room_min_dimension: int) -> None:
        #Recursively call function until node with no children found
        if (self.left != None) or (self.right != None):
            if (self.left != None):
                self.left.create_room(dungeon, room_min_dimension)
            if (self.right != None):
                self.right.create_room(dungeon, room_min_dimension)
            
            if (self.left != None) and (self.right != None):
                for x, y in tunnel_between((self.left.__get_room().center), (self.right.__get_room().center)):
                    dungeon.tiles[x, y] = tile_types.floor
        
        #Generate a room based on the node size
        else:
            room_width = random.randint(room_min_dimension - 1, self.width - 1)
            room_height = random.randint(room_min_dimension - 1, self.height - 1)
            room_x = random.randint(self.x, self.x2 - room_width - 1)
            room_y = random.randint(self.y, self.y2 - room_height - 1)
            self.room = RectangularRoom(room_x, room_y, room_width, room_height)
            dungeon.tiles[self.room.inner] = tile_types.floor

        
    def __split(self, room_min_dimension: int) -> bool:
        #Logic: Room size must be > min size =>
        #See which amount * constant dimension is enough for size,
        #then pick that as limit for cutting from both ends
        
        #Randomly choose direction for split
        splitVertical = bool(random.randint(0,1))
        
        #Check if ratio of room size is appropriate
        if (self.width > self.height) and (self.width / self.height >= 1.25):
            #If ratio of width to height is too big, split vertically
            splitVertical = True
        elif (self.height > self.width) and (self.height / self.width >= 1.25):
            #If ratio of height to width is too big, split width
            splitVertical = False
            
        max = (self.width if splitVertical else self.height) - room_min_dimension
        if max <= room_min_dimension:
            return False
        split_at = random.randint(room_min_dimension, max)
            
        if splitVertical:
            #Split vertically
            self.left = Node(self.x, self.y ,split_at, self.height)
            self.right= Node(self.x + split_at, self.y ,self.width - split_at, self.height)
        else:
            #Split horizontally
            self.left = Node(self.x, self.y, self.width, split_at)
            self.right = Node(self.x, self.y + split_at, self.width, self.height - split_at)
        return True
    
    def create_subnode(self, room_min_dimension: int) -> None:
        #If node has dimensions greater than twice the minimum size, split
        #call this function onto the children
        if self.__split(room_min_dimension):
            self.left.create_subnode(room_min_dimension)
            self.right.create_subnode(room_min_dimension)
            
    def __get_room(self) -> RectangularRoom:
        #Dig in all nodes down to their leaf to get a room
        #If two room are available, pick one randomly
        #Else return nothing
        if (self.room != None):
            return self.room
        else:
            if (self.left != None):
                left_room = self.left.__get_room()
            
            if (self.right != None):
                right_room = self.right.__get_room()
                
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
