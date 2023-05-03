from bson import ObjectId
from ..dbconfig import db
from datetime import date

def createPost(data):
    print(data)
    if data is None:
        raise IOError("No data provided")
    #Made newpost object
    newPost = {
        "postedOn": str(date.today()),
        "title": data['title'],
        "body": data['body'],
        "by": data['by'],
        "comments": []
    }

    res = db.posts.insert_one(newPost)
    post = db.posts.find_one({"_id":res.inserted_id})
    if post is None:
        raise BaseException("Some error occured!")
    #post['_id'] = str(post['_id'])
    return True

def getAllPosts():
    cursor = db.posts.find()
    posts = []
    for i in cursor:
        postDict = {}
        i['_id'] = str(i['_id'])
        userId = ObjectId(i['by'])
        user = db.user.find_one({'_id':userId})
        postDict = {
            '_id':i['_id'],
            'title':i['title'],
            'body':i['body'],
            'comments':i['comments'],
            'by':user['name'],
            'postedOn':i['postedOn']
        }
        posts.append(postDict)
    return posts

def getUserPosts(id):
    if not id:
        raise IOError("Something went wrong")
    #####
    cursor = db.posts.find({"by":id})
    posts = []
    for i in cursor:
        i['_id'] = str(i['_id'])
        posts.append(i)

    return posts

