from abc import ABC, abstractmethod

class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []
        self.stats = {
            "HP": 128,  # health points
            "MP": 42,  # magic points, 
            "SP": 100,  # skill points
            "Strength": 15,  # сила
            "Endurance": 8,  # выносливость
            "Perception": 4,  # восприятие
            "Charisma": 2,  # харизма
            "Intelligence": 3,  # интеллект
            "Agility": 8,  # ловкость 
            "Luck": 1  # удача
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(ABC, Hero):

    def __init__(self, base):
        self.base = base
        self.bad_effects = self.good_effects = {}

    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects

    def get_stats(self):
        _temp_stats = self.base.get_stats()
        for key, val in self.bad_effects.items():
            _temp_stats[key] -= val
        for key, val in self.good_effects.items():
            _temp_stats[key] += val
        return _temp_stats


class AbstractPositive(AbstractEffect):

    def get_negative_effects(self):
        return self.base.get_negative_effects().copy()


class AbstractNegative(AbstractEffect):

    def get_positive_effects(self):
        return self.base.get_positive_effects().copy()


class Berserk(AbstractPositive):
    def __init__(self, base):
        self.base = base
        self.good_effects = {
            "Strength": 7,
            "Endurance": 7,
            "Agility": 7,
            "Luck": 7,
            "HP": 50
        }
        self.bad_effects = {
            "Perception": 3,
            "Charisma": 3,
            "Intelligence": 3,
        }

    def get_positive_effects(self):
        _temp_lst = self.base.get_positive_effects()
        _temp_lst.append("Berserk")
        return _temp_lst.copy()


class Blessing(AbstractPositive):
    def __init__(self, base):
        self.base = base
        self.good_effects = {
            "Strength": 2,
            "Endurance": 2,
            "Perception": 2,
            "Charisma": 2,
            "Intelligence": 2,
            "Agility": 2,
            "Luck": 2
        }
        self.bad_effects = {}

    def get_positive_effects(self):
        _temp_lst = self.base.get_positive_effects()
        _temp_lst.append("Blessing")
        return _temp_lst.copy()


class Weakness(AbstractNegative):
    def __init__(self, base):
        self.base = base
        self.good_effects = {}
        self.bad_effects = {
            "Strength": 4,
            "Endurance": 4,
            "Agility": 4,
        }

    def get_negative_effects(self):
        _temp_lst = self.base.get_negative_effects()
        _temp_lst.append("Weakness")
        return _temp_lst.copy()


class EvilEye(AbstractNegative):
    def __init__(self, base):
        self.base = base
        self.good_effects = {}
        self.bad_effects = {
            "Luck": 10
        }

    def get_negative_effects(self):
        _temp_lst = self.base.get_negative_effects()
        _temp_lst.append("EvilEye")
        return _temp_lst.copy()


class Curse(AbstractNegative):
    def __init__(self, base):
        self.base = base
        self.good_effects = {}
        self.bad_effects = {
            "Strength": 2,
            "Endurance": 2,
            "Perception": 2,
            "Charisma": 2,
            "Intelligence": 2,
            "Agility": 2,
            "Luck": 2
        }

    def get_negative_effects(self):
        _temp_lst = self.base.get_negative_effects()
        _temp_lst.append("Curse")
        return _temp_lst.copy()

