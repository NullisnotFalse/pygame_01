import pygame
import random
import time
import math
from datetime import datetime


class Player:
    hp = 100
    power = 30
    alive = True
    max_hp = hp

    def __init__(self, name):
        self.name = name

    def attack(self, other):
        damage = random.randint(self.power - 2, self.power + 2)
        other.hp = max(other.hp - damage, 0)
        print(f"{self.name}의 공격! {other.name}에게 {damage}의 데미지를 입혔습니다.")
        if other.hp == 0:
            print(f"{other.name}이(가) 쓰러졌습니다.")
            other.alive = False

    def magic_attack(self, other):
        damage = random.randint(self.power * 2 - 5, self.power * 2 + 5)
        other.hp = max(other.hp - damage, 0)
        print(f"{self.name}의 마법 공격! {other.name}에게 {damage}의 데미지를 입혔습니다.")
        if other.hp == 0:
            print(f"{other.name}이(가) 쓰러졌습니다.")
            other.alive = False

    def show_status(self):
        print(f"{self.name}의 상태: HP {self.hp}/{self.max_hp}")


class Enemy:
    alive = True

    def __init__(self, name, hp, power):
        self.name = name
        self.hp = hp
        self.power = power
        self.max_hp = self.hp

    def attack(self, other):
        damage = random.randint(self.power - 2, self.power + 2)
        other.hp = max(other.hp - damage, 0)
        print(f"{self.name}의 공격! {other.name}에게 {damage}의 데미지를 입혔습니다.")
        if other.hp == 0:
            print(f"{other.name}이(가) 쓰러졌습니다.")
            other.alive = False

    def show_status(self):
        print(f"{self.name}의 상태: HP {self.hp}/{self.max_hp}")


name = input("이름을 입력해주세요 : ")
player = Player(name)
codus = Enemy("갓채연", 200, 25)

while player.alive and codus.alive:
    attack_type = input("어떤 공격을 사용하시겠습니까? (일반/마법): ")
    if attack_type == "일반":
        player.attack(codus)
        codus.show_status()
    elif attack_type == "마법":
        player.magic_attack(codus)
        codus.show_status()
    else:
        print("잘못된 입력입니다. 다시 입력해주세요.")
        continue
    if not codus.alive:
        break
    codus.attack(player)
    player.show_status()

print("전투가 끝났습니다!")

time.sleep(0.5)

temp = input("ENTER KEY를 눌러주세요.")


# 1. 게임 초기화
pygame.init()

# 2. 게임창 옵션 설정
size = [1200, 667]
screen = pygame.display.set_mode(size)

title = ""
pygame.display.set_caption(title)

# 3. 게임 내 필요한 설정
clock = pygame.time.Clock()


class Obj:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.move = 0
        self.dir = "down"

    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
        else:
            self.img = pygame.image.load(address)
            self.sx, self.sy = self.img.get_size()

    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size()

    def show(self):
        screen.blit(self.img, (self.x, self.y))


def crash(a, b):
    if (a.x - b.sx <= b.x) and (b.x <= a.x + a.sx):
        if (a.y - b.sy <= b.y) and (b.y <= a.y + a.sy):
            return True
        else:
            return False
    else:
        return False


background = pygame.image.load("./img/background1200_667.JPG")


left_go = False
right_go = False
up_go = False
down_go = False
space_go = False
missile_list = []
enemy_list = []
direction = "down"

black = (0, 0, 0)
white = (255, 255, 255)
frame = 0

go = 0
kill = 0
loss = 0

name = ""

# 4-0. 게임 시작 대기 화면
quit_code = 0
while quit_code == 0:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                name = "sehee"
                quit_code = 1
            if event.key == pygame.K_RIGHT:
                name = "chaeyeon"
                quit_code = 1
    screen.fill(black)
    font = pygame.font.Font("./font/ariblk.ttf", 25)
    text1 = font.render("← → ↑ ↓ + space bar",
                        True, (255, 255, 255))
    screen.blit(text1, (round(size[0]/2 - 150), 150))
    text2 = font.render("PRESS LEFT KEY OR RIGHT KEY TO CHOOSE CHARACTER",
                        True, (255, 255, 255))
    screen.blit(text2, (round(size[0]/2 - 400), 200))
    sehee_img = pygame.image.load("./img/sehee_down.png").convert_alpha()
    screen.blit(sehee_img, (round(size[0]/2 - 300), 340))
    chaeyeon_img = pygame.image.load("./img/chaeyeon_down.png").convert_alpha()
    screen.blit(chaeyeon_img, (round(size[0]/2 + 80), 300))
    pygame.display.flip()


