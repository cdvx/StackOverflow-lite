from app import app
from config import Config

app.config.from_object(Config)
