import libtcodpy as libtcod
import tcod
import math

from random import randint
from map_objects.game_map import GameMap
from fov_functions import initialize_fov, recompute_fov
from time import sleep
from loader_functions.initialize_new_game import get_constants
from render_functions import render_all
from input_handlers import handle_keys, handle_mouse
from entity import get_blocking_entities_at_location


def get_targeting_radius(con, panel, x, y, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
bar_width, panel_height, panel_y, mouse, colors, game_state,camera,left_click,right_click,animation_console):

    #여기서부터 커서 
    libtcod.console_set_char_background(animation_console, x, y,libtcod.dark_yellow)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    

    #마우스 위치 변경 감지시 클리어 
    
    if mouse.dcx !=0 or mouse.dcy !=0 or mouse.dcx !=0 and mouse.dcy !=0:
        libtcod.console_clear(animation_console)
        
    
    #왼클릭 올 오른클릭 감지시 좌표 리턴 
    if handle_mouse(mouse).get('left_click'):
        left_click = (x, y)
        return left_click
    elif handle_mouse(mouse).get('right_click'):
        right_click = (x, y)
        return right_click
    #다음 좌표 변경까지 0.1초 대기(깜빡임 방지)
    sleep(0.1)
    libtcod.console_clear(animation_console)
    
def get_player_tooltip(animation_console, x, y, mouse, screen_width, screen_height):
    libtcod.console_set_default_background(animation_console,(0,0,0))

    if (x,y) in [(6,10), (7,10), (8,10), (9,10), (10,10), (11,10), (12,10),(13,10),(14,10),(15,10),(16,10)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 30, 13 , 5, False, 'SP는 인간성을 유지할 수 있게 하는        ')
        libtcod.console_print_frame(animation_console, x+1, y+2, 30, 13 , 13, False, '정신적인 힘입니다. 0이 되면 죽습니다.       ')
        libtcod.console_print_frame(animation_console, x+1, y+3, 30, 13 , 13, False, '얻음:오락,음식,종교물,귀중품,선행,시체에서 흡수  ')
        libtcod.console_print_frame(animation_console, x+1, y+4, 30, 13 , 13, False, '잃음:마법/전투기술 시전, 탐험하며 천천히      ')




    if (x,y) in [(6,11), (7,11), (8,11), (9,11), (10,11), (11,11), (12,11),(13,11),(14,11),(15,11),(16,11)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 20, 13 , 5, False, 'DT는 캐릭터에게 가해지는 피해량을')
        libtcod.console_print_frame(animation_console, x+1, y+2, 20, 13 , 13, False, '고정된 수치만큼 감소시킵니다.   ')
    elif (x,y) in [(6,12), (7,12), (8,12), (9,12), (10,12), (11,12), (12,12),(13,12),(14,12),(15,12),(16,12)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 20, 13 , 5, False, 'AC는 얼마나 적의 공격을 얼마나')
        libtcod.console_print_frame(animation_console, x+1, y+2, 20, 13 , 13, False, '잘 피할 수 있는지를 말합니다.  ')
        libtcod.console_print_frame(animation_console, x+1, y+3, 20, 13 , 13, False, '기본 수치는 10+민첩입니다.   ')

    elif (x,y) in [(6,13), (7,13), (8,13), (9,13), (10,13), (11,13), (12,13),(13,13),(14,13),(15,13),(16,13)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 20, 13 , 5, False, '인내 방어는 독,몸싸움,감염 등의')
        libtcod.console_print_frame(animation_console, x+1, y+2, 20, 13 , 13, False, '난관들을 신체적인 강인함으로   ')
        libtcod.console_print_frame(animation_console, x+1, y+3, 20, 13 , 13, False, '극복할 수 있는 정도를 말합니다.   ')
        libtcod.console_print_frame(animation_console, x+1, y+4, 20, 13 , 13, False, '기본 수치는 (힘+건강)/2입니다.')

    elif (x,y) in [(6,14), (7,14), (8,14), (9,14), (10,14), (11,14), (12,14),(13,14),(14,14),(15,14),(16,14)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 21, 13 , 5, False, '반사 신경은 폭발 등의 공격    ')
        libtcod.console_print_frame(animation_console, x+1, y+2, 21, 13 , 13, False, '들을 빠른 발걸음과 반응속도로   ')
        libtcod.console_print_frame(animation_console, x+1, y+3, 21, 13 , 13, False, '회피할 수 있는 정도를 말합니다.    ')
        libtcod.console_print_frame(animation_console, x+1, y+4, 21, 13 , 13, False, '기본 수치는 (민첩+건강)/2입니다.')
    
    elif (x,y) in [(6,15), (7,15), (8,15), (9,15), (10,15), (11,15), (12,15),(13,15),(14,15),(15,15),(16,15)]:
        libtcod.console_print_frame(animation_console, x+1, y+1, 21, 13 , 5, False, '의지 방어는 캐릭터에게 부정적인   ')
        libtcod.console_print_frame(animation_console, x+1, y+2, 21, 13 , 13, False, '영향을 끼치는 마법들을 저항할   ')
        libtcod.console_print_frame(animation_console, x+1, y+3, 21, 13 , 13, False, '수 있는 정도를 말합니다.     ')
        libtcod.console_print_frame(animation_console, x+1, y+4, 21, 13 , 13, False, '기본 수치는 (지능+건강)/2입니다.')
    

          
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()


    if mouse.dcx !=0 or mouse.dcy !=0 or mouse.dcx !=0 and mouse.dcy !=0:
        libtcod.console_clear(animation_console)

    if handle_mouse(mouse).get('left_click'):
        left_click = (x, y)
        return left_click

    sleep(0.3)
    libtcod.console_clear(animation_console)





