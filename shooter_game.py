#Создай собственный Шутер

from pygame import *
from random import *
init()

win_widht = 700
win_hight = 500

window = display.set_mode((win_widht, win_hight))
display.set_caption("Шутер")
background = transform.scale(image.load('galaxy.jpg'),(win_widht, win_hight))

FPS = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self,image_sprite,img_x,img_y,speed):
        super().__init__()
        self.image = transform.scale(image.load(image_sprite), (65,65))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = img_x
        self.rect.y = img_y
        self.propysk = 0
    def show_s(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Hero(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed


    def fire (self):
        pyl = Pylya('bullet.png', self.rect.x, self.rect.y, 8)
        obgect_bullet.add(pyl)

class Pylya(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()
        

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed      
        global propysk
        if self.rect.y >= win_hight:
            self.rect.x = randint(80,win_widht -80)
            self.rect.y = 0
            propysk +=1
            
player = Hero('rocket.png',int( win_widht/2), win_hight- 80, 4)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()



monsters = sprite.Group()
obgect_bullet = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(80, win_widht- 40), win_hight, randint(1, 3 ))
    monsters.add(monster)

font.init()
font1 = font.Font(None,35)

font2 = font.Font(None, 35)

run = True
finish = False
propysk = 0
score = 0
while run:
    for e in event.get():
        if e.type ==  QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
    window.blit(background,(0,0))
    if finish != True:
        
        player.show_s()
        player.update()
        for i in monsters:
            i.show_s()
            i.update()
    
        for i in obgect_bullet:
            i.show_s()
            i.update()


        popadanie = sprite.groupcollide(monsters, obgect_bullet, True, True)
        for c in popadanie:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_widht - 80), -40, randint(1, 5))
            monsters.add(monster)
        kills = font1.render('Убито:' + str(score), True, (255, 255, 255))
        skip = font2.render('Пропущено ' + str(propysk), True,(255, 255, 255))

        if propysk >20:
            finish = True
        
        if score >= 40:
            finish = True


        window.blit(kills,(10,10))
        window.blit(skip,(10,40))

        display.update()
        
    else:
        propysk= 0
        score = 0
        finish = False
        player.show_s()
        for i in monsters:
            i.kill()   
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_widht- 40), win_hight, randint(1, 3 ))
            monsters.add(monster)
        time.delay(3000)
    display.update()
    FPS.tick(60)
