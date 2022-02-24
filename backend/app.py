from check_remarks import db
import check_remarks_dao
import os
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://b2514fae4958b8:16a5852e@us-cdbr-east-05.cleardb.net:3306/heroku_6d3166f8ecfc76d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.route('/', methods=['GET'])
def serviceIsRunning():
    return check_remarks_dao.serviceIsRunning()

@app.route('/<string:tracking_id>', methods=['GET'])
def query_engineers(tracking_id):
    return check_remarks_dao.show_all_remarks_from_tracking_id(tracking_id)

if __name__ == "__main__":
    print("This is flask for " + os.path.basename(__file__) + ": manage remarks by drivers ...")
    app.run(host='0.0.0.0', port=8000, debug=True)