ss = Obj()
if name == "sehee":
    ss.put_img("./img/sehee_down.png")
elif name == "chaeyeon":
    ss.put_img("./img/chaeyeon_down.png")
ss.change_size(37, 50)
ss.x = round(size[0]/2) - round(ss.sx/2)
ss.y = round(size[1]/2) - round(ss.sy/2)
ss.move = 7


# 4. 메인 이벤트
start_time = datetime.now()
quit_code = 0
while quit_code == 0:

    # 4-1. FPS설정
    clock.tick(60)

    # 4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_code = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if name == "sehee":
                    ss.put_img("./img/sehee_left.png")
                elif name == "chaeyeon":
                    ss.put_img("./img/chaeyeon_left.png")
                ss.change_size(40, 50)
                left_go = True
                direction = "left"
            elif event.key == pygame.K_RIGHT:
                if name == "sehee":
                    ss.put_img("./img/sehee_right.png")
                elif name == "chaeyeon":
                    ss.put_img("./img/chaeyeon_right.png")
                ss.change_size(40, 50)
                right_go = True
                direction = "right"
            elif event.key == pygame.K_UP:
                if name == "sehee":
                    ss.put_img("./img/sehee_up.png")
                elif name == "chaeyeon":
                    ss.put_img("./img/chaeyeon_up.png")
                ss.change_size(40, 50)
                up_go = True
                direction = "up"
            elif event.key == pygame.K_DOWN:
                if name == "sehee":
                    ss.put_img("./img/sehee_down.png")
                elif name == "chaeyeon":
                    ss.put_img("./img/chaeyeon_down.png")
                ss.change_size(40, 50)
                down_go = True
                direction = "down"
            elif event.key == pygame.K_SPACE:
                space_go = True
                frame = 0

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_go = False
            elif event.key == pygame.K_RIGHT:
                right_go = False
            elif event.key == pygame.K_UP:
                up_go = False
            elif event.key == pygame.K_DOWN:
                down_go = False
            elif event.key == pygame.K_SPACE:
                space_go = False

    # 4-3. 입력, 시간에 따른 변화
    current_time = datetime.now()
    delta_time = round((current_time - start_time).total_seconds())

    if left_go:
        ss.x -= ss.move
        if ss.x <= 0:
            ss.x = 0
    elif right_go:
        ss.x += ss.move
        if ss.x >= size[0]-ss.sx:
            ss.x = size[0]-ss.sx
    elif up_go:
        ss.y -= ss.move
        if ss.y <= 0:
            ss.y = 0
    elif down_go:
        ss.y += ss.move
        if ss.y >= size[1]-ss.sy:
            ss.y = size[1]-ss.sy

    if space_go == True and frame % 15 == 0:

        if direction == "up":
            mm = Obj()
            if name == "sehee":
                mm.put_img("./img/beam_up.png")
            elif name == "chaeyeon":
                mm.put_img("./img/mint_choco_up.png")
            mm.change_size(20, 30)
            mm.x = round(ss.x + ss.sx/2 - mm.sx/2)
            mm.y = ss.y - mm.sy - 5
            mm.move = 15
            mm.dir = "up"
            missile_list.append(mm)

        if direction == "down":
            mm = Obj()
            if name == "sehee":
                mm.put_img("./img/beam_down.png")
            elif name == "chaeyeon":
                mm.put_img("./img/mint_choco_down.png")
            mm.change_size(20, 30)
            mm.x = round(ss.x + ss.sx/2 - mm.sx/2)
            mm.y = ss.y + mm.sy + 5
            mm.move = 15
            mm.dir = "down"
            missile_list.append(mm)

        if direction == "left":
            mm = Obj()
            if name == "sehee":
                mm.put_img("./img/beam_left.png")
            elif name == "chaeyeon":
                mm.put_img("./img/mint_choco_left.png")
            mm.change_size(30, 20)
            mm.x = ss.x - mm.sx - 5
            mm.y = round(ss.y + ss.sy/2 - mm.sy/2)
            mm.move = 15
            mm.dir = "left"
            missile_list.append(mm)

        if direction == "right":
            mm = Obj()
            if name == "sehee":
                mm.put_img("./img/beam_right.png")
            elif name == "chaeyeon":
                mm.put_img("./img/mint_choco_right.png")
            mm.change_size(30, 20)
            mm.x = ss.x + mm.sx + 5
            mm.y = round(ss.y + ss.sy/2 - mm.sy/2)
            mm.move = 15
            mm.dir = "right"
            missile_list.append(mm)

    frame += 1

    delete_list = []
    for i in range(len(missile_list)):
        m = missile_list[i]
        if m.dir == "up":
            m.y -= m.move
        elif m.dir == "down":
            m.y += m.move
        elif m.dir == "left":
            m.x -= m.move
        elif m.dir == "right":
            m.x += m.move

        if not -m.sy < m.y <= size[1] + m.sy or not -m.sx < m.x <= size[0] + m.sx:
            delete_list.append(i)

    delete_list.sort()
    for d in reversed(delete_list):
        del missile_list[d]

    if random.random() > 0.95:
        ee = Obj()
        if name == "sehee":
            ee.put_img("./img/hanmariyang_down.png")
        elif name == "chaeyeon":
            ee.put_img("./img/beam_up.png")
        ee.change_size(35, 50)
        ee.x = random.choice([
            random.randrange(0, size[0] - ee.sx - round(ss.sx/2)),
            random.randrange(0, size[0] - ee.sx - round(ss.sx/2)),
            10, size[0] - 10])
        if (ee.x == 10) or (ee.x == size[0] - 10):
            ee.y = random.randrange(0, size[1] - ee.sy - round(ss.sy/2))
        else:
            ee.y = random.choice([10, size[1] - 10])
        ee.move = max(math.floor(kill/20) + 1, math.floor(delta_time/20 + 1))
        if ee.x == 10:
            ee.dir = "right"
        elif ee.x == size[0] - 10:
            ee.dir = "left"
        elif ee.y == 10:
            ee.dir = "down"
        elif ee.y == size[1] - 10:
            ee.dir = "up"
        enemy_list.append(ee)

    delete_list = []
    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if e.dir == "up":
            e.y -= e.move
        elif e.dir == "down":
            e.y += e.move
        elif e.dir == "left":
            e.x -= e.move
        elif e.dir == "right":
            e.x += e.move

        if not -e.sy < e.y <= size[1] + e.sy or not -e.sx < e.x <= size[0] + e.sx:
            delete_list.append(i)

    delete_list.sort()
    for d in reversed(delete_list):
        del enemy_list[d]
        loss += 1

    delete_missile_list = []
    delete_enemy_list = []
    for i in range(len(missile_list)):
        for j in range(len(enemy_list)):
            m = missile_list[i]
            e = enemy_list[j]
            if crash(m, e) == True:
                delete_missile_list.append(i)
                delete_enemy_list.append(j)
    delete_missile_list = list(set(delete_missile_list))
    delete_enemy_list = list(set(delete_enemy_list))

    delete_missile_list.sort()
    for dm in reversed(delete_missile_list):
        del missile_list[dm]

    delete_enemy_list.sort()
    for de in reversed(delete_enemy_list):
        del enemy_list[de]
        kill += 1

    for i in range(len(enemy_list)):
        e = enemy_list[i]
        if crash(e, ss):
            quit_code = 1
            go = 1
    # 4-4. 그리기
    screen.blit(background, (0, 0))
    ss.show()
    for m in missile_list:
        m.show()
    for e in enemy_list:
        e.show()

    font = pygame.font.Font("./font/ariblk.ttf", 20)
    text_kill = font.render("killed : {}  loss : {}".format(
        kill, loss), True, (255, 255, 0))
    screen.blit(text_kill, (10, 5))

    text_time = font.render("time : {}".format(
        delta_time), True, (255, 255, 255))
    screen.blit(text_time, (size[0] - 100, 5))

    # 4-5. 업데이트
    pygame.display.flip()

