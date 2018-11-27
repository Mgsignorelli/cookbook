import os
from pony.orm import Database, Required, Optional, PrimaryKey, Set, LongStr
from flask_login import UserMixin
from dotenv import load_dotenv

load_dotenv()

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


class User(db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    recipes = Set(Recipe)
    name = Required(str)
    email = Required(str, unique=True)
    password = Required(str)


provider = os.environ.get('DB_PROVIDER')

if provider == 'sqlite':
    db.bind(
        provider=provider,
        filename=os.environ.get('DB_DATABASE'),
        create_db=True,
    )

elif provider == 'postgres':
    db.bind(
        provider=provider,
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOSTNAME'),
        database=os.environ.get('DB_DATABASE'),
    )

else:
    raise EnvironmentError('DB_PROVIDER not set to either postgres or sqlite')


db.generate_mapping(create_tables=True)