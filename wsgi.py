import os
from app import app

if __name__ == "__main__":
    # Set production environment
    os.environ["FLASK_ENV"] = "production"
    app.run()
