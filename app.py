from flask import Flask
from my_project.controller.client_controller import client_bp

app = Flask(__name__)
app.register_blueprint(client_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)