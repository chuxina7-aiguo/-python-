import pygame
from plane_sprites import *
import time

class PlaneGame(object):
    """飞机大战主游戏"""

    def __init__(self):
        print("游戏初始化")

        # 1. 创建游戏的窗口 画布的初始化
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        #pygame.display.set_mode() 是 Pygame 提供的函数，用于创建游戏窗口（画布）并返回一个 Surface 对象。
        # 2. 创建游戏的时钟    时间的初始化
        self.clock = pygame.time.Clock()

        # 3. 调用私有方法，精灵和精灵组的创建,也是初始化     精灵、精灵组的初始化
        self.__create_sprites()
        #私有方法的主要目的是限制该方法只能在类内部调用，不能从外部直接访问。

        # 4. 设置定时器事件 - 创建敌机　设定敌机的刷新时间为1s，
        # 英雄子弹事件的刷新频率为0.3秒
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)     #自定义事件 及 发生的频率
        pygame.time.set_timer(HERO_FIRE_EVENT, 300)

    def __create_sprites(self):         #创建了背景精灵和精灵组，敌机的精灵组以及英雄的精灵和精灵组。

        # 1.创建背景精灵和精灵组
        bg1 = Background()              #建立了两个对象 (相同的背景)
        bg2 = Background(True)          #在创建第二个背景对象时，通过传入 True 参数，来指定它是交替图像。

        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 2.创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 3.创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):      #游戏的主循环，设置了刷新帧率、事件监听、碰撞检测、更新/绘制精灵组和更新显示。
        print("游戏开始...")

        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)      #开始循环 设置刷新频率
            # 2. 事件监听
            self.__event_handler()              #开始事件监听 是否退出?是否敌人出现?是否开火?是否按键盘?
            # 3. 碰撞检测
            self.__check_collide()              #碰撞检测  调用框架接口去实现
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):   #私有方法 只能在While 中调用
                                 #用于处理事件，包括退出游戏、创建敌机、英雄开火和键盘控制英雄移动。
        for event in pygame.event.get():
            #pygame.event.get()用于从事件队列中获取所有待处理的事件。它返回一个包含所有未处理事件的列表。
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()

            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场...")
                # 创建敌机精灵
                enemy = Enemy()
                # 将敌机精灵添加到敌机精灵组
                self.enemy_group.add(enemy)     #只要调用这个组就可以让其所有对象都执行某个方法
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            #     print("向右移动...")

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT]:         #如果按了键盘就改变英雄的速度
            self.hero.speed = 8
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.speed = -8
        elif keys_pressed[pygame.K_UP]:
            self.hero.speed2 = -8
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.speed2 = 8
        else:
            self.hero.speed = 0
            self.hero.speed2 = 0



    def __check_collide(self):     #用于碰撞检测，判断子弹是否摧毁敌机以及敌机是否撞毁英雄。

        # 1. 子弹摧毁敌机  两个精灵组  中的所有精灵碰撞检测
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
                                                        #子弹会消失;敌机也会消失  不用检测
        # 2. 敌机撞毁英雄   某个精灵 和 指定精灵组 中的精灵的碰撞
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
                                                        #发生碰撞 指定精灵会被移除
        # 判断列表时候有内容
        if len(enemies) > 0:        #碰撞到
            # 让英雄牺牲
            self.hero.kill()
            m = "./sound/use_bomb.wav"
            pygame.mixer.music.load(m)
            pygame.mixer.music.play()
            time.sleep(3)
            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self): #用于更新和绘制精灵组，包括背景精灵组、敌机精灵组、英雄精灵组和英雄子弹精灵组。

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod           #一个装饰器，用于声明一个静态方法。
    def __game_over():              #用于游戏结束的处理，包括打印提示信息、关闭 Pygame窗口和退出进程。
        print("游戏结束")
    #可以直接通过类名调用 __game_over() 方法，而不需要创建 PlaneGame 类的实例。
        pygame.quit()
        exit()  #进程结束


if __name__ == '__main__':
    # 创建游戏对象
    pygame.init()
    game = PlaneGame()

    # 启动游戏
    game.start_game()
