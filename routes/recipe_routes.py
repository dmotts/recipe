from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

recipe_routes = Blueprint('recipe_routes', __name__)

client = MongoClient(os.getenv('MONGO_URI'))
db = client.recipeDB
recipes_collection = db.recipes

@recipe_routes.route('/')
def list_recipes():
    recipes = recipes_collection.find()
    return render_template('recipe.html', recipes=recipes)

@recipe_routes.route('/recipes', methods=['POST'])
@login_required
def add_recipe():
    new_recipe = {
        "name": request.form.get("name"),
        "ingredients": request.form.getlist("ingredients"),
        "instructions": request.form.get("instructions")
    }
    recipes_collection.insert_one(new_recipe)
    return redirect(url_for('recipe_routes.list_recipes'))

@recipe_routes.route('/recipes/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(id):
    if request.method == 'POST':
        updated_recipe = {
            "name": request.form.get("name"),
            "ingredients": request.form.getlist("ingredients"),
            "instructions": request.form.get("instructions")
        }
        recipes_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_recipe})
        return redirect(url_for('recipe_routes.list_recipes'))
    else:
        recipe = recipes_collection.find_one({"_id": ObjectId(id)})
        return render_template('edit_recipe.html', recipe=recipe)

@recipe_routes.route('/recipes/<id>/delete', methods=['POST'])
@login_required
def delete_recipe(id):
    recipes_collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('recipe_routes.list_recipes'))
