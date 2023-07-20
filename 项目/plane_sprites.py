import random
import pygame

#pygame.sprite.Sprite 类是用于创建单个精灵对象的基类，而 pygame.sprite.Group 类是用于管理多个精灵对象的容器。
#它们共同构成了 Pygame 中精灵类和精灵组的重要组成部分，用于实现游戏中的元素管理和交互。

# 屏幕大小的常量对象
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量，为事件定义不同名字的常量，从而能够区分，从24算起
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件，为事件定义不同名字的常量，从而能够区分
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):         #一所有精灵类的基类，用于创建游戏中的精灵。
    """飞机大战游戏精灵"""
#传入 pygame.sprite.Sprite 是为了让 GameSprite 类成为它的子类，从而继承了 pygame.sprite.Sprite 类的属性和方法。
    def __init__(self, image_name, speed=1):
        # 调用父类的初始化方法        精灵的初始化方法
        super().__init__()

        # 定义对象的属性
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()       #获取图像的尺寸
        self.speed = speed

    def update(self):
        # 在屏幕的垂直方向上移动
        self.rect.y += self.speed       #两个背景 bg1,bg2 都同时移动

#GameSprite 类是一个基类，其他精灵类（Background、Enemy、Hero 和 Bullet）都继承自 GameSprite 类。
#这种继承关系使得其他精灵类可以共享 GameSprite 类中定义的属性和方法，避免了重复编写相同的代码.
#通过继承，子类可以拥有父类的属性和方法，并可以在子类中添加自己的特定行为或重写父类的方法。

class Background(GameSprite):    #继承自 GameSprite。负责创建背景精灵对象，并实现了背景图的垂直移动效果。
    """游戏背景精灵"""
    def __init__(self, is_alt=False):

        # 1. 调用父类方法  实现精灵的创建(image/rect/speed)
        super().__init__("./images/background.png")

        # 2. 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:      #bg2一开始为True 在bg1的上面
            self.rect.y = -self.rect.height
    #背景图 运动的情况
    def update(self):

        # 1. 调用父类的方法实现      调用父类 pygame.sprite.Sprite 的 update() 方法。
        super().update()        #可以调速度

        # 2. 判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):   #敌机精灵类，继承自 GameSprite。
    """敌机精灵"""          #它负责创建敌机精灵对象，并实现了敌机的垂直移动和随机位置、速度的设置。

    def __init__(self):
        # 1. 调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__("./images/enemy1.png")     #必须先执行父类

        # 2. 指定敌机的初始 随机速度 1 ~ 3
        self.speed = random.randint(1, 4)

        # 3. 指定敌机的初始随机位置
        self.rect.bottom = 0

        max_x = SCREEN_RECT.width - self.rect.width  #减去自身宽度 机身也需要占空间
        self.rect.x = random.randint(0, max_x)          #敌机随机出现的x轴方向的位置

    def update(self):
        # 1. 调用父类方法，保持垂直方向的飞行
        super().update()

        # 2. 判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            # print("飞出屏幕，需要从精灵组删除...")
            # kill方法可以将精灵从所有精灵组中移出，精灵就会被自动销毁
            self.kill()

    def __del__(self):
        # print("敌机挂了 %s" % self.rect)
        pass


class Hero(GameSprite):   #英雄精灵类，继承自 GameSprite。
    """英雄精灵"""          #负责创建英雄精灵对象，并实现了英雄的水平移动、发射子弹等功能。

    def __init__(self):

        # 1. 调用父类方法，设置image&speed
        super().__init__("./images/me1.png", 0)

        # 2. 设置英雄的初始位置
        self.rect.centerx = SCREEN_RECT.centerx     #初始在 centerx:自动计算 使其处于屏幕中间
        self.rect.bottom = SCREEN_RECT.bottom - 120

        # 3. 创建子弹的精灵组
        self.bullets = pygame.sprite.Group()      #可以提前调用 是因为主程序运行时 该代码已经全部被加载
#英雄精灵的子弹精灵组 英雄发射子弹时，会通过 self.bullets.add(bullet) 将子弹精灵添加到 self.bullets 精灵组中
    def update(self):

        # 英雄在水平方向移动
        self.rect.x += self.speed

        # 控制英雄不能离开屏幕
        if self.rect.x < 0:              # 限制不能越过左侧边界
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:        # 限制不能越过右侧边界
            self.rect.right = SCREEN_RECT.right

        #英雄在垂直方向移动
        self.rect.y += self.speed2

        if self.rect.y<0:           # 限制不能越过上边界
            self.rect.y =0
        elif self.rect.bottom > SCREEN_RECT.bottom:  # 限制不能越过下边界
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        print("发射子弹...")

        for i in (0, 1, 2):
#通过循环迭代，重复执行 3 次，从而创建了 3 颗子弹精灵，并设置它们的位置，并将它们添加到英雄精灵的子弹精灵组中。
#当英雄精灵调用 fire() 方法时，就会创建出 3 颗子弹，并形成一列垂直排列的子弹效果。
            # 1. 创建子弹精灵
            bullet = Bullet()       #每颗子弹都是一个对象 ; 一次发射3颗子弹

            # 2. 设置精灵的位置
            bullet.rect.bottom = self.rect.y - i * 20     #i的取值为 0,1,2
            #i以 20 的目的是将每个子弹的垂直位置相对于英雄精灵往上偏移 0、20、40 的距离，从而形成多个子弹的排列效果。
            bullet.rect.centerx = self.rect.centerx     #让子弹始终由英雄中心发出

            # 3. 将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):       #负责创建英雄精灵对象，并实现了英雄的水平移动、发射子弹等功能。
    """子弹精灵"""                #它负责创建子弹精灵对象，并实现了子弹的垂直移动和销毁功能。

    def __init__(self):
        # 调用父类方法，设置子弹图片，设置初始速度
        super().__init__("./images/bullet1.png", -5)

    def update(self):
        # 调用父类方法，让子弹沿垂直方向飞行
        super().update()

        # 判断子弹是否飞出屏幕
        if self.rect.bottom < 0:
            self.kill()

    def __del__(self):
         print("子弹被销毁...")

# 每个精灵对象都有自己的 update 方法，用于更新精灵的状态和位置。