from components.equipment_slot import EquipmentSlots


class Equipment:
    def __init__(self, main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    '''
    아이템 보너스 총점 
    they sum up the “bonuses” from both the main hand and off hand equipment, 
    and return the value. Since we’re using properties, 
    these values can be accessed like a regular variable
    '''
    
    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        return bonus
    
    @property
    def base_dice(self):
        dice = '1d4t'

        if self.main_hand and self.main_hand.equippable:
            dice= self.main_hand.equippable.base_dice 

        if self.off_hand and self.off_hand.equippable:
            dice= self.off_hand.equippable.base_dice 

        return dice
    

    @property
    def power_bonus(self):
        bonus = '0'

        if self.main_hand and self.main_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.main_hand.equippable.power_bonus)

        if self.off_hand and self.off_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.off_hand.equippable.power_bonus)

        return bonus

    @property
    def acc_bonus(self):
        bonus = '0'

        if self.main_hand and self.main_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.main_hand.equippable.acc_bonus)

        if self.off_hand and self.off_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.off_hand.equippable.acc_bonus)

        return bonus

    @property
    def dt_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.dt_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.dt_bonus

        return bonus

    @property
    def ac_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.ac_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.ac_bonus

        return bonus
    
    @property
    def fort_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.fort_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.fort_bonus

        return bonus
    
    @property
    def refl_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.refl_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.refl_bonus

        return bonus
    
    @property
    def will_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.will_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.will_bonus

        return bonus

    @property
    def dpower_bonus(self):
        bonus = '0'

        if self.main_hand and self.main_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.main_hand.equippable.dpower_bonus)

        if self.off_hand and self.off_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.off_hand.equippable.dpower_bonus)

        return bonus

    @property
    def lpower_bonus(self):
        bonus = '0'

        if self.main_hand and self.main_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.main_hand.equippable.lpower_bonus)

        if self.off_hand and self.off_hand.equippable:
            bonus= bonus.replace('0','',1)
            bonus += str(self.off_hand.equippable.lpower_bonus)

        return bonus


    @property
    def luck_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.luck_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.luck_bonus

        return bonus



    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results