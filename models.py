from pony.orm import *


db = Database()


class Allergy(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    ingredients = Set('Ingredient')


class Category(db.Entity):
    id = PrimaryKey(int, auto=True)
    recipes = Set('Recipe')
    name = Required(str)


class Recipe(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required('User')
    categories = Set(Category)
    title = Required(str)
    method = Required(LongStr)
    upvotes = Optional(int, unsigned=True)
    downvotes = Optional(int, unsigned=True)
    ingredients = Set('Ingredient')


class Ingredient(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    allergies = Set(Allergy)
    recipes = Set(Recipe)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    recipes = Set(Recipe)
    name = Required(str)
    email = Required(str)
    password = Required(str)


db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)