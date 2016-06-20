
import kivy
kivy.require('1.0.6')
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '717')
import time
from kivy.app import App
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty,ListProperty, BooleanProperty,StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.core.window import Window
from random import randrange, randint
from kivy.uix.image import Image
from math import radians,cos,sin,sqrt
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.audio import SoundLoader
root = Builder.load_file('My360.kv')
circle_path = 'circle.png'
white_circle_path = 'white_circle.png'
grey_circle_path = 'grey_circle.png'
big_grey_circle_path = 'big_grey_circle.png'
big_orange_circle_path = 'orange_big_circle.png'

# lose_sound = SoundLoader.load()
win_sound = SoundLoader.load('360winsound.wav')
music_sound = SoundLoader.load('360sound.wav')

# time.sleep(music_sound.length)
size = Window.size
window_x = (size[0])
window_y = (size[1])

player_fps=70
enemy_fps = 60
sound_on = True
speed_time = 0
direction_time = 0
score= 0
time=0

highscore_file= open('highscore.txt','r')
actual_highscore = highscore_file.readline()
highscore_file.close()
sm= ScreenManager(transition=FadeTransition())
class how_to_play_label(Widget):
    pass
class BackgroundTemplate(Widget):
    pass
class CircleButton(Widget):
    font_size = NumericProperty(20)
    def __init__(self,path,screen,radius,midpoint,font_size,word,**kwargs):
        super(CircleButton,self).__init__(**kwargs)
        self.texture = Image(source=path,mipmap=True).texture
        self.font_size = font_size
        self.radius = radius
        self.screen = screen
        self.midpoint = midpoint
        self.x = self.midpoint[0]
        self.y = self.midpoint[1]
        self.real_pos = (self.x-self.radius,self.y-self.radius)
        self.word = word
        self.label = Label(center_x=self.x,center_y=self.y,font_size = (self.font_size),text=(self.word))

        with self.canvas:
            Ellipse(texture=(self.texture),pos=(self.real_pos),size=(self.radius*2,self.radius*2))
        self.add_widget(self.label)
    def on_touch_down(self,touch):
        if self.real_pos[0] < touch.x < self.x+self.radius and self.real_pos[1] < touch.y < self.y+self.radius:
            sm.current = self.screen

class TinyButton(Widget):
    font_size = NumericProperty(20)
    def __init__(self,path,screen,radius,midpoint,font_size,word,**kwargs):
        super(TinyButton,self).__init__(**kwargs)
        self.texture = Image(source=path,mipmap=True).texture
        self.font_size = font_size
        self.radius = radius
        self.screen = screen
        self.midpoint = midpoint
        self.x = self.midpoint[0]
        self.y = self.midpoint[1]
        self.real_pos = (self.x-self.radius,self.y-self.radius)
        self.word = word
        self.label = Label(x=self.midpoint[0],center_y = self.midpoint[1],font_size =(self.font_size),text=(self.word))
        self.label.bind(size=self.label.setter('text_size'))

        with self.canvas:
            Ellipse(texture=(self.texture),pos=(self.real_pos),size=(self.radius*2,self.radius*2))
        self.add_widget(self.label)
    def on_touch_down(self,touch):
        if self.real_pos[0] < touch.x < self.x+self.radius and self.real_pos[1] < touch.y < self.y+self.radius:
            sm.current = self.screen





class Circle(Widget):
    texture = Image(source=circle_path,mipmap=True).texture
    was_position = ListProperty([])
    font_size = NumericProperty(20)
    def __init__(self,radius,midpoint,font_size,name='',**kwargs):
        super(Circle,self).__init__(**kwargs)
        self.font_size = font_size
        self.radius = radius
        self.midpoint = midpoint
        self.x = self.midpoint[0]
        self.y = self.midpoint[1]
        self.real_pos = (self.x-self.radius,self.y-self.radius)

        self.position_list = []
        self.name = name
        self.is_full = False
        for position in range(0,360):
            self.fi = radians(position)
            x = int(self.x - (self.radius + 30) * cos(self.fi)) - 11
            y = int(self.y + (self.radius + 30) * sin(self.fi)) - 11
            self.position_list.append((x,y))
        with self.canvas:
            Ellipse(texture=(self.texture),pos=(self.real_pos),size=(self.radius*2,self.radius*2))


