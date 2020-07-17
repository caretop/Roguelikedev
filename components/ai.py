# pylint: disable=E1101
import tcod as libtcod
from game_messages import Message
from random import randrange

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        monster_idle_movement = randrange(-1,2) #시야 외 몬스터의 랜덤 이동
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
                        
            elif target.fighter. hp > 0 :
                attack_results = monster.fighter.attack (target)
                results.extend(attack_results)
                #공격로그는 list.extend를 사용한다. 중복 방지 위해
            
            
        '''
        else:
            #if monster_idle_movement < 1: 시야 외 랜덤 이동 
                #monster.
            

            if monster.distance_to(target) <= 8:
                #몬스터가 근처에 있을 때&움직일 때에 출력!
                results.append({'message': Message('근처에서 무언가의 발소리가 들린다..', libtcod.white)})
        '''
        return results
        