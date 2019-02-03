from pony.orm import ObjectNotFound, select, flush, commit, desc

from models import *


class Repository:
    def get_repository_model(self):
        return self.repository_model

    def get_repository_fields(self):
        return self.repository_fields

    def get_assignable_fields_from_kwargs(self, kwargs):
        derived_fields = {}
        for field, options in self.get_repository_fields().items():
            if field in kwargs and options['type'] != 'collection' and options['type'] != 'model':
                derived_fields[field] = kwargs[field]

        return derived_fields

    def get_collection_fields_from_kwargs(self, kwargs):
        derived_fields = {}
        for field, options in self.get_repository_fields().items():
            if field in kwargs and options['type'] == 'collection':
                derived_fields[field] = kwargs[field]

        return derived_fields

    def get_model_field_from_kwargs(self, kwargs):
        for field, options in self.get_repository_fields().items():
            if field in kwargs and options['type'] == 'model':
                return kwargs[field]
        return None

    def get_repository_model_field(self):
        for field, options in self.get_repository_fields().items():
            if options['type'] == 'model':
                return options
        return None

    def create(self, **kwargs):
        owner_model = self.get_model_field_from_kwargs(kwargs)
        if owner_model is None:
            model = self.get_repository_model()(**self.get_assignable_fields_from_kwargs(kwargs=kwargs))
        else:
            model = getattr(owner_model, self.get_repository_model_field()['key']) \
                .create(**self.get_assignable_fields_from_kwargs(kwargs=kwargs))

        for field, value in self.get_collection_fields_from_kwargs(kwargs).items():
            for item in value:
                if item.isdigit():
                    try:
                        getattr(model, field).add(self.repository_fields[field]['model'][item])
                    except ObjectNotFound:
                        continue
                else:
                    getattr(model, field).create(**{self.repository_fields[field]['key']: item})
        commit()
        return model

    def find(self, model_id):
        if model_id is None:
            return None
        try:
            return self.get_repository_model()[model_id]
        except ObjectNotFound:
            return None

    def find_many(self, model_ids):
        found = set()

        for model_id in model_ids:
            try:
                found.add(self.get_repository_model()[model_id])
            except ObjectNotFound:
                continue

        return found

    def update(self, model_id, **kwargs):
        try:
            model = self.get_repository_model()[model_id]
        except ObjectNotFound:
            return None

        for field, value in self.get_assignable_fields_from_kwargs(kwargs).items():
            setattr(model, field, value)

        for field, value in self.get_collection_fields_from_kwargs(kwargs).items():
            getattr(model, field).clear()
            for item in value:
                if item.isdigit():
                    try:
                        getattr(model, field).add(self.repository_fields[field]['model'][item])
                    except ObjectNotFound:
                        continue
                else:
                    getattr(model, field).create(**{self.repository_fields[field]['key']: item})

        commit()
        return self.find(model_id=model_id)

    def get(self):
        return select(m for m in self.get_repository_model()).order_by(
            getattr(self.get_repository_model(), self.default_sort_field))[:]

    def delete(self, model_id):
        try:
            model = self.get_repository_model()[model_id]
        except ObjectNotFound:
            return None

        model.delete()
        return True


class AllergyRepository(Repository):
    def __init__(self):
        self.repository_model = Allergy
        self.default_sort_field = 'name'
        self.repository_fields = {
            'name': {'type': 'string'}
        }


class CategoryRepository(Repository):
    def __init__(self):
        self.repository_model = Category
        self.default_sort_field = 'name'
        self.repository_fields = {
            'name': {'type': 'string'}
        }

    @staticmethod
    def get_most_popular_categories_with_recipe(limit=5):
        categories = select(m for m in Category).order_by(lambda c: desc(sum(c.recipes.recipe_votes.vote))).limit(limit)

        most_voted_for_category_recipes = []

        for c in categories:
            most_voted_for_category_recipes.append({
                "recipe": RecipeRepository.get_most_popular_recipe_in_category(c),
                "category": c
            })

        return most_voted_for_category_recipes


class RecipeRepository(Repository):
    def __init__(self):
        self.repository_model = Recipe
        self.default_sort_field = 'title'
        self.repository_fields = {
            'title': {'type': 'string'},
            'method': {'type': 'string'},
            'ingredients': {'type': 'collection', 'model': Ingredient, 'key': 'name'},
            'categories': {'type': 'collection', 'model': Category, 'key': 'name'},
            'user': {'type': 'model', 'model': User, 'key': 'recipes'},
        }

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

    @staticmethod
    def get_recipe_by_vote_count(limit=3):
        return select(m for m in Recipe).order_by(lambda r: desc(sum(r.recipe_votes.vote))).limit(limit)

    @staticmethod
    def get_most_popular_recipe_in_category(category):
        return category.recipes.order_by(lambda c: desc(sum(c.recipe_votes.vote))).first()


class IngredientRepository(Repository):
    def __init__(self):
        self.repository_model = Ingredient
        self.default_sort_field = 'name'
        self.repository_fields = {
            'name': {'type': 'string'},
            'allergies': {'type': 'collection', 'model': Allergy, 'key': 'name'},
        }


class UserRepository(Repository):
    def __init__(self):
        self.repository_model = User
        self.default_sort_field = 'name'
        self.repository_fields = {
            'name': {'type': 'string'},
            'email': {'type': 'string'},
            'password': {'type': 'password'},
            'is_admin': {'type': 'boolean'},
        }

    @staticmethod
    def authenticate(email, password):
        user = User.get(email=email)
        if user is not None and user.password == password:
            return user
        return None
