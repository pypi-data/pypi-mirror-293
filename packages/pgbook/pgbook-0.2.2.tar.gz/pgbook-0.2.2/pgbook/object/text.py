import pygame,os
import pkg_resources
from .object import Position
from ..eventlist.thinglist import ThingList
from ..eventlist.signal import Signal,Count

class BaseText:
    def __init__(self,text='Some Text',color=(255,255,255),textsize=24,textfile=None):
        self.objects_type='BaseText'
        self.drawlist=ThingList()
        self.eventlist=ThingList()
        
        self.new_data(text,color,textsize,textfile)
        
    def connect_page(self,page):
        self.pos=Position(0,0,page.screen.width,page.screen.height)
        page.drawlist.connect(self.drawlist)
        page.eventlist.connect(self.eventlist)
        self.drawlist.connect(self.draw,'DrawButton')
        
    def draw(self,screen):
        textRect = self.textbook.get_rect()
        textRect.center = (self.pos.true_pos().x,self.pos.true_pos().y)
        screen.blit(self.textbook, textRect)
        
    def new_data(self,text='Some Text',color=(255,255,255),textsize=24,textfile=None):
        self.text=text
        self.textcolor=color
        self.TextSize=textsize
        if textfile==None:
            self.font_path = pkg_resources.resource_filename('pgbook', 'static/fonts/NotoFont.ttf')
        else:
            self.font_path=textfile
        self.font= pygame.font.Font(self.font_path,self.TextSize)
        self.textbook = self.font.render(self.text, True, self.textcolor,None)
        
class EnglishTextInput:
    def __init__(self,text='',empty_text='Input Some Text',
                 back_color=(138,138,138),cback_color=(96,96,96),
                 text_color=(255,255,255),notext_color=(200,200,200)
                 ,centercolor=(168,168,168),textsize=24,
                 textfile=None,width=256,outline=3):
        
        self.new_data(text,empty_text,back_color,cback_color,
                 text_color,notext_color,centercolor,textsize,
                 textfile,width,outline)
        
        self.objects_type='ETextInput'
        self.drawlist=ThingList()
        self.eventlist=ThingList()
        
        self.IsFocus=Signal()
        self.ShowFocus=Count()
        
        
    def connect_page(self,page):
        self.pos=Position(0,0,page.screen.width,page.screen.height)
        page.drawlist.connect(self.drawlist)
        page.eventlist.connect(self.eventlist)
        self.drawlist.connect(self.draw_background,'DrawBackGroung')
        self.drawlist.connect(self.draw_text,'DrawText')
        self.drawlist.connect(self.changeMouseDown,'ChangeMouseDown')
        self.eventlist.connect(self.changeevent,'ChangeTextInput')
        
    def draw_background(self,screen):
        self.rect=pygame.rect.Rect(0,0,0,0)
        self.rect.height=int(self.TextSize*1.333333)+2*self.outline#self.text.textbook.get_rect().height+2*self.outline
        self.rect.width=self.Width+2*self.outline
        self.rect.center=(self.pos.true_pos().x,self.pos.true_pos().y)
        if self.IsFocus.is_true():
            NowColor=self.DefaultBackColor
        else:
            NowColor=self.SelectedBackColor
        crect=self.rect
        crect.height=int(self.TextSize*1.333333)
        crect.width=self.Width
        crect.center=(self.pos.true_pos().x,self.pos.true_pos().y)
        
        self.DrawBack_cen=pygame.draw.rect(screen,self.CenterColor,self.rect,width=0,
                                       border_radius=6)
        self.DrawBack_out=pygame.draw.rect(screen,NowColor,self.rect,width=self.outline,
                                       border_radius=6)
    
    def draw_text(self,screen):
        if self.NowText=='':
            self.textbook = self.font.render(self.DefaultEmptyText, True, self.NoTextColor,None)
            textRect = self.textbook.get_rect()
            textRect.center=self.DrawBack_cen.center+self.outline
            textRect.left=self.DrawBack_cen.left
            screen.blit(self.textbook, textRect)
        else:
            self.textbook = self.font.render(self.DefaultEmptyText, True, self.DefaultTextColor,None)
            textRect = self.textbook.get_rect()
            textRect.center=self.DrawBack_cen.center
            textRect.left=self.DrawBack_cen.left+self.outline
            screen.blit(self.textbook, textRect)
            if self.IsFocus.is_true():
                if self.ShowFocus.get():
                    trybook = self.font.render(self.DefaultEmptyText[0:self.cursor], True, self.DefaultTextColor,None)
                    trytextRect = trybook.get_rect()
                    trytextRect.center=self.DrawBack_cen.center
                    trytextRect.left=self.DrawBack_cen.left+self.outline
                    pygame.draw.line(screen,self.DefaultTextColor,trytextRect.topright,trytextRect.bottomright,2)
            
    
    def changeMouseDown(self,screen):
        mouse_presses = pygame.mouse.get_pressed()
 
        if mouse_presses[0]:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.IsFocus.give(True)
                os.environ["SDL_IME_SHOW_UI"] = "1"
                pygame.key.start_text_input()
            else:
                self.IsFocus.give(False)
                pygame.key.stop_text_input()
                
    def changeevent(self,event):
        if event.type == pygame.TEXTINPUT:
            str_list = list(self.NowText)
            str_list.insert(self.cursor, event.text)  # 在指定位置插入字符串
            self.NowText=''.join(str_list)
            self.cursor+=event.text.__len__()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                str_list = list(self.NowText)
                print(str_list)
                print(self.cursor)
                str_list.pop(self.cursor-1)  # 在指定位置删除字符
                self.NowText=''.join(str_list)
                self.cursor-=1
            elif event.key == pygame.K_EXCLAIM or event.key == pygame.K_TAB:
                self.IsFocus.give(False)
                pygame.key.stop_text_input()
            elif event.key == pygame.K_RIGHT:
                self.cursor+=1
            elif event.key == pygame.K_LEFT:
                self.cursor-=1
    
    def new_data(self,text='',empty_text='Input Some Text',
                 back_color=(138,138,138),cback_color=(96,96,96),
                 text_color=(255,255,255),notext_color=(200,200,200)
                 ,centercolor=(168,168,168),textsize=24,
                 textfile=None,width=256,outline=3):
        
        #默认文字
        self.DefaultText=text
        self.DefaultEmptyText=empty_text
        self.NowText=self.DefaultText
        self.cursor=self.DefaultText.__len__()
        #默认颜色
        self.DefaultBackColor=back_color#失去选中颜色
        self.SelectedBackColor=cback_color#选中颜色
        self.CenterColor=centercolor
        self.DefaultTextColor=text_color#文字颜色
        self.NoTextColor=notext_color#空时字体颜色
        
        self.TextSize = textsize
        self.Width=width
        if textfile==None:
            self.font_path = pkg_resources.resource_filename('pgbook', 'static/fonts/NotoFont.ttf')
        else:
            self.font_path = textfile
        self.font= pygame.font.Font(self.font_path,self.TextSize)
        self.outline=outline
        