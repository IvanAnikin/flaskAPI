from flask import Flask, redirect, url_for, request

import os


from database.database import get_countries


app = Flask(__name__)


@app.route('/')
def index():
    return 'Urban Heat Resilient Vulnerability API' 


# /get_countries?continents="asia"
@app.route("/get_countries")
def list_posts_view():
    
    continents = request.args.get('continents')

    countries = get_countries(continents)

    return countries



if __name__ == '__main__':
    _debug = app.config.get('DEBUG', False)

    kwargs = {
        'host': os.getenv('FLASK_HOST', '0.0.0.0'),
        'port': int(os.getenv('FLASK_PORT', '5000')),
        'debug': _debug,
        'use_reloader': app.config.get('USE_RELOADER', _debug),
        **app.config.get('SERVER_OPTIONS', {})
    }

    app.run(debug=True)

    # app.run(**kwargs)