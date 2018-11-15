#!/usr/bin/env python3
import os
from repositories import *
from flask import Flask, request, redirect, url_for, render_template, send_from_directory

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

@app.route('/admin/allergy_create')
def allergy_create():
    return render_template('allergy_create.html')

@app.route('/admin/allergy_create', methods=['POST'])
def allergy_save():
    name = request.form['name']
    AllergyRepository.create(name)
    return redirect(url_for('allergy_create'))

if __name__ == '__main__':
    host = os.environ.get('IP') if os.environ.get('IP') else '0.0.0.0'
    port = int(os.environ.get('PORT') if os.environ.get('PORT') else 8080)
    debug = bool(os.environ.get('DEBUG') if os.environ.get('DEBUG') else False)
    app.run(host, port, debug)
