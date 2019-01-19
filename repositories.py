from pony.orm import ObjectNotFound, select, flush, commit

from models import *


class AllergyRepository:
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
    def find_many(ids):
        found = set()

        for id in ids:
            try:
                found.add(Allergy[id])
            except ObjectNotFound:
                continue

        return found

    @staticmethod
    def update(id, name):
        try:
            allergy = Allergy[id]
        except ObjectNotFound:
            return None

        allergy.name = name
        commit()
        return Allergy[id]

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


class CategoryRepository:
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
    def find_many(ids):
        found = set()

        for id in ids:
            try:
                found.add(Category[id])
            except ObjectNotFound:
                continue

        return found

    @staticmethod
    def update(id, name):
        try:
            category = Category[id]
        except ObjectNotFound:
            return None

        category.name = name
        commit()
        return Category[id]

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


class RecipeRepository:
    @staticmethod
    def create(title, user, method, ingredients, categories):
        recipe = user.recipes.create(
            title=title,
            method=method,
        )

        for ingredient in ingredients:
            if ingredient.isdigit():
                try:
                    recipe.ingredients.add(Ingredient[ingredient])
                except ObjectNotFound:
                    continue
            else:
                recipe.ingredients.create(name=ingredient)

        for category in categories:
            if category.isdigit():
                try:
                    recipe.categories.add(Category[category])
                except ObjectNotFound:
                    continue
            else:
                recipe.categories.create(name=category)

        return recipe

    @staticmethod
    def find(id):
        try:
            return Recipe[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def find_many(ids):
        found = set()

        for id in ids:
            try:
                found.add(Recipe[id])
            except ObjectNotFound:
                continue

        return found

    @staticmethod
    def update(id, title=None, categories=None, ingredients=None, method=None):
        try:
            recipe = Recipe[id]
        except ObjectNotFound:
            return None

        if title:
            recipe.title = title
        if method:
            recipe.method = method
        if categories:
            recipe.categories.clear()
            for category in categories:
                if category.isdigit():
                    try:
                        recipe.categories.add(Category[category])
                    except ObjectNotFound:
                        continue
                else:
                    recipe.categories.create(name=category)
        if ingredients:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                if ingredient.isdigit():
                    try:
                        recipe.ingredients.add(Ingredient[ingredient])
                    except ObjectNotFound:
                        continue
                else:
                    recipe.ingredients.create(name=ingredient)

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

    @staticmethod
    def get_votes_for_recipe(recipe):
        upvotes = len(recipe.recipe_votes.filter(lambda vote: vote.vote > 0)[:])
        downvotes = len(recipe.recipe_votes.filter(lambda vote: vote.vote < 0)[:])
        return [upvotes, downvotes]

    @staticmethod
    def search(title='', categories=None, ingredients=None):
        query = set(Recipe.select(lambda r: title.lower() in r.title.lower()))
        query_sets = []

        if categories:
            for category in categories:
                category = Category[category]
                query_sets.append(set(category.recipes))

        if ingredients:
            for ingredient in ingredients:
                ingredient = Ingredient[ingredient]
                query_sets.append(set(ingredient.recipes))

        return query.intersection(*query_sets)


class IngredientRepository:
    @staticmethod
    def create(name, allergies=[]):
        ingredient = Ingredient(name=name)
        for allergy in allergies:
            if allergy.isdigit():
                try:
                    ingredient.allergies.add(Allergy[allergy])
                except ObjectNotFound:
                    continue
            else:
                ingredient.allergies.create(name=allergy)
        return ingredient

    @staticmethod
    def find(id):
        try:
            return Ingredient[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def find_many(ids):
        found = set()

        for id in ids:
            try:
                found.add(Ingredient[id])
            except ObjectNotFound:
                continue

        return found

    @staticmethod
    def update(id, name, allergies=[]):
        try:
            ingredient = Ingredient[id]
        except ObjectNotFound:
            return None

        ingredient.name = name
        ingredient.allergies.clear()

        for allergy in allergies:
            if allergy.isdigit():
                try:
                    ingredient.allergies.add(Allergy[allergy])
                except ObjectNotFound:
                    continue
            else:
                ingredient.allergies.create(name=allergy)

        commit()
        return Ingredient[id]

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


class UserRepository:
    @staticmethod
    def create(name, email, password):
        user = User(name=name, email=email, password=password)
        flush()
        return user

    @staticmethod
    def find(id):
        try:
            return User[id]
        except ObjectNotFound:
            return None

    @staticmethod
    def find_many(ids):
        found = set()

        for id in ids:
            try:
                found.add(User[id])
            except ObjectNotFound:
                continue

        return found

    @staticmethod
    def update(id, name=None, email=None, password=None):
        try:
            user = User[id]
        except ObjectNotFound:
            return None

        if name:
            user.name = name
        if email:
            user.email = email
        if password:
            user.password = password

        commit()
        return User[id]

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
        user = UserRepository.get_by_email(email=email)
        if user is not None and user.password == password:
            return user
        return None

    @staticmethod
    def get_by_email(email):
        return User.get(email=email)
