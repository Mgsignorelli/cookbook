#!/usr/bin/env python3
import os
from repositories import *
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, abort


app = Flask('Cookbook')
app.secret_key = os.environ.get('APP_SECRET') if os.environ.get('APP_SECRET') else 'notsecurekey'


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('public/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('public/css', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('public/images', path)


@app.route('/allergy/create')
def allergy_create():
    return render_template('allergy_create.html')


@app.route('/allergy', methods=['POST'])
def allergy_store():
    name = request.form['name']
    AllergyRepository.create(name)
    return redirect(url_for('allergy_index'))


@app.route('/allergy/<allergy_id>')
def allergy_show(allergy_id):
    allergy = AllergyRepository.find(allergy_id)
    if allergy is None:
        return abort(404)
    return render_template('allergy_show.html', allergy=allergy)


@app.route('/allergy/<allergy_id>/edit')
def allergy_edit(allergy_id):
    allergy = AllergyRepository.find(allergy_id)
    if allergy is None:
        return abort(404)
    return render_template('allergy_edit.html', allergy=allergy)


@app.route('/allergy/<allergy_id>', methods=['POST'])
def allergy_update(allergy_id):
    allergy = AllergyRepository.update(allergy_id, request.form['name'])
    if allergy is None:
        return abort(404)
    return redirect(url_for('allergy_index'))


@app.route('/allergy/<allergy_id>/delete', methods=['POST'])
def allergy_delete(allergy_id):
    deleted = AllergyRepository.delete(allergy_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('allergy_index'))


@app.route('/allergy')
def allergy_index():
    return render_template('allergy_index.html', allergies=AllergyRepository.get())


@app.route('/category/create')
def category_create():
    return render_template('category_create.html')


@app.route('/category', methods=['POST'])
def category_store():
    name = request.form['name']
    CategoryRepository.create(name)
    return redirect(url_for('category_index'))


@app.route('/category/<category_id>')
def category_show(category_id):
    category = CategoryRepository.find(category_id)
    if category is None:
        return abort(404)
    return render_template('category_show.html', category=category)


@app.route('/category/<category_id>/edit')
def category_edit(category_id):
    category = CategoryRepository.find(category_id)
    if category is None:
        return abort(404)
    return render_template('category_edit.html', category=category)


@app.route('/category/<category_id>', methods=['POST'])
def category_update(category_id):
    category = CategoryRepository.update(category_id, request.form['name'])
    if category is None:
        return abort(404)
    return redirect(url_for('category_index'))


@app.route('/category/<category_id>/delete', methods=['POST'])
def category_delete(category_id):
    deleted = CategoryRepository.delete(category_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('category_index'))


@app.route('/category')
def category_index():
    return render_template('category_index.html', categories=CategoryRepository.get())


@app.route('/ingredient/create')
def ingredient_create():
    return render_template('ingredient_create.html')


@app.route('/ingredient', methods=['POST'])
def ingredient_store():
    name = request.form['name']
    IngredientRepository.create(name)
    return redirect(url_for('ingredient_index'))


@app.route('/ingredient/<ingredient_id>')
def ingredient_show(ingredient_id):
    ingredient = IngredientRepository.find(ingredient_id)
    if ingredient is None:
        return abort(404)
    return render_template('ingredient_show.html', ingredient=ingredient)


@app.route('/ingredient/<ingredient_id>/edit')
def ingredient_edit(ingredient_id):
    ingredient = IngredientRepository.find(ingredient_id)
    if ingredient is None:
        return abort(404)
    return render_template('ingredient_edit.html', ingredient=ingredient)


@app.route('/ingredient/<ingredient_id>', methods=['POST'])
def ingredient_update(ingredient_id):
    ingredient = IngredientRepository.update(ingredient_id, request.form['name'])
    if ingredient is None:
        return abort(404)
    return redirect(url_for('ingredient_index'))


@app.route('/ingredient/<ingredient_id>/delete', methods=['POST'])
def ingredient_delete(ingredient_id):
    deleted = IngredientRepository.delete(ingredient_id)
    if deleted is None:
        return abort(404)
    return redirect(url_for('ingredient_index'))


@app.route('/ingredient')
def ingredient_index():
    return render_template('ingredient_index.html', ingredients=IngredientRepository.get())



if __name__ == '__main__':
    host = os.environ.get('IP') if os.environ.get('IP') else '0.0.0.0'
    port = int(os.environ.get('PORT') if os.environ.get('PORT') else 8080)
    debug = bool(os.environ.get('DEBUG') if os.environ.get('DEBUG') else False)
    app.run(host, port, debug)
