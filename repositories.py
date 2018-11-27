import sys

from pony.orm import ObjectNotFound, select

from models import *


class AllergyRepository():
    @staticmethod
    def create(name):
        return Allergy(name=name)

    @staticmethod
    def find(id):
        try:
            return Allergy[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def update(id, name):
        try:
            allergy = Allergy[id]
        except ObjectNotFound:
            return None

        allergy.name = name
        return allergy

    @staticmethod
    def get():
        return select(a for a in Allergy).order_by(Allergy.name)[:]


    @staticmethod
    def delete(id):
        try:
            allergy = Allergy[id]
        except ObjectNotFound:
            return None

        allergy.delete()
        return True


class CategoryRepository():
    @staticmethod
    def create(name):
        return Category(name=name)


    @staticmethod
    def find(id):
        try:
            return Category[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def update(id, name):
        try:
            category = Category[id]
        except ObjectNotFound:
            return None

        category.name = name
        return category

    @staticmethod
    def get():
        return select(a for a in Category).order_by(Category.name)[:]


    @staticmethod
    def delete(id):
        try:
            category = Category[id]
        except ObjectNotFound:
            return None

        category.delete()
        return True

class RecipeRepository():
    @staticmethod
    def create(title, user, method, ingredients, categories):
    def create(title):
        return Recipe(title=title)

    @staticmethod
    def find(id):
        try:
            return Recipe[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def update(id, title):
        try:
            recipe = Recipe[id]
        except ObjectNotFound:
            return None

        recipe.title = title
        return recipe


    @staticmethod
    def get():
        return select(a for a in Recipe).order_by(Recipe.title)[:]


    @staticmethod
    def delete(id):
        try:
            recipe = Recipe[id]
        except ObjectNotFound:
            return None

        recipe.delete()
        return True

class IngredientRepository():
    @staticmethod
    def create(name):
        return Ingredient(name=name)


    @staticmethod
    def find(id):
        try:
            return Ingredient[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def update(id, name, allergies):
        try:
            ingredient = Ingredient[id]
        except ObjectNotFound:
            return None

        ingredient.name = name
        newAllergies = []
        for allergy in allergies:
            print(allergy, file=sys.stderr)

            try:
                newAllergies.append(Allergy[allergy])
            except ObjectNotFound:
                return None

        ingredient.allergies.clear()
        for allergy in newAllergies:
            ingredient.allergies.add(allergy)

        return ingredient

    @staticmethod
    def get():
        return select(a for a in Ingredient).order_by(Ingredient.name)[:]


    @staticmethod
    def delete(id):
        try:
            ingredients = Ingredient[id]
        except ObjectNotFound:
            return None

        ingredients.delete()
        return True


class UserRepository():
    @staticmethod
    def create(name, email, password):
        return User(name=name, email=email, password=password)


    @staticmethod
    def find(id):
        try:
            return User[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def update(id, name, email, password):
        try:
            user = User[id]
        except ObjectNotFound:
            return None

        user.name = name
        user.email = email
        user.password = password
        return user

    @staticmethod
    def get():
        return select(a for a in User).order_by(User.name)[:]


    @staticmethod
    def delete(id):
        try:
            users = User[id]
        except ObjectNotFound:
            return None

        users.delete()
        return True

    @staticmethod
    def authenticate(email, password):
        user = User.get(email=email)
        if user is not None and user.password == password:
            return user
        return None


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