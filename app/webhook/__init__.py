# from flask import Flask, render_template
# from app.webhook.routes import webhook
# from app.extensions import init_extensions
#
#
# def create_app():
#     app = Flask(__name__,
#                 static_folder='../static',  # Point to the static folder
#                 static_url_path='',  # This makes static files serve from root
#                 template_folder='../static')  # Use static folder for templates too
#
#     # Initialize extensions
#     init_extensions(app)
#
#     # Register blueprints
#     app.register_blueprint(webhook)
#
#     # Add root route to serve the UI
#     @app.route('/')
#     def home():
#         return render_template('index.html')
#
#     return app