from typing import Iterator, Tuple
import random

#Object for rectangular room
class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        #Bottom right coordinate
        self.__x2 = x + width
        self.__y2 = y + height
        self.__size = width * height
        
    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.__x2) / 2)
        center_y = int((self.y1 + self.__y2) / 2)
        
        return center_x, center_y
        
    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of room as 2D array index."""
        return slice(self.x1 + 1, self.__x2), slice(self.y1 + 1, self.__y2)
    
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between two chosen points."""
    x1, y1 = start
    x2, y2 = end
    
    #Reverse step if starting coords larger than ending coords
    stepx = 1
    if x1 > x2:
        stepx = -1
    stepy = 1
    if y1 > y2:
        stepy = -1
    
    option = random.randint(1, 2)
    #Horizontal then vertical
    if option == 1:
        currentx = x1
        for x in range(x1, x2 + 1, stepx):
            yield x, y1
            currentx = x
        for y in range(y1, y2 + 1, stepy):
            yield currentx, y
    #Vertical then horizontal
    else:
        currenty = y1
        for y in range(y1, y2 + 1, stepy):
            yield x1, y
            currenty = y
        for x in range(x1, x2 + 1, stepx):
            yield x, currenty