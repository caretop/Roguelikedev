import libtcodpy as libtcod
#타게팅 안 되는거 해결하기 
from time import sleep
from random import randint
from game_messages import Message
from death_functions import kill_monster, kill_player, get_victim_cord
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from camera import Camera
from game_states import GameStates
from entity import Entity
from components.fighter import Fighter
from input_handlers import handle_keys, handle_mouse, get_mouse_movement, handle_main_menu
from loader_functions.initialize_new_game import get_constants,get_game_variables
from render_functions import clear_all, render_all
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box, level_up_menu, character_screen
from map_objects.animations import blood_splatter, explosion, get_targeting_radius, get_player_tooltip


def main():
    constants = get_constants()
    
    libtcod.tileset.set_default(libtcod.tileset.load_truetype_font('ngeb.ttf',0,16))
    #libtcod.console_set_custom_font('arial12x12.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])
    
    animation_console= libtcod.console_new(constants['screen_width'], constants['screen_height'])
    libtcod.console_set_key_color(animation_console, (0,0,0))
    
    
    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False


    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN
                
                         
                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, animation_console, constants)
            
            show_main_menu = True
    
def testfunc():
    print('dd')



def play_game(player, entities, game_map, message_log, game_state, con, panel, animation_console, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    camera = Camera(
    x=0,
    y=0,
    width=constants['screen_width'],
    height=constants['screen_height'],
    map_width=constants['map_width'],
    map_height=constants['map_height'],
    )
    camera.update(player)

    targeting_item = None
    weapon_target = None 

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
    
        x_in_camera, y_in_camera = camera.apply(player.x, player.y)


        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        render_all(con, panel,entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'],
                    game_state,camera)
        
        

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities,camera)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        targeter = action.get('targeter')
        fire = action.get('fire')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                
                    
                else:
                    player.move(dx, dy)
                    camera.update(player)

                    fov_recompute = True

                    for entity in entities:
                        if entity != player and entity.x == player.x and entity.y == player.y:
                        
                             see_results = [{'message': Message('{0}(이)가 보인다.'.format(entity.name), libtcod.white)}]
                             player_turn_results.extend(see_results)

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN


        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('여기에는 주울 수 있는 것이 없다.', libtcod.yellow))
        
        if targeter:
            previous_game_state = GameStates.PLAYERS_TURN
            testfunc()
            game_state = GameStates.WEAPON_TARGETING


        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))


        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    camera.update(player)
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('여기에는 계단이 없다.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_ += 1

            game_state = previous_game_state


        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN
        
        if game_state == GameStates.CHARACTER_SCREEN:
            x, y = get_mouse_movement(mouse)
            get_player_tooltip(animation_console, x, y, mouse, constants['screen_width'], constants['screen_height'])
            if left_click:

                game_state = previous_game_state 


        
        if game_state == GameStates.WEAPON_TARGETING: 
            wx, wy = get_mouse_movement(mouse)
            get_targeting_radius(con, panel, wx, wy, entities, player, game_map, fov_map, fov_recompute, message_log,
            constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],
            mouse, constants['colors'], game_state,camera,left_click,right_click,animation_console)
            if left_click:
                weapon_target_x, weapon_target_y = left_click
                weapon_target_x -= camera.x
                weapon_target_y -= camera.y
                if not libtcod.map_is_in_fov(fov_map, weapon_target_x, weapon_target_y):
                    message_log.add_message(Message('시야 밖의 적을 목표로 지정할 수는 없다.'))
                for entity in entities:
                    if entity.distance(weapon_target_x, weapon_target_y) == 0 and entity.name=='Player':
                        message_log.add_message(Message('자기 자신을 목표로 지정할 수는 없다.'))

                    elif entity.distance(weapon_target_x, weapon_target_y) == 0 and entity.fighter:
                        player_turn_results.append({'wep_targetted': True})
                        weapon_target = entity
                        
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
                
        
        if fire:
            #수동으로 타겟을 잡았거나, 자동 발사로 타겟이 잡혔을 때
            
            #원거리 무기 미장비시 
            if not player.equipment.main_hand:
                message_log.add_message(Message('발사할 수 있는 것을 장비하고 있지 않다.'))

            #원거리 무기 장비시 
            elif player.equipment.main_hand.equippable.ranged_weapon == True:
                #타겟이 지정되었을 때
                if weapon_target is not None :
                    print(weapon_target)
                    message_log.add_message(Message('당신은 {0}을(를) 발사한다! '.format(player.equipment.main_hand.name)))
                    attack_results = player.fighter.attack(weapon_target)
                    player_turn_results.extend(attack_results)
                    if weapon_target.fighter.hp <= 0 :
                        weapon_target = None 
                    game_state = GameStates.ENEMY_TURN
            #타겟이 지정되지 않았을 때 자동 발사  
                else:
                    closest_distance = 10+1
                    for entity in entities:
                        if entity.fighter and libtcod.map_is_in_fov(fov_map, entity.x, entity.y) and entity.name != 'Player' and entity.blocks == True :
                            distance = player.distance_to(entity)

                            if distance < closest_distance:
                                weapon_target = entity
                                closest_distance = distance
                    #자동 발사 대상 지정 후 발사, 타겟 지정 
                    if weapon_target:
                        message_log.add_message(Message('당신은 {0}을(를) 발사한다! '.format(player.equipment.main_hand.name)))
                        attack_results = player.fighter.attack(weapon_target)
                        player_turn_results.extend(attack_results)
                        if weapon_target.fighter.hp <= 0 :
                            weapon_target = None 
                        game_state = GameStates.ENEMY_TURN
                    #타겟이 지정되지 않았고 적이 Fov 외에 있을 때
                    else:
                        message_log.add_message(Message('사격할 수 있는 대상이 보이지 않는다.'))
                        weapon_target = None
                
                    game_state = GameStates.ENEMY_TURN


            else:
                message_log.add_message(Message('발사할 수 있는 것을 장비하고 있지 않다.'))

                   


        if game_state == GameStates.TARGETING:
            x, y = get_mouse_movement(mouse)
            get_targeting_radius(con, panel, x, y, entities, player, game_map, fov_map, fov_recompute, message_log,
            constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],
            mouse, constants['colors'], game_state,camera,left_click,right_click,animation_console)


            if left_click:
                target_x, target_y = left_click
                target_x -= camera.x
                target_y -= camera.y
                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})


        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.LEVEL_UP:
                level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, constants['screen_width'], 
                constants['screen_height'])
            elif game_state == GameStates.CHARACTER_SCREEN:
                character_screen(player, 30, 10, constants['screen_width'], constants['screen_height'])
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state)

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            wep_targetted = player_turn_result.get('wep_targetted')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)
                

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)

                else:
                    victim_cord_x, victim_cord_y = get_victim_cord(dead_entity)

                    explosion(con, panel,victim_cord_x, victim_cord_y, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], mouse, constants['colors'],camera,animation_console)

                    blood_splatter(con,game_map, victim_cord_x, victim_cord_y, constants['colors'])
                    libtcod.console_clear(con)

                    fov_recompute = True
                    message = kill_monster(dead_entity)
                    
                    pass

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN
            
            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('{0}(을)를 장비했다.'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('{0}(을)를 해제했다.'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if wep_targetted:
                game_state = previous_game_state
                message_log.add_message(Message('당신은 목표를 조준한다.'))



            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('목표 지정을 취소하였다.'))


            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(Message('당신은 {0}의 경험치를 얻었다..'.format(xp)))

                if leveled_up:
                    message_log.add_message(Message(
                        '레벨 {0}에 도달하였다!'.format(
                            player.level.current_level) + '!', libtcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP         

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN






if __name__ == '__main__':
    main()