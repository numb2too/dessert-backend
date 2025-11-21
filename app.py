from apiflask import APIFlask
from routes.user_routes import user_bp

app = APIFlask(__name__)
app.register_blueprint(user_bp, url_prefix="/api/users")

if __name__ == "__main__":
    app.run(debug=True)
