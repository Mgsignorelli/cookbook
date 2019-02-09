import unittest
from pony.orm import db_session
from faker import Faker
import repositories
from testseeder import TestSeeder
TestSeeder.backup()
TestSeeder.seed()


class AllergyTest(unittest.TestCase):
    @db_session
    def test_inserting_an_allergy_in_the_database(self):
        fake = Faker()
        test_allergy_name = fake.word()
        allergy = repositories.AllergyRepository().create(name=test_allergy_name)
        self.assertIsNotNone(allergy.id)
        self.assertEqual(allergy.name, test_allergy_name)

    @db_session
    def test_updating_an_allergy_in_the_database(self):
        fake = Faker()
        allergy = repositories.AllergyRepository().get()[0]
        self.assertIsNotNone(allergy.id)
        found_allergy_name = allergy.name
        repositories.AllergyRepository().update(model_id=allergy.id, name=fake.word())
        allergy = repositories.AllergyRepository().get()[0]
        self.assertNotEqual(allergy.name, found_allergy_name)

    @db_session
    def test_deleting_an_allergy_in_the_database(self):
        allergy = repositories.AllergyRepository().find('1')
        self.assertIsNotNone(allergy.id)
        found_allergy_id = allergy.id
        repositories.AllergyRepository().delete(model_id=allergy.id)
        self.assertIsNone(repositories.AllergyRepository().find(model_id=found_allergy_id))


class CategoryTest(unittest.TestCase):
    @db_session
    def test_inserting_a_category_in_the_database(self):
        fake = Faker()
        test_category_name = fake.word()
        category = repositories.CategoryRepository().create(name=test_category_name)
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, test_category_name)

    @db_session
    def test_updating_a_category_in_the_database(self):
        fake = Faker()
        category = repositories.CategoryRepository().get()[0]
        self.assertIsNotNone(category.id)
        found_category_name = category.name
        repositories.CategoryRepository().update(model_id=category.id, name=fake.word())
        category = repositories.CategoryRepository().get()[0]
        self.assertNotEqual(category.name, found_category_name)

    @db_session
    def test_deleting_a_category_in_the_database(self):
        category = repositories.CategoryRepository().find('1')
        self.assertIsNotNone(category.id)
        found_category_id = category.id
        repositories.CategoryRepository().delete(model_id=category.id)
        self.assertIsNone(repositories.CategoryRepository().find(model_id=found_category_id))


class IngredientTest(unittest.TestCase):
    @db_session
    def test_inserting_an_ingredient_in_the_database(self):
        fake = Faker()
        test_ingredient_name = fake.word()
        ingredient = repositories.IngredientRepository().create(name=test_ingredient_name)
        self.assertIsNotNone(ingredient.id)
        self.assertEqual(ingredient.name, test_ingredient_name)

    @db_session
    def test_updating_an_ingredient_in_the_database(self):
        fake = Faker()
        ingredient = repositories.IngredientRepository().get()[0]
        self.assertIsNotNone(ingredient.id)
        found_ingredient_name = ingredient.name
        repositories.IngredientRepository().update(model_id=ingredient.id, name=fake.word(), allergies=ingredient.allergies)
        ingredient = repositories.IngredientRepository().get()[0]
        self.assertNotEqual(ingredient.name, found_ingredient_name)

    @db_session
    def test_deleting_an_ingredient_in_the_database(self):
        ingredient = repositories.IngredientRepository().find('1')
        self.assertIsNotNone(ingredient.id)
        found_ingredient_id = ingredient.id
        repositories.IngredientRepository().delete(model_id=ingredient.id)
        self.assertIsNone(repositories.IngredientRepository().find(model_id=found_ingredient_id))


class RecipeTest(unittest.TestCase):
    @db_session
    def test_inserting_a_recipe_in_the_database(self):
        fake = Faker()
        test_recipe_title = fake.text(max_nb_chars=20)
        user = repositories.UserRepository().find(1)
        method = "\n".join(fake.paragraphs(nb=3))
        categories = ['1']
        ingredients = ['1']
        recipe = repositories.RecipeRepository().create(
            title=test_recipe_title,
            user=user,
            method=method,
            categories=categories,
            ingredients=ingredients
        )
        self.assertIsNotNone(recipe.id)
        self.assertEqual(recipe.title, test_recipe_title)

    @db_session
    def test_updating_a_recipe_in_the_database(self):
        fake = Faker()
        recipe = repositories.RecipeRepository().get()[0]
        self.assertIsNotNone(recipe.id)

        found_recipe_title = recipe.title
        repositories.RecipeRepository().update(model_id=recipe.id, title=fake.word())
        recipe = repositories.RecipeRepository().find(recipe.id)
        self.assertNotEqual(recipe.title, found_recipe_title)

        found_recipe_method = recipe.method
        repositories.RecipeRepository().update(model_id=recipe.id, method="\n".join(fake.paragraphs(nb=3)))
        recipe = repositories.RecipeRepository().find(recipe.id)
        self.assertNotEqual(recipe.method, found_recipe_method)

        found_recipe_ingredients = recipe.ingredients
        repositories.RecipeRepository().update(model_id=recipe.id, ingredients=['2'])
        recipe = repositories.RecipeRepository().find(recipe.id)
        self.assertNotIn('1', recipe.ingredients.id)

        found_recipe_categories = recipe.categories
        repositories.RecipeRepository().update(model_id=recipe.id, categories=['2'])
        recipe = repositories.RecipeRepository().find(recipe.id)
        self.assertNotIn('1', recipe.categories.id)

    @db_session
    def test_deleting_a_recipe_in_the_database(self):
        recipe = repositories.RecipeRepository().find('1')
        self.assertIsNotNone(recipe.id)
        found_recipe_id = recipe.id
        repositories.RecipeRepository().delete(model_id=recipe.id)
        self.assertIsNone(repositories.RecipeRepository().find(model_id=found_recipe_id))


class UserTest(unittest.TestCase):
    @db_session
    def test_inserting_a_user_in_the_database(self):
        fake = Faker()
        test_user_name = fake.name()
        email = fake.email()
        password = fake.password()
        user = repositories.UserRepository().create(name=test_user_name, email=email, password=password)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.name, test_user_name)

    @db_session
    def test_updating_a_user_in_the_database(self):
        fake = Faker()
        user = repositories.UserRepository().get()[0]
        self.assertIsNotNone(user.id)
        found_user_name = user.name
        repositories.UserRepository().update(model_id=user.id, name=fake.name())
        user = repositories.UserRepository().find(user.id)
        self.assertNotEqual(user.name, found_user_name)

        found_user_email = user.email
        repositories.UserRepository().update(model_id=user.id, email=fake.word())
        user = repositories.UserRepository().find(user.id)
        self.assertNotEqual(user.email, found_user_email)

        found_user_password = user.password
        repositories.UserRepository().update(model_id=user.id, password=fake.password())
        user = repositories.UserRepository().find(user.id)
        self.assertNotEqual(user.password, found_user_password)

    @db_session
    def test_deleting_a_user_in_the_database(self):
        user = repositories.UserRepository().find('1')
        self.assertIsNotNone(user.id)
        found_user_id = user.id
        repositories.UserRepository().delete(model_id=user.id)
        self.assertIsNone(repositories.UserRepository().find(model_id=found_user_id))

if __name__ == '__main__':
    unittest.main()
