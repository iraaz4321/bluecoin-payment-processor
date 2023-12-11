
import os
from flask import Flask, send_from_directory


ROOT_DIR = './static'  # Define the root directory
TEMPLATE_DIR = "./templates"
ERROR_DIR = os.path.join(TEMPLATE_DIR, 'error')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
    )

    # Set security cookies
    # https://flask.palletsprojects.com/en/2.3.x/security/#set-cookie-options
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # This fixes potential mime type issue which exist in some environments.
    import mimetypes
    mimetypes.add_type('text/javascript', '.js')
    mimetypes.add_type('text/css', '.css')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from flaskr import index
    app.register_blueprint(index.bp)

    #@app.route('/favicon.ico')
    #def favicon():
    #    return send_from_directory(os.path.join(app.root_path, 'static'),
    #                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

    return app




if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8000, debug=True)