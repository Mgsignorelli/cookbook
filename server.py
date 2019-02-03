#!/usr/bin/env python3

from forms import RegisterForm, RecipeCreateForm, RecipeEditForm, IngredientCreateForm, AllergyCreateForm, \
    AllergyEditForm, CategoryCreateForm, CategoryEditForm, UserEditForm
from permissions import can
from repositories import *
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort, flash
from dotenv import load_dotenv
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from pony.flask import Pony
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from request_gates import controller_exists_gate, permission_gate
from flask_paginate import Pagination, get_page_parameter

load_dotenv()

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DSN'),
    integrations=[FlaskIntegration()],
    environment=os.environ.get('APP_ENV')
)

app = Flask('Cookbook')
app.secret_key = os.environ.get('APP_SECRET') if os.environ.get('APP_SECRET') else 'notsecurekey'

Pony(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return UserRepository().find(model_id=user_id)


@app.before_request
def before_request():
    if not controller_exists_gate(app=app, request=request):
        return render_template('error.html', error="Not found")

    if not permission_gate(app=app, request=request):
        flash('Permission denied. You are not an Admin!')
        return redirect(url_for('index'))


@app.route('/')
def index():
    most_voted_for_recipes = RecipeRepository.get_recipe_by_vote_count(3)
    return render_template('home.html',
                           categories=CategoryRepository().get(),
                           ingredients=IngredientRepository().get(),
                           most_voted_for_recipes=most_voted_for_recipes
                           )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = UserRepository.authenticate(request.values.get('email'), request.values.get('password'))
        if user is not None:
            login_user(user)
            flash('Logged in successfully.')
            return redirect(request.args.get('next') or url_for('index'))

        flash('Login failed')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.get(email=request.values.get('email'))
        if user is not None:
            flash('Already registered, please log in')
            return redirect(url_for('login'))

        user = UserRepository().create(
            email=request.values.get('email'),
            name=request.values.get('name'),
            password=request.values.get('password'),
        )

        if user is not None:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/browserconfig.xml')
def send_browserconfig(path):
    return send_from_directory('public', path)


@app.route('/manifest.json')
def send_manifestjson(path):
    return send_from_directory('public', path)


@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('public/assets', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('public/images', path)


@app.route('/allergy/create')
@login_required
def allergy_create():
    form = AllergyCreateForm(request.form)
    return render_template('allergy_create.html', form=form)


@app.route('/allergy', methods=['POST'])
def allergy_store():
    form = AllergyCreateForm(request.form)
    if form.validate():
        name = form.name.data
        AllergyRepository().create(name=name)
        return redirect(url_for('allergy_index'))
    return render_template('allergy_create.html', form=form)


@app.route('/allergy/<allergy_id>')
def allergy_show(allergy_id):
    allergy = AllergyRepository().find(allergy_id)
    if allergy is None:
        return abort(404)
    return render_template('allergy_show.html', allergy=allergy)


@app.route('/allergy/<allergy_id>/edit')
def allergy_edit(allergy_id):
    form = AllergyEditForm(request.form)
    allergy = AllergyRepository().find(allergy_id)
    if allergy is None:
        return abort(404)
    return render_template('allergy_edit.html', allergy=allergy, form=form)


@app.route('/allergy/<allergy_id>', methods=['POST'])
def allergy_update(allergy_id):
    form = AllergyEditForm(request.form)

    allergy = AllergyRepository().find(allergy_id)
    if allergy is None:
        return abort(404)

    if form.validate():
        AllergyRepository().update(allergy.id, name=form.name.data)
        return redirect(url_for('allergy_index'))
    return render_template('allergy_edit.html', allergy=allergy, form=form)


@app.route('/allergy/<allergy_id>/delete', methods=['POST'])
def allergy_delete(allergy_id):
    deleted = AllergyRepository().delete(allergy_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('allergy_index'))


@app.route('/allergy')
def allergy_index():
    return render_template('allergy_index.html', allergies=AllergyRepository().get())


@app.route('/category/create')
def category_create():
    form = CategoryCreateForm(request.form)
    return render_template('category_create.html', form=form)


@app.route('/category', methods=['POST'])
def category_store():
    form = CategoryCreateForm(request.form)
    if form.validate():
        CategoryRepository().create(name=form.name.data)
        return redirect(url_for('category_index'))
    return render_template('category_create.html', form=form)


@app.route('/category/<category_id>')
def category_show(category_id):
    category = CategoryRepository().find(category_id)
    if category is None:
        return abort(404)
    return render_template('category_show.html', category=category)


@app.route('/category/<category_id>/edit')
def category_edit(category_id):
    form = CategoryEditForm(request.form)
    category = CategoryRepository().find(category_id)
    if category is None:
        return abort(404)
    return render_template('category_edit.html', category=category, form=form)


@app.route('/category/<category_id>', methods=['POST'])
def category_update(category_id):
    form = CategoryCreateForm(request.form)
    category = CategoryRepository().find(category_id)
    if category is None:
        return abort(404)
    if form.validate():
        CategoryRepository().update(model_id=category_id, name=form.name.data)
        return redirect(url_for('category_index'))
    return render_template('category_edit.html', category=category, form=form)


@app.route('/category/<category_id>/delete', methods=['POST'])
def category_delete(category_id):
    deleted = CategoryRepository().delete(category_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('category_index'))


@app.route('/category')
def category_index():
    return render_template('category_index.html', categories=CategoryRepository().get())


@app.route('/recipe/create')
@login_required
def recipe_create():
    form = RecipeCreateForm(request.form)
    return render_template('recipe_create.html', ingredients=IngredientRepository().get(),
                           categories=CategoryRepository().get(), form=form)


@app.route('/recipe', methods=['POST'])
@login_required
def recipe_store():
    form = RecipeCreateForm(request.form)
    if form.validate():
        RecipeRepository().create(
            user=current_user,
            title=request.form['title'],
            method=request.form['method'],
            ingredients=request.form.getlist('ingredients'),
            categories=request.form.getlist('categories'),
        )
        return redirect(url_for('recipe_index'))

    return render_template('recipe_create.html', ingredients=IngredientRepository().get(),
                           categories=CategoryRepository().get(), form=form)


@app.route('/recipe/<recipe_id>')
def recipe_show(recipe_id):
    recipe = RecipeRepository().find(recipe_id)
    if recipe is None:
        return abort(404)
    votes = RecipeRepository.get_votes_for_recipe(recipe)
    can_vote = True
    if current_user.id in recipe.recipe_votes.user.id:
        can_vote = False
    return render_template('recipe_show.html', recipe=recipe, votes=votes, allergies=set(recipe.ingredients.allergies),
                           can_vote=can_vote)


@app.route('/recipe/<recipe_id>/<vote>', methods=['POST'])
def recipe_vote(recipe_id, vote):
    recipe = RecipeRepository().find(recipe_id)
    if recipe is None:
        return abort(404)
    if current_user.id not in recipe.recipe_votes.user.id:
        if vote == 'up':
            vote = 1
        elif vote == 'down':
            vote = -1
        vote = recipe.recipe_votes.create(vote=vote)
        current_user.recipe_votes.add(vote)
    return redirect(url_for('recipe_show', recipe_id=recipe.id))


@app.route('/recipe/<recipe_id>/edit')
def recipe_edit(recipe_id):
    form = RecipeEditForm(request.form)
    recipe = RecipeRepository().find(recipe_id)
    if recipe is None:
        return abort(404)
    allergies = AllergyRepository().get()
    categories = CategoryRepository().get()
    ingredients = IngredientRepository().get()
    return render_template(
        'recipe_edit.html',
        recipe=recipe,
        allergies=allergies,
        categories=categories,
        ingredients=ingredients,
        form=form,
    )


@app.route('/recipe/<recipe_id>', methods=['POST'])
def recipe_update(recipe_id):
    form = RecipeEditForm(request.form)
    if form.validate():

        recipe = RecipeRepository().update(
            model_id=recipe_id,
            title=request.form['title'],
            ingredients=request.form.getlist('ingredients'),
            categories=request.form.getlist('categories'),
            method=request.form['method']
        )
        if recipe is None:
            return abort(404)
        return redirect(url_for('recipe_index'))
    allergies = AllergyRepository().get()
    categories = CategoryRepository().get()
    ingredients = IngredientRepository().get()
    recipe = RecipeRepository().find(recipe_id)

    return render_template(
        'recipe_edit.html',
        recipe=recipe,
        allergies=allergies,
        categories=categories,
        ingredients=ingredients,
        form=form
    )


@app.route('/recipe/<recipe_id>/delete', methods=['POST'])
def recipe_delete(recipe_id):
    deleted = RecipeRepository().delete(recipe_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('recipe_index'))


@app.route('/recipe')
def recipe_index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    recipes = RecipeRepository().get()
    pagination = Pagination(page=page, total=len(recipes), record_name='recipes', css_framework='bootstrap4')
    page_index = (page - 1) * 10
    return render_template('recipe_index.html', recipes=recipes[page_index:page_index + 10], pagination=pagination)


@app.route('/search')
def recipe_search():
    title = request.values.get('title')
    title = title if title else ''

    categories = request.values.getlist('categories')
    ingredients = request.values.getlist('ingredients')

    recipes = RecipeRepository.search(title=title, categories=categories, ingredients=ingredients)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=len(recipes), record_name='recipes', css_framework='bootstrap4')
    page_index = (page - 1) * 9

    return render_template(
        'recipe_search.html',
        recipes=list(recipes)[page_index:page_index + 9],
        title=title,
        selected_categories=CategoryRepository().find_many(categories),
        selected_ingredients=IngredientRepository().find_many(ingredients),
        categories=CategoryRepository().get(),
        ingredients=IngredientRepository().get(),
        pagination=pagination
    )


@app.route('/ingredient/create')
def ingredient_create():
    form = IngredientCreateForm(request.form)
    allergies = AllergyRepository().get()
    return render_template('ingredient_create.html', allergies=allergies, form=form)


@app.route('/ingredient', methods=['POST'])
def ingredient_store():
    form = IngredientCreateForm(request.form)
    if form.validate():
        name = form.name.data
        allergies = form.allergies.data('allergies')
        IngredientRepository().create(name=name, allergies=allergies)
        return redirect(url_for('ingredient_index'))

    allergies = AllergyRepository().get()
    return render_template('ingredient_create.html', allergies=allergies, form=form)


@app.route('/ingredient/<ingredient_id>')
def ingredient_show(ingredient_id):
    ingredient = IngredientRepository().find(ingredient_id)
    if ingredient is None:
        return abort(404)
    return render_template('ingredient_show.html', ingredient=ingredient)


@app.route('/ingredient/<ingredient_id>/edit')
def ingredient_edit(ingredient_id):
    form = IngredientCreateForm(request.form)
    ingredient = IngredientRepository().find(ingredient_id)

    if ingredient is None:
        return abort(404)
    return render_template('ingredient_edit.html', ingredient=ingredient, allergies=AllergyRepository().get(),
                           form=form)


@app.route('/ingredient/<ingredient_id>', methods=['POST'])
def ingredient_update(ingredient_id):
    form = IngredientCreateForm(request.form)
    ingredient = IngredientRepository().find(ingredient_id)
    if ingredient is None:
        return abort(404)

    if form.validate():
        IngredientRepository().update(model_id=ingredient.id, name=form.name.data, allergies=form.allergies.data)
        return redirect(url_for('ingredient_index'))

    return render_template('ingredient_edit.html', ingredient=ingredient, allergies=AllergyRepository().get(),
                           form=form)


@app.route('/ingredient/<ingredient_id>/delete', methods=['POST'])
def ingredient_delete(ingredient_id):
    deleted = IngredientRepository().delete(ingredient_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('ingredient_index'))


@app.route('/ingredient')
def ingredient_index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    ingredients = IngredientRepository().get()
    pagination = Pagination(page=page, total=len(ingredients), record_name='ingredients', css_framework='bootstrap4')
    page_index = (page - 1) * 10
    return render_template('ingredient_index.html', ingredients=ingredients[page_index:page_index + 10],
                           pagination=pagination)


@app.route('/user/<user_id>')
def user_show(user_id):
    user = UserRepository().find(user_id)
    if user is None:
        return abort(404)
    return render_template('user_show.html', user=user)


@app.route('/user/<user_id>/edit')
def user_edit(user_id):
    form = UserEditForm(request.form)
    user = UserRepository().find(user_id)
    if user is None:
        return abort(404)
    return render_template('user_edit.html', user=user, form=form)


@app.route('/user/<user_id>', methods=['POST'])
def user_update(user_id):
    form = UserEditForm(request.form)
    user = UserRepository().find(user_id)
    if user is None:
        return abort(404)
    if form.validate():
        UserRepository().update(model_id=user.id, name=form.name.data, email=form.email.data,
                                password=form.password.data)
        return redirect(url_for('user_index'))
    return render_template('user_edit.html', user=user, form=form)


@app.route('/user/<user_id>/delete', methods=['POST'])
def user_delete(user_id):
    deleted = UserRepository().delete(user_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('user_index'))


@app.route('/user')
def user_index():
    return render_template('user_index.html', users=UserRepository().get())


if __name__ == '__main__':
    host = os.environ.get('IP') if os.environ.get('IP') else '0.0.0.0'
    port = int(os.environ.get('PORT') if os.environ.get('PORT') else 8080)
    debug = bool(os.environ.get('DEBUG') if os.environ.get('DEBUG') else False)
    app.jinja_env.globals.update(can=can)
    app.run(host, port, debug)