middle_circle = Circle(70,[window_x//2,window_y//2],name='middle',font_size =25)
down_circle = Circle(50,[window_x//2,window_y//2-180],name='down',font_size =20)
up_circle = Circle(50,[window_x//2,window_y//2+180],name='up',font_size =20)


class Player(Widget):
    texture = Image(source=white_circle_path).texture
    diameter = 22
    radius = diameter//2

    kill = BooleanProperty(True)
    def __init__(self,actual_circle,enemies_circle_list,main_circle=middle_circle,second_circle=up_circle,third_circle=down_circle,**kwargs):
        super(Player,self).__init__(**kwargs)
        self.main_circle = main_circle
        self.second_circle = second_circle
        self.third_circle = third_circle
        self.actual_circle = actual_circle
        self.new_actual_circle = actual_circle
        self.position_list = self.actual_circle.position_list
        self.change_direction = True

        self.position = 180
        self.speed = 2
        self.enemies_circle_list = enemies_circle_list
        self.x = self.pos[0] + self.diameter//2
        self.y = self.pos[1] + self.diameter//2
    def set_position(self):
        if self.change_direction == True:
            if self.position < len(self.position_list)-self.speed:
                self.position += self.speed
            else:
                self.position = 0
        else:
            if self.position > 0:
                self.position -= self.speed
            else:
                self.position = len(self.position_list)-self.speed
        self.pos  = self.position_list[self.position]


    def set_circle(self):
        if self.x > self.actual_circle.x - self.diameter and self.x < self.actual_circle.x + self.diameter :
            if self.actual_circle == self.main_circle:
                if self.y < self.actual_circle.y:
                    self.new_actual_circle = self.third_circle
                elif self.y > self.actual_circle.y:
                    self.new_actual_circle = self.second_circle
            if self.actual_circle == self.third_circle:
                if self.y > self.actual_circle.y:
                    self.new_actual_circle = self.main_circle
            if self.actual_circle == self.second_circle:
                if self.y < self.actual_circle.y:
                    self.new_actual_circle = self.main_circle
        if self.new_actual_circle != self.actual_circle:
            self.actual_circle = self.new_actual_circle
            if self.actual_circle == self.main_circle:
                if self.y < self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))

                if self.y > self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))

            if self.actual_circle == self.second_circle:
                if self.y < self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))

            if self.actual_circle == self.third_circle:
                if self.y > self.actual_circle.y:
                    self.position = int(abs(self.position - len(self.position_list)))

        self.position_list= self.actual_circle.position_list

    def do_kill(self):
        global score, lose_sound
        for i in self.enemies_circle_list:
            distance = sqrt((i.x-self.x)**2+(i.y-self.y)**2)
            if distance <= self.radius + i.radius:
                self.actual_circle =  middle_circle
                self.position_list = middle_circle.position_list
                self.x,self.y = middle_circle.position_list[self.position]
                for i in self.enemies_circle_list:
                    i.speed=0
                    self.position = 0

                self.speed=0
                self.position = 180

                sm.current = 'game_over_screen'
                return True




class Enemy(Widget):
    texture= Image(source=grey_circle_path).texture
    diameter = 22
    radius = diameter//2
    change_direction = BooleanProperty(True)
    position = NumericProperty(0)
    def __init__(self,circle,**kwargs):
        super(Enemy,self).__init__(**kwargs)
        self.actual_circle = circle
        self.new_actual_circle = circle
        self.position_list = self.actual_circle.position_list
        self.local_speed_time = 0
        self.local_direction_time = 0

        self.speed = 1
        self.min_speed = 1
        self.max_speed = 1


        self.x = self.pos[0] + self.diameter//2
        self.y = self.pos[1] + self.diameter//2

    def set_position(self):
        global speed_time
        if self.change_direction == True:
            if self.position < len(self.position_list)-self.speed:
                self.position += self.speed
            else:
                self.position = 0
        else:
            if self.position > 0:
                self.position -= self.speed
            else:
                self.position = len(self.position_list)-self.speed
        self.pos  = self.position_list[self.position]

    def change_speed(self):
        if self.min_speed != self.max_speed:
            self.speed = randrange(self.min_speed,self.max_speed)

    def update(self):
        global speed_time, direction_time
        self.set_position()

        if speed_time > self.local_speed_time and randint(0,1) and self.local_speed_time != 0:
            self.change_speed()
            speed_time = 0
        if direction_time > self.local_direction_time and True and self.local_direction_time != 0:
            self.change_direction = not self.change_direction
            direction_time = 0

