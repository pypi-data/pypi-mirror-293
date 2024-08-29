import pygame
from hellopy.gameobject.gameobject import GameObject, rotate_point
from hellopy.collision import CollisionComponent
from hellopy.window import window

# 多边形函数
def polygon(*arg):  
    if arg:
        if isinstance(arg[-1], str) or isinstance(arg[-1], tuple) :
            color = arg[-1]
            p_list = convert2list(arg[:len(arg)-1])
        else:
            color = "orange"
            p_list = convert2list(arg)
    else:
        color = "green"
        p_list = convert2list(arg)
    pygame.draw.polygon(window.screen,color,p_list)

def convert2list(points):
    if len(points) < 6:
        print("坐标参数少于6个，将使用默认坐标")
        return [(100,50),(200,60),(210,160),(110,170)]
    if len(points) % 2 == 1:
        print("坐标参数为奇数个，最后一个参数将被忽略")
        points = tuple(points[:len(points)-1])
    p_list = []
    for i in range(0, len(points)-1, 2):
        p_list.append((points[i],points[i+1]))
    return p_list

# 多边形类
class Polygon(GameObject,CollisionComponent):
    def __init__(self,points=[(100,50),(200,60),(210,160),(110,170)],color="red"):
        self.points = points
        super().__init__(self.get_rect())
        self.color = color
        self.outline_color = "blue"
        self.scale = 1
        self.line_width = 1
        self.angle = 0
        self._x = self.get_center()[0]
        self._y = self.get_center()[1]
        self._w = self.get_rect()[2]
        self._h = self.get_rect()[3]
        self.v_from_center = self.get_vectors()
        self.show_outline = False
        self.is_moving = False
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,x):
        if self._x != x:
            self._x = x
            self.is_moving = True
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,y):
        if self._y != y:
            self._y = y
            self.is_moving = True

    def get_vectors(self):
        nps=[]
        for p in self.points:
            nps.append((p[0]-self.x, p[1]-self.y))
        return nps
    def get_rect(self):
        x_list = []
        y_list = []
        for dot in self.points:
            x_list.append(dot[0])
            y_list.append(dot[1])
        return (min(x_list),min(y_list),max(x_list)-min(x_list),max(y_list)-min(y_list))
    def draw(self):
        if self.is_moving:
            self.update_points()
        pygame.draw.polygon(window.screen,self.color,self.points)
        if self.show_outline:
            pygame.draw.polygon(window.screen,self.outline_color,self.points,self.line_width)
    def stroke(self):
        self.update_points()
        pygame.draw.polygon(window.screen,self.color,self.points,self.line_width)
    def update_points(self):
        # 更新位置
        nps = []
        for p in self.v_from_center:
            nps.append((self.x+p[0]*self.scale,self.y+p[1]*self.scale))
        self.points = nps.copy()
    def get_center(self):
        x_list = []
        y_list = []
        for dot in self.points:
            x_list.append(dot[0])
            y_list.append(dot[1])
        return (sum(x_list)//len(x_list), sum(y_list)//len(y_list))
    
    def rotate(self,angle=90,rotate_center=None):
        # 旋转一个角度
        rc = (self.x,self.y)
        if rotate_center != None:
            rc = rotate_center
        nc = rotate_point(rc,(self.x,self.y),angle)
        self.x = nc[0]
        self.y = nc[1]
        nps = []
        for p in self.v_from_center:
            nps.append(rotate_point((0,0),p,angle))
        self.v_from_center = nps.copy()
        self.angle = (self.angle + angle) % 360
    def rotate_to(self,angle=90,rotate_center=None):
        # 旋转到某个角度
        a = (angle - self.angle)
        rc = (self.x,self.y)
        if rotate_center != None:
            rc = rotate_center
        nc = rotate_point(rc,(self.x,self.y),a)
        nps = []
        for p in self.v_from_center:
            nps.append(rotate_point((0,0),p,a))
        self.v_from_center = nps.copy()
        self.angle = angle % 360
    def set_scale(self,scale):
        if self.scale == scale:
            return

        nps = []
        for p in self.v_from_center:
            nps.append((self.x+p[0]*self.scale,self.y+p[1]*self.scale))
        self.points = nps.copy()
        self.is_moving = True