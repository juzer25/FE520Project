from bson import ObjectId
from ..dbconfig import db
from datetime import date
from .user import userInfo
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
            'by':user['email'],
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

def getPost(id):
    id = ObjectId(id)
    post = db.posts.find_one({"_id":id})
    if post:
        post["_id"] = str(post["_id"])
    return post


def createComment(data):
    userId = data['userId']
    postId = data["postId"]
    user = userInfo(userId)
    post = getPost(postId)

    newComment = {
        "_id":ObjectId(),
        "comment": data['comment'],
        "commentBy": user["email"],
        "commentedOn": str(date.today())
    }

    post['comments'].append(newComment)
    response = db.posts.update_one(
        {"_id":ObjectId(postId)},
        {"$set":{'comments':post['comments']}}
    )

    return response

def deletePost(postId):
    if postId is None:
        print("Here")
        raise BaseException("something went wrong!")
    
    postId = ObjectId(postId)
    postDeleted = db.posts.delete_one({"_id":postId})
    print("what about this")
    print(postDeleted)
    if postDeleted.deleted_count > 0:
        return postDeleted.deleted_count
    else:
        print("is it coming here")
        raise BaseException("something went wrong!")

