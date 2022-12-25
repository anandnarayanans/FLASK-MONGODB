from flask import Flask

from flask_pymongo import pymongo

from bson.json_util import dumps
from bson.objectid import ObjectId

from flask import jsonify,request

from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.secret_key="asd"


con_string = "mongodb+srv://anands2001:QyxZoFp6VLeI1NjA@cluster0.qc5haeq.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('user')

user_collection = pymongo.collection.Collection(db, 'demo') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")


@app.route('/add',methods=['POST'])
def add_user():
    json=request.json
    name=json['name']
    email=json['email']
    password=json['pwd']
    
    if name and email and password and request.method=='POST':
        hashed_password=generate_password_hash(password)
        _id=user_collection.insert_one({'name':name, 'email':email, 'pwd':hashed_password})
        resp=jsonify("User added SuccessFully")
        resp.status_code=200
        
        return resp
    return not_found()




@app.route('/users',methods=['GET'])
def users():
    users=user_collection.find()
    resp=dumps(users)
    return resp

@app.route('/user/<id>')
def user(id):
    user=user_collection.find_one({'_id':ObjectId(id)})
    resp=dumps(user)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def delete_user(id):
    user_collection.delete_one({'_id':ObjectId(id)})
    resp=jsonify("USer DEleted Successfully")
    resp.status_code=200
    
    return resp


@app.route('/update/<id>',methods=['PUT'])
def update_user(id):
    _id=id
    json=request.json
    name=json['name']
    email=json['email']
    password=json['pwd']
    
    if name and email and password and request.method=='PUT':
        hashed_password=generate_password_hash(password)
        
        user_collection.update_one({'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},{'$set':{'name':name, 'email':email, 'pwd':hashed_password}})
        resp=jsonify("Updated Successfuly")
        resp.status_code=200
        return resp
    return not_found()
    



@app.errorhandler(404)
def not_found(error=None):
    message={
        'status':404,
        'message':'Not FOund '+ request.url
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp



if __name__=='__main__':
    app.run(debug=True)

