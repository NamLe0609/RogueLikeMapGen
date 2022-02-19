import math
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
        
    def create_room(self, dungeon: GameMap) -> None:
        #Recursively call function until node with no children found
        if (self.left != None) or (self.right != None):
            if (self.left != None):
                self.left.create_room(dungeon)
            if (self.right != None):
                self.right.create_room(dungeon)
            
            if (self.left != None) and (self.right != None):
                for x, y in tunnel_between((self.left.__get_room().center), (self.right.__get_room().center)):
                    dungeon.tiles[x, y] = tile_types.floor
        
        #Generate a room based on the node size
        else:
            room_width = random.randint(1, self.width - 1)
            room_height = random.randint(1, self.height - 1)
            room_x = random.randint(self.x + 1, self.x2 - room_width)
            room_y = random.randint(self.y + 1, self.y2 - room_height)
            self.room = RectangularRoom(room_x, room_y, room_width, room_height)
            dungeon.tiles[self.room.inner] = tile_types.floor

        
    def __split(self, room_min_dimension: int) -> bool:
        #Logic: Room size must be > min size =>
        #See which amount * constant dimension is enough for size,
        #then pick that as limit for cutting from both ends
        
        #Randomly choose direction for split
        decision = random.randint(1,2)
        
        #Check if ratio of room size is appropriate
        if (self.width < self.height) and (self.width / self.height > 0.55):
            #If ratio of width to height is too small, split height
            decision = 1
        elif (self.height < self.width) and (self.height / self.width > 0.55):
            #If ratio of height to width is too small, split width
            decision = 2
            
        if decision == 1:
            #Split vertically
            min, max = room_min_dimension, self.width - room_min_dimension
            split_at = random.randint(min, max)
            self.left = Node(self.x, self.y ,split_at, self.height)
            self.right= Node(self.x + split_at, self.y ,self.width - split_at, self.height)
        elif decision == 2:
            #Split horizontally
            min, max = room_min_dimension, self.height - room_min_dimension
            split_at = random.randint(min, max)
            self.left = Node(self.x, self.y, self.width, split_at)
            self.right = Node(self.x, self.y + split_at, self.width, self.height - split_at)
    
    def create_subnode(self, room_min_dimension: int) -> None:
        #If node has dimensions greater than twice the minimum size, split
        #call this function onto the children
        if (self.width > room_min_dimension * 2) and (self.height > room_min_dimension * 2) :
            self.__split(room_min_dimension)
            self.left.create_subnode(room_min_dimension)
            self.right.create_subnode(room_min_dimension)
            
    def __get_room(self) -> RectangularRoom:
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
            

    """ def connect_room(self, dungeon: GameMap) -> GameMap:
        if (self.__has_offsprings()):
            #If children are leaves, connect the rooms toghether
            if (not self.left.__has_offsprings()) and (not self.right.__has_offsprings()):
                dungeon.tiles[self.left.room.inner] = tile_types.floor
                dungeon.tiles[self.right.room.inner] = tile_types.floor
                for x, y in tunnel_between((self.left.room.center), (self.right.room.center)):
                    dungeon.tiles[x, y] = tile_types.floor
                    
            #Else, recursively call connect_room on its children    
            else:
                self.left.connect_room(dungeon)
                self.right.connect_room(dungeon)
                
            
        return dungeon """
            
            
    #def _connect_room(self, dungeon: GameMap):