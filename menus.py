import tcod as libtcod
import tcod


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)+8
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)



def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(item.name))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(item.name))
            else:
                options.append(item.name)

    menu(con, header, options, 20, screen_width, screen_height)


def main_menu(con, screen_width, screen_height):
    libtcod.console_load_xp(con, 'test4.xp')
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) + 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'TOMBS OF THE ANCIENT KINGS')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By (Your name here)')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 , from {0})'.format(player.fighter.dt)]

    menu(con, header, options, menu_width, screen_width, screen_height)



def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(20, 40)

    libtcod.console_load_xp(window, 'charmockup.xp')
    libtcod.console_get_default_foreground(libtcod.black)

    libtcod.console_print_rect_ex(window, 1, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '캐릭터')
    libtcod.console_print_rect_ex(window, 1, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '레벨: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 1, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '경험치: {0}\n'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 1, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '레벨업까지 남은 경험치: {0}\n'.format(player.level.experience_to_next_level))
    #방어 수치 
    libtcod.console_print_rect_ex(window, 1, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'HP:{1}/{0}'.format(player.fighter.max_hp, player.fighter.hp))
                                  
    libtcod.console_print_rect_ex(window, 1, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'SP:{0}'.format(player.fighter.sp))
                                  
    libtcod.console_print_rect_ex(window, 1, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '피해 감쇄(DT):{0}'.format(player.fighter.dt))
    libtcod.console_print_rect_ex(window, 1, 9, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '회피(AC):{0}'.format(player.fighter.ac))
    libtcod.console_print_rect_ex(window, 1, 10, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '인내 방어(Fort):{0}'.format(player.fighter.fort))
    libtcod.console_print_rect_ex(window, 1, 11, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '반사 신경(Refl):{0}'.format(player.fighter.refl))
    libtcod.console_print_rect_ex(window, 1, 12, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '의지 방어(Will):{0}'.format(player.fighter.will))
    #능력치 피해 명중 
    libtcod.console_print_rect_ex(window, 1, 14, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '근력(STR):{0}'.format(player.fighter.STR))
    libtcod.console_print_rect_ex(window, 1, 15, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '민첩(DEX):{0}'.format(player.fighter.DEX))
    libtcod.console_print_rect_ex(window, 1, 16, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '건강(CON):{0}'.format(player.fighter.CON))
    libtcod.console_print_rect_ex(window, 1, 17, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '지능(INT):{0}'.format(player.fighter.INT))
    libtcod.console_print_rect_ex(window, 1, 18, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '무기 피해:{0}'.format(player.fighter.power.replace('t','')))
    libtcod.console_print_rect_ex(window, 1, 19, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '무기 명중:{0}'.format(player.fighter.acc.replace('t','')))
    libtcod.console_print_rect_ex(window, 1, 20, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '치명타 확률:{0}'.format(player.fighter.luck))
    libtcod.console_print_rect_ex(window, 1, 21, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '어둠 주문력:{0}'.format(player.fighter.lpower.replace('+','',1)))
    libtcod.console_print_rect_ex(window, 1, 22, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '빛 주문력:{0}'.format(player.fighter.dpower.replace('+','',1)))


    #기술
    libtcod.console_print_rect_ex(window, 4, 25, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '근접:{0}'.format(player.fighter.melee))
    libtcod.console_print_rect_ex(window, 12, 25, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '화기:{0}'.format(player.fighter.gun))
    libtcod.console_print_rect_ex(window, 4, 26, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '기술:{0}'.format(player.fighter.tec))
    libtcod.console_print_rect_ex(window, 12, 26, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '지식:{0}'.format(player.fighter.lore))
    libtcod.console_print_rect_ex(window, 4, 27, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '빛:{0}'.format(player.fighter.light))
    libtcod.console_print_rect_ex(window, 12, 27, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, '어둠:{0}'.format(player.fighter.light))

    x = screen_width // 2 - character_screen_width // 2 
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, -50, 0, character_screen_width+60, 50, 0, x-70, y-17, 1.0, 1.0)



def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)