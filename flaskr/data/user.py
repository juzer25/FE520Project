from bson import ObjectId
from ..dbconfig import db

#making function that perform db operation

def signup(userData):
    #conditions to check if the user is already present
    #print("Userdata = ",userData)
    
    data = db.user.find_one({"email" : userData['email'].lower()})
    if data:
        raise BaseException("User already exists")
    
    newUser = {
        'name' : userData['name'],
        'email': userData['email'].lower(),
        'password': userData['password'],
        'tickers': []
    }
    
    db.user.insert_one(newUser)
    res = db.user.find_one({"email" : newUser['email']})
    res['_id'] = str(res['_id'])
    
    return res

def login(reqbody):
    data = db.user.find_one({"email":reqbody["email"]})

    if reqbody['password'] == data['password']:
        data['_id'] = str(data['_id'])
        return data

    raise IOError("email or password is wrong") 

def updateTicker(updateUser):
    updateUser['_id'] = ObjectId(updateUser['_id'])
    response = db.user.update_one(
        {'_id':updateUser['_id']},
        {'$set':{'tickers':updateUser['tickers']}}
        )
    
    return response

def userInfo(id):
    id = ObjectId(id)
    user = db.user.find_one({'_id':id})
    print(user)
    if user:
        #print("here")
        user['_id'] = str(user['_id'])
        userData = {
            "_id" : user['_id'],
            "name": user['name'],
            "email": user['email'],
            "tickers": user['tickers']
        }
        
        return userData
    
    raise BaseException("user does not exist")