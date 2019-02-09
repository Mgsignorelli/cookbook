from faker import Faker
from pony.orm import db_session, commit
from models import *


class TestSeeder:
    @staticmethod
    def backup():
        if os.path.isfile('../database.sqlite'):
            os.rename('../database.sqlite', '../database.sqlite.backup')

    @staticmethod
    def restore():
        if os.path.isfile('../database.sqlite.backup'):
            if os.path.isfile('../database.sqlite'):
                os.remove('../database.sqlite')
            os.rename('../database.sqlite.backup', '../database.sqlite')

    @staticmethod
    def seed():
        db.drop_all_tables(with_all_data=True)
        db.create_tables()
        fake = Faker()
        with db_session():
            nuts = Allergy(name='Nuts')
            dairy = Allergy(name='Dairy')
            gluten = Allergy(name='Gluten')
            meat = Allergy(name='Meat')

            breakfast = Category(name='Breakfast')
            lunch = Category(name='Lunch')
            dinner = Category(name='Dinner')
            tea = Category(name='Tea')

            steak = Ingredient(name='Steak')
            steak.allergies.add(meat)
            peanut = Ingredient(name='Peanut')
            peanut.allergies.add(nuts)
            wheat = Ingredient(name='Wheat')
            wheat.allergies.add(gluten)
            milk = Ingredient(name='Milk')
            milk.allergies.add(dairy)
            sugar = Ingredient(name='Sugar')

            user = User(name='alpha', email=fake.email(), password='123qwe')
            user.recipes.create(title='Pie', ingredients=[steak, wheat, milk], categories=[dinner],
                                method="\n".join(fake.paragraphs(nb=3)))
            user = User(name='beta', email=fake.email(), password='b123qwe')
            user.recipes.create(title='Bread', ingredients=[steak, peanut, milk], categories=[lunch],
                                method="\n".join(fake.paragraphs(nb=3)))
            user.recipes.create(title='Spaghetti', ingredients=[sugar, wheat, steak], categories=[breakfast],
                                method="\n".join(fake.paragraphs(nb=3)))
            user.recipes.create(title='Pasta Bake', ingredients=[peanut, wheat, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='Pasta', ingredients=[milk, wheat, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 1', ingredients=[peanut, wheat, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 2', ingredients=[peanut, wheat, milk], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 3', ingredients=[milk, wheat, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 4', ingredients=[peanut, steak, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 5', ingredients=[peanut, wheat, steak], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 6', ingredients=[milk, wheat, steak], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 7', ingredients=[sugar, wheat, milk], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 8', ingredients=[peanut, wheat, milk], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 9', ingredients=[milk, wheat, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 10', ingredients=[peanut, steak, sugar], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 11', ingredients=[peanut, wheat, steak], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 12', ingredients=[milk, wheat, steak], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user.recipes.create(title='RECIPE 13', ingredients=[sugar, wheat, milk], categories=[tea],
                                method="\n".join(fake.paragraphs(nb=3)))

            user = User(name='gamma', email=fake.email(), password='g123qwe')
            user = User(name='delta', email=fake.email(), password='d123qwe', is_admin=1)
            commit()


if __name__ == '__main__':
    TestSeeder.backup()
    TestSeeder.seed()
