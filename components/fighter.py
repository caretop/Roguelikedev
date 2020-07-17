# pylint: disable=E1101
import tcod as libtcod
import dice
import math


from game_messages import Message

#stats
class Fighter :
    def __init__(self, hp, sp, dt, ac, dice, power, 
    acc, STR, DEX, CON, INT, fort, refl, will,
    melee, gun, light, dark, tec, lore, lpower, dpower, luck, xp):
        self.base_max_hp = hp
        self.hp = hp + 5*CON
        self.sp = sp  
        self.base_dt = dt
        self.base_ac = ac
        self.base_dice = dice #무기에 따라 바뀌는 피해 다이스 
        self.base_power = power
        self.base_acc = acc
        self.STR = STR # str -> 힘 기반 무기 명중에 보너스, 힘 기반 무기 피해에 보너스 
        self.DEX = DEX # dex - > 덱스 기반 무기 명중에 보너스, 덱 기반 무기 피해에 보너스, ac에 보너스 
        self.CON = CON # con - > 한 점당 체력에 5 보너스, 내성에 보너스 
        self.INT = INT # int - > 의지 내성에 보너스, 주문력에 보너스 
        self.base_fort = fort
        self.base_refl = refl
        self.base_will = will
        self.xp = xp
        self.melee = melee
        self.gun = gun
        self.light = light
        self.dark = dark 
        self.tec = tec
        self.lore = lore 
        self.base_lpower = lpower
        self.base_dpower = dpower
        self.base_luck = luck 

        
    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus + self.CON*5
    
    @property
    def dice(self):
        if self.owner and self.owner.equipment:
            dice = self.owner.equipment.base_dice
        else:
            dice = self.base_dice
        
        return dice


    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = '+' + str(self.owner.equipment.power_bonus)
        else:
            bonus = ''
        
        if self.owner.equipment == None or self.owner.equipment.main_hand == None:
            return self.dice + bonus + '+' + str(self.STR)
        elif self.owner.equipment.main_hand.equippable.STR_weapon == True:
            return self.dice + bonus + '+' + str(self.STR)
        elif self.owner.equipment.main_hand.equippable.DEX_weapon == True:
            return self.dice + bonus + '+' + str(self.DEX)
        

        return self.dice + bonus + '+' + str(self.STR)
    
    @property
    def acc(self):
        if self.owner and self.owner.equipment:
            bonus = '+' + str(self.owner.equipment.acc_bonus)
        else:
            bonus = ''
        
        if self.owner.equipment == None or self.owner.equipment.main_hand == None:
            return self.base_acc + bonus + '+' + str(self.STR) + '+' + str(2 * self.melee)
        elif self.owner.equipment.main_hand.equippable.STR_weapon == True:
            return self.base_acc + bonus + '+' + str(self.STR) + '+' + str(2 * self.melee)
        elif self.owner.equipment.main_hand.equippable.DEX_weapon == True:
            return self.base_acc + bonus + '+' + str(self.DEX) + '+' + str(2 * self.melee)
        


    @property
    def dt(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dt_bonus
        else:
            bonus = 0

        return self.base_dt + bonus
    
    @property
    def ac(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.ac_bonus
        else:
            bonus = 0

        return self.base_ac + bonus + self.DEX


    #내성
    @property
    def fort(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.fort_bonus
        else:
            bonus = 0

        return self.base_fort + bonus +math.ceil((self.STR+self.CON) / 2)
    
    @property
    def refl(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.refl_bonus
        else:
            bonus = 0

        return self.base_refl + bonus + math.ceil((self.DEX+self.CON) / 2)

    @property
    def will(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.will_bonus
        else:
            bonus = 0

        return self.base_will + bonus + math.ceil((self.INT+self.CON) / 2)
    

    @property
    def lpower(self):
        if self.owner and self.owner.equipment:
            bonus = str(self.owner.equipment.lpower_bonus)
        else:
            bonus = ''

        return self.base_lpower + '+' + bonus + '+' + str(self.INT) + '+' + str(self.light) 
    
    @property
    def dpower(self):
        if self.owner and self.owner.equipment:
            bonus = str(self.owner.equipment.dpower_bonus)
        else:
            bonus = ''

        return self.base_dpower + '+' + bonus + '+' + str(self.INT) + '+' + str(self.dark) 
  
    
    @property
    def luck(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.luck_bonus
        else:
            return self.base_luck

        return self.base_luck + bonus 

        



    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <=0:
            results.append({'dead': self.owner, 'xp': self.xp})
        
        return results


    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        crit = False
        results = []
        # if acc roll > target's ac - > hit!
        crit_die = dice.roll('d100t')
        if crit_die in range(1,self.luck+1):
            crit = True 
        print(target.name)

        if dice.roll(self.acc) > target.fighter.ac or crit == True:
            
            if crit: #크리 범위를 캐릭터마다 다르게 해서 리스트로 가져오자.
                damage = dice.roll(self.power) * 2 - target.fighter.dt

            else:
                damage = dice.roll(self.power) - target.fighter.dt

            if damage > 0:

                if crit == True:
                    results.append({'message': Message('{0}(은)는 {1}에게 치명타로 {2}의 피해를 입혔다!'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.yellow)})
                    results.extend(target.fighter.take_damage(damage))

                else:
                    results.append({'message': Message('{0}는 {1}에게 {2}의 피해를 입혔다.'.format(
                    self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
                    results.extend(target.fighter.take_damage(damage))

            

            else:
                results.append({'message': Message('{0}(은)는 {1}에게 아무런 피해도 입히지 못했다.'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white)})
        
        else:
            results.append({'message': Message('{1}(은)는 {0}의 공격을 회피했다!'.format(
                    self.owner.name.capitalize(), target.name), libtcod.white)})

        del crit_die
        return results