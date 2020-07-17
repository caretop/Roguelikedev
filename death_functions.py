import libtcodpy as libtcod

from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('죽었다!', libtcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    #monster - >entity
    death_message = Message('{0} 가 죽었다!'.format(monster.name.capitalize()), libtcod.orange)

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = monster.name +'의 시체 ' 
    monster.render_order = RenderOrder.CORPSE

    monster.x

    return death_message

def get_victim_cord(monster):
    return monster.x, monster.y