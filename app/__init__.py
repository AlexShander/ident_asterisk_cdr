from flask import Flask


app = Flask(__name__)
app.config.from_object('config.Config')
print(app.config)


from app import routes
from app import cdr_redis
