from models import *

class AllergyRepository():
    @staticmethod
    @db_session
    def create(name):
        return Allergy(name=name)


class CategoryRepository():
    @staticmethod
    @db_session
    def create(name):
        return Category(name=name)

class IngredientRepository():
    @staticmethod
    @db_session
    def create(name):
        return Ingredient(name=name)

class RecipeRepository():
    @staticmethod
    @db_session
    def create(name):
        return Recipe(name=name)

class UserRepository():
    @staticmethod
    @db_session
    def create(name):
        return User(name=name)
'''
@db_session
def add_allergy(name):
    Allergy(name=name)



@db_session
def add_ingredient(name):
    Ingredient(name=name)


@db_session
def add_peanuts():
    allergy = Allergy.select(lambda a: a.name == 'nuts').first()
    ingredient = Ingredient.select(lambda i: i.name == 'peanuts').first()
    ingredient.allergies.add(allergy)

#add_peanuts()

@db_session
def get_ingredients():
    ingredients = Ingredient.select()
    for i in ingredients:
        print(i.name)
        for a in i.allergies:
            print(a.name)

get_ingredients()
'''