class GameScreen(Screen):
    global score, direction_time, middle_circle

    game_score = StringProperty(str(score))
    def __init__(self,**kwargs):
        super(GameScreen,self).__init__(**kwargs)


        self.middle_enemy = Enemy(middle_circle)
        self.up_enemy = Enemy(up_circle)
        self.down_enemy = Enemy(down_circle)
        self.enemies_circle_list = [self.middle_enemy,self.down_enemy,self.up_enemy]
        self.circle_list = [middle_circle,up_circle,down_circle]
        self.player_circle = Player(middle_circle,self.enemies_circle_list,middle_circle,up_circle,down_circle)

    def raise_level(self,dt):
        global score,fps,direction_time
        if score > 6:
            fps = 75
            for i in self.enemies_circle_list:
                i.local_direction_time = 450
        if score > 12:
            fps =82
            for i in self.enemies_circle_list:
                i.local_direction_time = 400
        if score > 24:
            fps =90
            for i in self.enemies_circle_list:
                i.local_direction_time = 380
        if score > 36:
            fps =99
            for i in self.enemies_circle_list:
                i.local_direction_time = 360
        if score > 48:
            fps = 110
            for i in self.enemies_circle_list:
                i.local_direction_time = 340
        if score > 60:
            fps= 120
            for i in self.enemies_circle_list:
                i.local_direction_time = 320
        if score > 72:
            for i in self.enemies_circle_list:
                i.local_direction_time = 300

        if score > 84:
            for i in self.enemies_circle_list:
                i.local_direction_time = 290
        if score > 96:
            for i in self.enemies_circle_list:
                i.local_direction_time = 280

    def is360(self,player,main_circle,all=True,sound=True,second_circle=up_circle,third_circle=down_circle):

        global score, sound_on, win_sound
        if player.position not in player.actual_circle.was_position:
            player.actual_circle.was_position.append(player.position)
            if (len(player.actual_circle.was_position)) == len(player.actual_circle.position_list)/2:
                player.actual_circle.is_full = True
                player.actual_circle.asteriks = True
                score +=1
                if sound_on == True:
                    win_sound.play()
        if all == True:
            if main_circle.is_full and second_circle.is_full and third_circle.is_full:
                score +=3
                for i in self.circle_list:
                    i.was_position = []
                    i.is_full = False
                    # i.asteriks = False
        else:
            if main_circle.is_full:
                main_circle.was_position =[]
                main_circle.is_full = False
                main_circle.asteriks = False

    def update(self,dt):
        global score, direction_time, sm
        self.game_score = str(score)
        self.player_circle.set_position()
        self.is360(self.player_circle,self.player_circle.actual_circle)
        self.raise_level(dt)
        direction_time +=1
        print(score)
        if self.player_circle.do_kill():
            sm.current = 'game_over_screen'
    def enemy_update(self,dt):
        for circle in self.enemies_circle_list:
            circle.update()


    def enemy_change_speed(self,dt):
        if self.min_speed != self.max_speed:
            self.speed = random.randrange(self.min_speed,self.max_speed)

    def on_touch_down(self,touch):
        ais = True
        if self.player_circle.change_direction == False:
            self.player_circle.change_direction = True
        else:
            self.player_circle.change_direction = False
        if ais:
            self.player_circle.set_circle()
    def restart(self):
        global speed_time,direction_time,score,time,enemies_circle_list,fps
        self.player_circle.kill = False
        fps=70
        speed_time=0
        direction_time=0
        score=0
        time=0
        self.player_circle.actual_circle,self.player_circle.new_actual_circle=middle_circle,middle_circle
        self.player_circle.x,self.player_circle.y  = self.player_circle.position_list[self.player_circle.position]
        self.player_circle.speed = 2
        for i in self.enemies_circle_list:
            i.position = 0
            i.speed = 1

        for i in self.circle_list:
            i.was_position=[]
            i.is_full = False
            i.asteriks=False
    def on_pre_enter(self):
        self.restart()
        Clock.schedule_interval(self.update, 1.0 / 60)
        Clock.schedule_interval(self.enemy_update, 1.0 / 60)
    def on_leave(self):
        Clock.unschedule(self.update)
        Clock.unschedule(self.enemy_update)

