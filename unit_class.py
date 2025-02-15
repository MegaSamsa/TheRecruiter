import init
from init import unit_settings, specifications_list
from methods import sex_to_str

specification_level = unit_settings['specification_level']
age_range = unit_settings['age_range']

class Unit:
    def __init__(self, name: str, age: int, sex: bool, specifications: dict):
        self.__name = name
        self.__age = age
        self.__sex = sex
        self.__specifications = specifications
        self.specifications_sex()
        self.__specifications_sum = sum(self.__specifications.values())
    
    # модификатор характеристик, зависящий от пола
    def specifications_sex(self):
        match self.__sex:
            case True:
                self.specification_update(specification='dexterity', action='-', value=1)
            case False:
                self.specification_update(specification='power', action='-', value=1)

    def specification_update(self, specification: str, action: str, value: int):
        match action:
            case '-':
                self.__specifications[specification] -= value
            case '+':
                self.__specifications[specification] += value
        self.__specifications[specification] = max(specification_level['min'], min(self.__specifications[specification], specification_level['max']))

    def get_name(self):
        return self.__name
    
    def get_age(self):
        return self.__age
    
    def get_sex(self):
        return self.__sex
    
    def get_specifications(self):
        return self.__specifications

    def get_specifications_sum(self):
        return self.__specifications_sum

    def greeting(self):
        specifications_str = ", ".join(f"{key}: {value}" for key, value in self.__specifications.items())
        return f"Hello, sir! My name is {self.__name} and I'm {self.__age} years old {sex_to_str(self.__sex)}.\nMy specifications is: {specifications_str} ({self.__specifications_sum})"

class UnitGenerator:
    def __init__(self):
        self.__sex = self.gen_sex()
        self.__name = self.gen_name()
        self.__age = self.gen_age()
        self.__specifications = self.gen_specifications()
    
    def gen_name(self):
        return init.names.get_first_name(sex_to_str(self.__sex))

    def gen_sex(self):
        return init.rnd.choice([True, False])

    def gen_age(self):
        return init.rnd.randint(age_range['min'], age_range['max'])
    
    def gen_specifications(self):
        specifications = {}
        for key in specifications_list:
            specifications[key] = init.rnd.randint(specification_level['min'], specification_level['max'])
        return specifications

    def new_unit(self):
        return Unit(name=self.__name, age=self.__age, sex=self.__sex, specifications=self.__specifications)
