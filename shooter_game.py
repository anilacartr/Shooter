from pygame import *
from random import randint
from time import time as timer

#Fontlar ve yazılar
font.init()
font1 = font.Font(None,80)
win = font1.render("YOU WIN!",True,(255,255,255))
lose = font1.render("YOU LOSE!",True,(180,0,0))
font2 = font.Font(None,36)



#Arka plan Müziği
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

#Görsellerin tanımlanması
img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_bullet = "bullet.png"
img_ast = "asteroid.png"

score = 0 #Vurulan gemiler
lost = 0 # Kaçırılan gemiler
max_lost = 3 # Kaçırılabilecek maksimum düşman sayısı

#Sprite için süper sınıfı oluşturuyoruz
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)

        self.image= transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        if self.rect.y < 0 :
            self.kill()

bullets = sprite.Group()
   
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y  > win_height :
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost + 1

win_width = 700
win_height = 500
display.set_caption("Shooter Game")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back),(win_width,win_height))

ship = Player(img_hero,5,win_height-100,80,100,10)

monters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monters.add(monster)

astreoids = sprite.Group()
for i in range(1,3):
    astreoid = Enemy(img_ast,randint(30,win_width-30),-40,80,50,randint(1,7))
    astreoids.add(astreoid)


finish = False

run = True

rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE :
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        #Arka planı güncelliyoruz
        window.blit(background,(0,0))
        #Ekrana metin yazıyoruz
        text = font2.render("Score : "+str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render("Lost   : "+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        #Sprite hareketini üretiyoruz
        ship.update()
        monters.update()
        bullets.update()

        #Döngünün her yenilenmesinde onları yeni bir konumda güncelliyoruz
        ship.reset()
        monters.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3 :
                reload = font2.render("Wait,reload...",1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False


        # Mermi ve canavarların çarpışması
        collides = sprite.groupcollide(monters,bullets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monters.add(monster)
        #Muhtemel Kaybetme Durumu
        if sprite.spritecollide(ship,monters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        #Kazanma Durumu
        if score >= 9:
            finish = True
            window.blit(win,(200,200))      
        display.update()
    else:
        finish = False
        score = 0 
        lost = 0
        for b in bullets:
            b.kill()
        for m in monters:
            m.kill()
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monters.add(monster)

    time.delay(50)