class GameOverScreen(Screen):
    global score, actual_highscore
    game_score =StringProperty(score)
    highscore = StringProperty(str(actual_highscore))
    def __init__(self,**kwargs):
        super(GameOverScreen,self).__init__(**kwargs)
        self.again_button = CircleButton(big_grey_circle_path,'game_screen',70,[window_x//2,window_y//2],40,'again')
        self.menu_button = CircleButton(big_grey_circle_path,'menu_screen',40,[window_x//2+125,window_y//2-125],20,'menu')
        self.add_widget(self.again_button)
        self.add_widget(self.menu_button)
        print('gameover',score)
    def update(self,dt):
        global score, direction_time, sm
        self.game_score = str(score)
    def on_pre_enter(self):
        Clock.schedule_interval(self.update, 1.0 / 60)
class MenuScreen(Screen):
    menu_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =25)
    menu_player = Player(menu_circle,[])
    game_score = StringProperty(str(score))
    def __init__(self,**kwargs):
        super(MenuScreen,self).__init__(**kwargs)
        self.play_button = TinyButton(big_orange_circle_path,'game_screen',18,[40,window_y//2-150],25,'play')
        self.htp_button = TinyButton(big_grey_circle_path,'htp1_screen',18,[40,window_y//2-200],25,'                how to play')
        self.quit_button = TinyButton(big_grey_circle_path,'menu_screen',18,[40,window_y//2-250],25,'quit')
        self.add_widget(self.menu_circle)
        self.add_widget(self.menu_player)
        self.add_widget(self.play_button)
        self.add_widget(self.htp_button)
        self.add_widget(self.quit_button)
        self.circle_list = [self.menu_circle]

    def is360(self,player,main_circle,all=True,sound=True,second_circle=up_circle,third_circle=down_circle):

        global score


        if player.position not in player.actual_circle.was_position:
            player.actual_circle.was_position.append(player.position)
            if (len(player.actual_circle.was_position)) == len(player.actual_circle.position_list)/2:
                player.actual_circle.is_full = True
                player.actual_circle.asteriks = True
                score +=1
                # if sound_on == True:
                #     win_sound.play()
        if all == True:
            if main_circle.is_full and second_circle.is_full and third_circle.is_full:
                score +=3
                for i in self.circle_list:
                    i.was_position = []
                    i.is_full = False
                    # i.asteriks = False
        else:
            if main_circle.is_full:
                main_circle.was_position =[]
                main_circle.is_full = False
                main_circle.asteriks = False
    def update(self,dt):
        self.menu_player.set_position()
        self.is360(self.menu_player,self.menu_circle,all=False)

    def on_pre_enter(self):
        Clock.schedule_interval(self.update,1.0/60)
    def on_leave(self):
        Clock.unschedule(self.update)


class HtpScreen(Screen):
    htp_middle_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =20)
    htp_player = Player(htp_middle_circle,[])
    game_score = StringProperty(str(score))
    htp_enemy = Enemy(htp_middle_circle)

    def __init__(self,**kwargs):
        super(HtpScreen,self).__init__(**kwargs)

    def is360(self,player,main_circle,all=True,sound=True,second_circle=up_circle,third_circle=down_circle):
        self.circle_list=(main_circle,second_circle,third_circle)
        global score, sound_on, win_sound

        if player.position not in player.actual_circle.was_position:
            player.actual_circle.was_position.append(player.position)
            if (len(player.actual_circle.was_position)) == len(player.actual_circle.position_list)/2:
                player.actual_circle.is_full = True
                player.actual_circle.asteriks = True
                score +=1
                if sound_on == True:
                    win_sound.play()
        if all == True:
            if main_circle.is_full and second_circle.is_full and third_circle.is_full:
                score +=3
                for i in self.circle_list:
                    i.was_position = []
                    i.is_full = False
                    # i.asteriks = False
        else:
            if main_circle.is_full:
                main_circle.was_position =[]
                main_circle.is_full = False
                main_circle.asteriks = False
    def update(self,dt):
        global score, direction_time
        self.game_score = str(score)
        self.htp_player.set_position()
        self.htp_enemy.set_position()
        self.is360(self.htp_player,self.htp_middle_circle,all=False)

class Htp1Screen(HtpScreen):
    game_score = StringProperty(str(score))
    htp_middle_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =20)
    htp_player = Player(htp_middle_circle,[])
    def __init__(self,**kwargs):
        super(Htp1Screen,self).__init__(**kwargs)
        self.add_widget(self.htp_middle_circle)
        self.add_widget(self.htp_player)
        self.next1to2_button = CircleButton(big_grey_circle_path,'htp2_screen',40,[window_x//2+100,window_y//2+250],25,'next')
        self.back1tomenu_button = CircleButton(big_grey_circle_path,'menu_screen',40,[window_x//2-100,window_y//2+250],25,'back')
        self.add_widget(self.next1to2_button)
        self.add_widget(self.back1tomenu_button)
    def on_touch_down(self,touch):
        self.next1to2_button.on_touch_down(touch)
        self.back1tomenu_button.on_touch_down(touch)
        if touch.y < window_y//2+250:
            ais = True
            if self.htp_player.change_direction == False:
                self.htp_player.change_direction = True
            else:
                self.htp_player.change_direction = False
            if ais:
                self.htp_player.set_circle()

    def on_enter(self):
        Clock.schedule_interval(self.update,1.0/60)
    def on_pre_leave(self):
        Clock.unschedule(self.update)
class Htp2Screen(HtpScreen):

    htp_middle_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =20)
    htp_player = Player(htp_middle_circle,[])
    htp_enemy = Enemy(htp_middle_circle)
    def __init__(self,**kwargs):
        super(Htp2Screen,self).__init__(**kwargs)
        self.add_widget(self.htp_middle_circle)
        self.add_widget(self.htp_player)
        self.next2to3_button = CircleButton(big_grey_circle_path,'htp3_screen',40,[window_x//2+100,window_y//2+250],25,'next')
        self.back2to1_button = CircleButton(big_grey_circle_path,'htp1_screen',40,[window_x//2-100,window_y//2+250],25,'back')
        self.add_widget(self.next2to3_button)
        self.add_widget(self.back2to1_button)
        self.add_widget(self.htp_enemy)
    def on_touch_down(self,touch):
        self.next2to3_button.on_touch_down(touch)
        self.back2to1_button.on_touch_down(touch)
        if touch.y < window_y//2+250:
            ais = True
            if self.htp_player.change_direction == False:
                self.htp_player.change_direction = True
            else:
                self.htp_player.change_direction = False
            if ais:
                self.htp_player.set_circle()
    def on_enter(self):
        Clock.schedule_interval(self.update,1.0/60)
    def on_pre_leave(self):
        Clock.unschedule(self.update)
class Htp3Screen(HtpScreen):
    game_score = StringProperty(str(score))
    htp_middle_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =20)
    htp_down_circle = Circle(50,[window_x//2,window_y//2-180],name='down',font_size =20)
    htp_up_circle = Circle(50,[window_x//2,window_y//2+180],name='up',font_size =20)
    htp_player = Player(htp_middle_circle,[],main_circle=htp_middle_circle,second_circle=htp_up_circle,third_circle=htp_down_circle)
    def __init__(self,**kwargs):
        super(Htp3Screen,self).__init__(**kwargs)
        self.next3to4_button = CircleButton(big_grey_circle_path,'htp4_screen',40,[window_x//2+100,window_y//2+250],25,'next')
        self.back3to2_button = CircleButton(big_grey_circle_path,'htp2_screen',40,[window_x//2-100,window_y//2+250],25,'back')
        self.add_widget(self.htp_middle_circle)
        self.add_widget(self.htp_player)
        self.add_widget(self.next3to4_button)
        self.add_widget(self.back3to2_button)
        self.add_widget(self.htp_up_circle)
        self.add_widget(self.htp_down_circle)
    def on_touch_down(self,touch):
        self.next3to4_button.on_touch_down(touch)
        self.back3to2_button.on_touch_down(touch)
        if touch.y < window_y//2+250:
            ais = True
            if self.htp_player.change_direction == False:
                self.htp_player.change_direction = True
            else:
                self.htp_player.change_direction = False
            if ais:
                self.htp_player.set_circle()
    def update(self,dt):
        global score, direction_time
        self.game_score = str(score)
        self.htp_player.set_position()
        self.htp_enemy.set_position()
        self.is360(self.htp_player,self.htp_middle_circle,all=True,second_circle=self.htp_down_circle,third_circle=self.htp_up_circle)
    def on_enter(self):
        Clock.schedule_interval(self.update,1.0/60)
    def on_pre_leave(self):
        Clock.unschedule(self.update)
class Htp4Screen(HtpScreen):
    game_score = StringProperty(str(score))
    htp_middle_circle = Circle(70,[window_x//2,window_y//2],name='menu',font_size =20)
    htp_down_circle = Circle(50,[window_x//2,window_y//2-180],name='down',font_size =20)
    htp_up_circle = Circle(50,[window_x//2,window_y//2+180],name='up',font_size =20)
    htp_player = Player(htp_middle_circle,[],main_circle=htp_middle_circle,second_circle=htp_up_circle,third_circle=htp_down_circle)

    def __init__(self,**kwargs):
        super(Htp4Screen,self).__init__(**kwargs)
        self.next4tomenu_button = CircleButton(big_grey_circle_path,'menu_screen',40,[window_x//2+100,window_y//2+250],25,'next')
        self.back4to3_button = CircleButton(big_grey_circle_path,'htp3_screen',40,[window_x//2-100,window_y//2+250],25,'back')
        self.add_widget(self.htp_middle_circle)
        self.add_widget(self.htp_player)
        self.add_widget(self.next4tomenu_button)
        self.add_widget(self.back4to3_button)
        self.add_widget(self.htp_up_circle)
        self.add_widget(self.htp_down_circle)
    def on_touch_down(self,touch):
        self.next4tomenu_button.on_touch_down(touch)
        self.back4to3_button.on_touch_down(touch)
        if touch.y < window_y//2+250:
            ais = True
            if self.htp_player.change_direction == False:
                self.htp_player.change_direction = True
            else:
                self.htp_player.change_direction = False
            if ais:
                self.htp_player.set_circle()
    def update(self,dt):
        global score, direction_time
        self.game_score = str(score)
        self.htp_player.set_position()
        self.htp_enemy.set_position()
        self.is360(self.htp_player,self.htp_middle_circle,all=True)
    def on_enter(self):
        Clock.schedule_interval(self.update,1.0/60)
    def on_pre_leave(self):
        Clock.unschedule(self.update)
class My360App(App):
    def build(self):
        global sm
        music_sound.loop = True
        music_sound.play()
        game_screen = GameScreen(size=(400,717),name='game_screen')
        menu_screen = MenuScreen(name='menu_screen')
        game_over_screen = GameOverScreen(name='game_over_screen')
        htp1_screen = Htp1Screen(name='htp1_screen')
        htp2_screen = Htp2Screen(name='htp2_screen')
        htp3_screen = Htp3Screen(name='htp3_screen')
        htp4_screen = Htp4Screen(name='htp4_screen')


        game_screen.add_widget(middle_circle)
        game_screen.add_widget(up_circle)
        game_screen.add_widget(down_circle)

        game_screen.add_widget(game_screen.middle_enemy)
        game_screen.add_widget(game_screen.down_enemy)
        game_screen.add_widget(game_screen.up_enemy)
        game_screen.add_widget(game_screen.player_circle)

        sm.add_widget(menu_screen)
        sm.add_widget(game_screen)
        sm.add_widget(game_over_screen)
        sm.add_widget(htp1_screen)
        sm.add_widget(htp2_screen)
        sm.add_widget(htp3_screen)
        sm.add_widget(htp4_screen)


        return sm


if __name__ == '__main__':
    My360App().run()


