from flask import Flask


app = Flask(__name__)
app.config.from_object('config.Config')
print(app.config)

if __name__ == '__main__':
    app.run(host='0.0.0.0')


from app import routes
from app import cdr_redis
