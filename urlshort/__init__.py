from flask import Flask



def create_app(test_config=None):
    app= Flask(__name__) # __name__ : name of module
    # required for secure_name
    app.secret_key=',jhhjjhgj98897979gjhvhj897gjhvjh78yui788b'
    from . import urlshort
    app.register_blueprint(urlshort.bp)
    return app
