from typing import List
import pygame, sys, random
import math

from scipy import rand

# Screen 
BLUE = (44, 176, 218)
screen_width = 1920
screen_height = 1080
screen =  pygame.display.set_mode((screen_width, screen_height))
# orbsim_icon = pygame.image.load('./images/orbsim_logo.png')

# pygame.display.set_icon(orbsim_icon)

earth = ['./earth3.png', './earth2.png']
class Sphere(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        rot_angle = 0
        while rot_angle < 360:
            self.sprites.append(pygame.image.load(f'./images/img_rotate_{rot_angle}_grades.png'))
            rot_angle += 15
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect =  self.image.get_rect()
        # print(self.rect)
        self.rect.topleft =  [pos_x, pos_y]
        self.rot_a = 0 
        self.rot_s = float(1.5) 
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.index = 1

    def update(self):
        if self.is_animating:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0 
            self.image = self.sprites[int(self.current_sprite)]
    
    def animate(self):
        self.is_animating = True
    
    def not_animate(self):
        self.is_animating = False
    # def draw(self, surface):
    #     surface.blit(self.rot_image, self.rect)

# class Crosshair(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__()
#         # self.image = pygame.image.load('./images/pointer.png')
#         self.rect = self.image.get_rect()
#         self.rect.center =[pos_x, pos_y]
#         # print(self.rect)
#         self.image.set_colorkey(( 255,   0, 255))

#     def shoot(self):
#         pass
#         pygame.sprite.spritecollide(crosshair, target_group, True)
#     def update(self) -> None:
#         self.rect.center = pygame.mouse.get_pos()
        
# class Target(pygame.sprite.Sprite):
#     def __init__(self, pos_x, pos_y):
#         super().__init__()
#         self.image = pygame.image.load('./big_rock.png')
#         self.rect = self.image.get_rect()
#         self.rect.center = [pos_x, pos_y]
#         self.image.set_colorkey(( 255,   0, 255))


class Junk(pygame.sprite.Sprite):
    
    def __init__(self, pos_x, pos_y, type: str, a, b, orbit_center, vel: int = 0.5):
        super().__init__()
        path = ''
        if type == 'rock':
            path = './images/rock1.png'
        if type == 'satellite':
            path = './images/satellite1.png'
        self.type =  type
        self.image =  pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        
        self.image.set_colorkey(( 255,   0, 255))
        self.orbit_angle = 0
        self.orbit_vel = vel
        self.a = a 
        self.b = b
        self.orbit_center = orbit_center
        self.selected =  False
    
    def update(self) -> None:
        nex_pos = next_point_moving_in_elipse(self.orbit_center,self.a, self.b, int(self.orbit_angle))
        self.rect.center = [nex_pos[0], nex_pos[1]]
        self.orbit_angle += self.orbit_vel
        if self.orbit_angle > 360:
            self.orbit_angle = 0
    
    def draw_points(self, screen, color = (255,255,255)):
        pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, 2,0)
        pygame.draw.circle(screen, (255, 255, 0), self.rect.bottomright, 2,0)

    def draw_selection(self, surface):
        
        if self.selected:
            pygame.draw.line(surface,BLUE, self.orbit_center, self.rect.center,2)
            pygame.draw.rect(surface,BLUE, self.rect,2)
    
    def change_selected(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.selected = not self.selected

class ElipticOrbit:
    def __init__(self, center, width, height):
        self.center = center
        self.size = (width, height)
        self.over_axis = 'x' if width > height else 'y'
        self.semi_major_axis = max(self.size)/2
        self.semi_minor_axis = min(self.size)/2
        self.focus = math.sqrt(self.semi_major_axis**2 - self.semi_minor_axis**2)
        if self.over_axis == 'x':
            self.vertex1 = (self.center[0] - self.semi_major_axis, self.center[1])
            self.vertex2 = (self.center[0] + self.semi_major_axis, self.center[1])
            self.covertex1 = (self.center[0], self.center[1] - self.semi_minor_axis)
            self.covertex2 = (self.center[0], self.center[1] + self.semi_minor_axis)
        else:
            self.vertex1 = (self.center[0], self.center[1] - self.semi_major_axis)
            self.vertex2 = (self.center[0], self.center[1] + self.semi_major_axis)
            self.covertex1 = (self.center[0] - self.semi_minor_axis, self.center[1])
            self.covertex2 = (self.center[0] + self.semi_minor_axis, self.center[1])
        self.rect = pygame.Rect(self.center[0]- width/2, self.center[1] - height/2, width, height)
        
    def __eq__(self, other: 'ElipticOrbit'):
        return self.semi_major_axis == other.semi_major_axis and self.semi_minor_axis == other.semi_minor_axis

    def draw_elipse(self, screen, color = (255,255,255)):
        pygame.draw.ellipse(screen, color,self.rect, 1)
        # pygame.draw.circle(screen, (255, 0, 0), self.vertex1, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.vertex2, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.covertex1, 4,0)
        # pygame.draw.circle(screen, (255, 0, 0), self.covertex2, 4,0)
        pygame.draw.circle(screen, (255, 255, 0), self.rect.topleft, 10,0)
        

def generate_orbits(center, number_of_orbits):
    orbits = []
    pointer = 0
    while pointer < number_of_orbits:
        
        width = random.randint(100,1000)
        height = random.randint(100,850)
        new_orbit = ElipticOrbit(center, width, height)
        if new_orbit in orbits:
            continue
        else:
            pointer +=1 
            orbits.append(new_orbit)
    return orbits
    
def generate_object_in_orbit(number_objects:int, orbit: 'ElipticOrbit')-> None:
    point = orbit.center
    objs = []
    for _ in range(number_objects):
        angle =  random.randint(0,360)
        a = orbit.semi_major_axis if orbit.over_axis == 'x' else orbit.semi_minor_axis
        b = orbit.semi_minor_axis if orbit.over_axis == 'x' else orbit.semi_major_axis
        vel =  random.random() *2
        type = random.randint(1,2)
        next_point = next_point_moving_in_elipse(point,  a, b, angle)
        junk = Junk(next_point[0], next_point[1], 'satellite' if type == 1 else 'rock', a, b, point, vel if vel > 0 else 0.1)
        objs.append(junk)
    return objs
pygame.init()
clock = pygame.time.Clock()



crosshair_group =  pygame.sprite.Group()
junks_group = pygame.sprite.Group()
target_group = pygame.sprite.Group()
earth_group = pygame.sprite.Group()

pygame.mouse.set_visible(False)
# background = pygame.image.load('./bg.jpg')
# for i in range (10):
crosshair = Crosshair(random.randint(0,1920),random.randint(0,1080))
crosshair_group.add(crosshair)
earth = Sphere(screen.get_rect().centerx, screen.get_rect().centery)
earth_group.add(earth)



def next_point_moving_in_elipse(point, a, b, degree):
    new_x = point[0] + (a*math.cos(degree * 2 * math.pi / 360))
    new_y = point[1] + (b*math.sin(degree * 2 * math.pi / 360))
    return (new_x, new_y)
# Importing the library
import pygame
  
# Initializing Pygame
pygame.init()
pygame.display.iconify
# Initializing surface
surface = pygame.display.set_mode((1920,1080))
  
# Initialing Color
color = (255,0,0)
rect: pygame.Rect =  pygame.Rect(screen.get_rect().centerx -512, screen.get_rect().centery - 541, 1024, 1024)
# print(rect.center)
# print(rect.bottomright)
# Drawing Rectangle

counting_l = 0

# for i in range(20):
#     new_target = Target(random.randrange(0, screen_width), random.randrange(0, screen_height))
#     target_group.add(new_target)
screen_center = (screen.get_rect().centerx, screen.get_rect().centery)
orbits: List['ElipticOrbit'] =  generate_orbits(screen_center, 8)


for o in orbits:
    new_obj = generate_object_in_orbit(4, o)
    junks_group.add(new_obj)

print(screen.get_rect().centerx, screen.get_rect().centery)
while True:
    # screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for o in junks_group.sprites():
                o.change_selected()
                
            # crosshair.shoot()
            # earth.animate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                earth.animate()
            if event.key == pygame.K_DOWN:
                earth.not_animate()
        
        # if event.type == pygame.K_SPACE:
        #     print('H1')
        # if event.type == pygame.K_DOWN:
        #     print('H2')
        # if event.type == pygame.K_UP:
        #     print('H3')
        # if event.type == pygame.K_a:
        #     print('JUI')
        #     earth.not_animate()
    # crosshair = Crosshair(random.randint(0,1920),random.randint(0,1080)) 
    # crosshair_group.add(crosshair)
    counting_l +=1
    if counting_l ==40:
        earth.not_animate()
    pygame.display.flip()
    screen.blit(background, (0,0))
    target_group.draw(screen)
    crosshair_group.draw(screen)
    earth_group.draw(screen)
    pygame.draw.rect(screen, color, rect,2)
    crosshair_group.update()
    junks_group.draw(screen)
    xRadius = 250
    yRadius = 100
    solo_una_vez = False
    # for degree in range(0,360,10):
    #     x1 = int(math.cos(degree * 2 * math.pi / 360) * xRadius) + 300
    #     y1 = int(math.sin(degree * 2 * math.pi / 360) * yRadius) + 150
    #     # if not solo_una_vez:
    #     #     print(x1,y1)
    #     #     solo_una_vez = True
    #     # screen.fill((0, 0, 0))
    # screen_center = (screen.get_rect().centerx, screen.get_rect().centery)
    # pygame.draw.circle(screen, (255, 0, 0), [300, 150], 35)
    # rect_elip = pygame.Rect(screen_center[0] - 300, screen_center[1] -100, 600, 200)
    # begin_point = (rect_elip.centerx-300, rect_elip.centery - 100)
    # pygame.draw.ellipse(screen, (0, 0, 0),rect_elip, 1)
    # for i in range(0,360, 5):
    #     new_point = next_point_moving_in_elipse(screen_center, 300, 100, i)
    #     pygame.draw.circle(screen, (255, 0, 0), new_point, 3,0)
    #     begin_point_a = (rect_elip.centerx-300, rect_elip.centery)
    #     begin_point_b = (rect_elip.centerx, rect_elip.centery-100)
       
    #     pygame.draw.circle(screen, (255, 0, 0), rect_elip.center, 3,0)
    #     pygame.draw.circle(screen, (255, 0, 0), begin_point, 4,0)
    #     pygame.draw.circle(screen, (255, 0, 0), begin_point_a, 4,0)
    #     pygame.draw.circle(screen, (255, 0, 0), begin_point_b, 4,0)
    #     pygame.draw.line(screen, (0,0,255), begin_point, begin_point_a)
    #     pygame.draw.line(screen, (0,0,255), screen_center, begin_point_a)
    #     pygame.draw.line(screen, (0,0,255), screen_center, begin_point)
    
    for o in orbits:
        o.draw_elipse(screen, (255,0,0))
    for o in junks_group.sprites():
        pygame.draw.circle(screen, (255,0,0), o.rect.center, 3, 1)
        o.draw_points(screen)
        o.draw_selection(screen)
        # pygame.C
        # pygame.draw.circle(screen, (0, 0, 255), [x1, y1], 15)
    junks_group.update()
    clock.tick(60)
    pygame.display.flip()
    earth_group.update()


