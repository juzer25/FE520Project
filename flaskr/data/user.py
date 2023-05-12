from bson import ObjectId
from ..dbconfig import db
from passlib.hash import sha256_crypt
#making function that perform db operation
#signup
def signup(userData):
    #validating data
    if userData is None:
        raise Exception("something went wrong!")
    
    #conditions to check if the user is already present
    data = db.user.find_one({"email" : userData['email'].lower()})
    #if user already present
    if data:
        raise Exception("User already exists")
    #encrypting password
    password = sha256_crypt.encrypt(userData['password'])
    newUser = {
        'firstName' : userData['firstName'],
        'lastName' : userData['lastName'],
        'email': userData['email'].lower(),
        'password': password,
        'tickers': []
    }
    #insert new user into the db
    insertedUser = db.user.insert_one(newUser)
    res = db.user.find_one({"_id" : insertedUser.inserted_id})
    if res:
        res['_id'] = str(res['_id'])
        return res
    raise Exception("something went wrong!")
    
#user login
def login(reqbody):
    if reqbody is None:
        raise Exception("Something went wrong")
    
    data = db.user.find_one({"email":reqbody["email"].lower()})
    
    if data is None:
        raise Exception("User does not exist!")
    #comparing if the password matches
    if sha256_crypt.verify(reqbody['password'], data['password']):
        data['_id'] = str(data['_id'])
        return data

    raise Exception("email or password is incorrect") 

#updating user ticker tracker
def updateTicker(updateUser):
    updateUser['_id'] = ObjectId(updateUser['_id'])
    response = db.user.update_one(
        {'_id':updateUser['_id']},
        {'$set':{'tickers':updateUser['tickers']}}
        )
    
    return response

#getting the user information
def userInfo(id):
    id = ObjectId(id)
    user = db.user.find_one({'_id':id})
    #print(user)
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
    
    raise Exception("user does not exist")