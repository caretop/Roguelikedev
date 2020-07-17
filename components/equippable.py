class Equippable:
    def __init__(self, slot, base_dice = '',power_bonus=0, acc_bonus=0, dt_bonus=0, ac_bonus=0,
    fort_bonus=0, refl_bonus=0, will_bonus=0, max_hp_bonus=0, STR_weapon=False, DEX_weapon=False,
    dpower_bonus=0, lpower_bonus=0, luck_bonus=0, ranged_weapon = False):
        self.slot = slot
        self.base_dice = base_dice
        self.power_bonus = power_bonus
        self.acc_bonus = acc_bonus
        self.dt_bonus = dt_bonus
        self.ac_bonus = ac_bonus
        self.fort_bonus = fort_bonus
        self.refl_bonus = refl_bonus
        self.will_bonus = will_bonus
        self.max_hp_bonus = max_hp_bonus
        self.STR_weapon= STR_weapon
        self.DEX_weapon= DEX_weapon
        self.dpower_bonus= dpower_bonus
        self.lpower_bonus= lpower_bonus
        self.luck_bonus = luck_bonus
        self.ranged_weapon = ranged_weapon 
        
        