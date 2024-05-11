from gdpc import Editor, Block, geometry
from Enums import DIRECTION
from buildings.geometry.Point import Point
from buildings.geometry.Vertice import Vertice

class Tile:
    def __init__(self, size : int, position : tuple[int, int]):
        self.size = size
        x,z = position
        leng  = self.size-1
        self.pos = Point(x = x, z = z)
        
        self.has_vertice = False
        
        self.north_west = self.pos
        self.north_east = Point(x = self.pos.x + leng, z =self.pos.z)
        self.south_west = Point(x = self.pos.x, z = self.pos.z + leng)
        self.south_east = Point(x = self.pos.x + leng, z = self.pos.z + leng)
        
        self.west_neighbor = None
        self.east_neighbor = None
        self.north_neighbor = None
        self.south_neighbor = None
        
        self.west_vertice = None
        self.east_vertice = None
        self.north_vertice = None
        self.south_vertice = None
        
    def fill(self, editor : Editor, material : str, y : int, y2 : int = None) -> list[Point]:
        if y2 == None: y2 = y
        geometry.placeCuboid(editor, (self.pos.x, y, self.pos.z), (self.pos.x+self.size-1, y2, self.pos.z+self.size-1), Block(material))
        
    def get_neighbors_coords(self):
        return [Point(x = self.pos.x - self.size, z = self.pos.z), # west
                Point(x = self.pos.x + self.size, z = self.pos.z), # east
                Point(x = self.pos.x, z = self.pos.z - self.size), # north
                Point(x = self.pos.x, z = self.pos.z + self.size)] # south
        
            
    def get_neighbor(self, direction) -> Point:
        match(direction):
            case DIRECTION.WEST:
                return self.west_neighbor
            case DIRECTION.EAST:
                return self.east_neighbor
            case DIRECTION.NORTH:
                return self.north_neighbor
            case DIRECTION.SOUTH:
                return self.south_neighbor
            
    def set_neighbor(self, direction, neighbor : 'Tile'):
        match(direction):
            case DIRECTION.WEST:
                self.west_neighbor = neighbor
            case DIRECTION.EAST:
                self.east_neighbor = neighbor
            case DIRECTION.NORTH:
                self.north_neighbor = neighbor
            case DIRECTION.SOUTH:
                self.south_neighbor = neighbor
    
    def get_vertice(self,vertice : int|DIRECTION) -> Vertice:
        # gives the corresponding vertice : 
        # 0 = west, 1 = east, 2 = north, 3 = south
        match(vertice):
            case 0 :
                return Vertice(self.north_west, self.south_west, DIRECTION.WEST)
            case 1 :
                return Vertice(self.north_east, self.south_east, DIRECTION.EAST)
            case 2 :
                return Vertice(self.north_west, self.north_east, DIRECTION.NORTH)
            case 3 :
                return Vertice(self.south_west, self.south_east, DIRECTION.SOUTH)
            case DIRECTION.WEST :
                return self.west_vertice
            case DIRECTION.EAST :
                return self.east_vertice
            case DIRECTION.NORTH :
                return self.north_vertice
            case DIRECTION.SOUTH :
                return self.south_vertice
            
    def set_vertice(self, direction : DIRECTION, vertice : Vertice):
        self.has_vertice = True
        match(direction):
            case DIRECTION.WEST :
                self.west_vertice = vertice
            case DIRECTION.EAST :
                self.east_vertice = vertice
            case DIRECTION.NORTH :
                self.north_vertice = vertice
            case DIRECTION.SOUTH :
                self.south_vertice = vertice