# 5. 게임 종료
while go == 1:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            go = 0
    font = pygame.font.Font("./font/ariblk.ttf", 60)
    text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(text, (round(size[0]/2 - 220), round(size[1]/2 - 100)))
    font = pygame.font.Font("./font/ariblk.ttf", 30)
    text_kill = font.render("killed : {}  loss : {}".format(
        kill, loss), True, (255, 255, 255))
    screen.blit(text_kill, (round(size[0]/2 - 160), round(size[1]/2)))
    text_time = font.render("time : {}".format(
        delta_time), True, (255, 255, 255))
    screen.blit(text_time, (round(size[0]/2 - 80), round(size[1]/2 + 30)))
    text = font.render("SPECIAL THANKS TO", True, (255, 255, 0))
    screen.blit(text, (round(size[0]/2 - 180), round(size[1]/2 + 100)))
    text = font.render(
        "\"LEE SE HEE\" AND \"SEO CHAE YEON\"", True, (255, 255, 0))
    screen.blit(text, (round(size[0]/2 - 330), round(size[1]/2 + 150)))
    text = font.render("AND \"HANMARIYANG\"", True, (255, 255, 0))
    screen.blit(text, (round(size[0]/2 - 180), round(size[1]/2 + 200)))
    pygame.display.flip()
pygame.quit()
