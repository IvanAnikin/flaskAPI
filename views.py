from flask import Blueprint
from flask import render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from extensions import db

from .forms import PostForm
from .models import Post

from database.database import get_countries

app = Blueprint('blog', __name__, template_folder='templates')


@app.route("/")
def list_posts_view():
    posts = Post.query.all()
    return render_template('index.html')


@app.route("/get_countries")
def list_posts_view():
    
    continents = request.args.get('continents')

    countries = get_countries(continents)

    return render_template('index.html', countries=countries)
