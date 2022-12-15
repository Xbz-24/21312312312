from flask import render_template

from app import app

# registramos los controladores de la app
from app.controllers.auth import auth
from app.controllers.quote_controller import quotes


app.register_blueprint(auth)
app.register_blueprint(quotes)


@app.route('/')
def home():
    return render_template('/home.html')


if __name__ == "__main__":
    app.run(debug=True)
