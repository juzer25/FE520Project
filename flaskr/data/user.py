from bson import ObjectId
from ..dbconfig import db
from passlib.hash import sha256_crypt
#making function that perform db operation

def signup(userData):

    if userData is None:
        raise BaseException({"code":500, "error":"something went wrong!"})
    
    #conditions to check if the user is already present
    data = db.user.find_one({"email" : userData['email'].lower()})
    if data:
        raise BaseException("User already exists")
    password = sha256_crypt.encrypt(userData['password'])
    newUser = {
        'firstName' : userData['firstName'],
        'lastName' : userData['lastName'],
        'email': userData['email'].lower(),
        'password': password,
        'tickers': []
    }
    insertedUser = db.user.insert_one(newUser)
    res = db.user.find_one({"_id" : insertedUser.inserted_id})
    if res:
        res['_id'] = str(res['_id'])
        return res
    raise BaseException({"code":500, "error":"something went wrong!"})
    

def login(reqbody):
    if reqbody is None:
        raise BaseException("Something went wrong")
    
    data = db.user.find_one({"email":reqbody["email"].lower()})
    
    if data is None:
        raise BaseException("User does not exist!")
    if sha256_crypt.verify(reqbody['password'], data['password']):
        data['_id'] = str(data['_id'])
        return data

    raise IOError("email or password is incorrect") 

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
            "firstName": user['firstName'],
            "lastName" : user['lastName'],
            "email": user['email'],
            "tickers": user['tickers']
        }
        
        return userData
    
    raise BaseException("user does not exist")