def get_line(path_map, x1,y1, x2,y2):
    astar = tcod.path.AStar(path_map)
    result = astar.get_path(y1,x1, y2,x2)
    return result


def blood_splatter(con,game_map,x,y,colors):

    for i in range(0,5):
        blood_x = x+randint(-2,2)
        blood_y = y+randint(-2,2)

        if game_map.tiles[blood_x][blood_y].block_sight:
            libtcod.console_put_char_ex(con, blood_x, blood_y,'▒',libtcod.red, colors.get('dark_wall'))
            game_map.tiles[blood_x][blood_y].bloodied = True

        else:
            libtcod.console_put_char_ex(con, blood_x, blood_y,'.',libtcod.red, colors.get('light_ground'))
            game_map.tiles[blood_x][blood_y].bloodied = True

def explosion(con, panel, x, y, entities, player, game_map, fov_map, fov_recompute, 
message_log, screen_width, screen_height,mouse, colors, camera,animation_console):

    '''
    for i in range(4):
        sleep(0.03)
        libtcod.console_put_char_ex(animation_console,player.x+i+camera.x,player.y+camera.y,'#',libtcod.red,libtcod.red)
        libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_put_char_ex(animation_console,player.x+i+camera.x+1,player.y+camera.y,'o',libtcod.red,libtcod.yellow)
        libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
                        
        libtcod.console_flush()
    '''
    '''
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x,y+camera.y,'.',libtcod.red,libtcod.orange)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x-1,y+camera.y-1,'.',libtcod.red,libtcod.yellow)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x+1,y+camera.y+1,'.',libtcod.red,libtcod.orange)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x-1,y+camera.y+1,'.',libtcod.red,libtcod.yellow)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x+1,y+camera.y-1,'.',libtcod.red,libtcod.orange)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x-1,y+camera.y,'.',libtcod.red,libtcod.yellow)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x+1,y+camera.y,'.',libtcod.red,libtcod.orange)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x,y+camera.y+1,'.',libtcod.red,libtcod.yellow)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()
    sleep(0.02)
    libtcod.console_put_char_ex(animation_console,x+camera.x,y+camera.y-1,'.',libtcod.red,libtcod.orange)
    libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
    libtcod.console_flush()


    libtcod.console_clear(animation_console)         
    '''
    pass



    '''
    projectile mockup
    
    for i in range(10):
        sleep(0.03)
        libtcod.console_put_char_ex(animation_console,x+i+camera.x,y+camera.y,'#',libtcod.red,libtcod.red)
        libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_put_char_ex(animation_console,x+i+camera.x+1,y+camera.y,'o',libtcod.red,libtcod.yellow)
        libtcod.console_blit(animation_console, 0, 0, screen_width, screen_height, 0, 0, 0)
                        
        libtcod.console_flush()
    '''
    
    







    