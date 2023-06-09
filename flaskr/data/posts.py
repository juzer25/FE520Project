﻿from bson import ObjectId
from ..dbconfig import db
from datetime import date
from .user import userInfo

#Creating posts to insert into db
def createPost(data):
    #print(data)
    #validating input
    if data is None:
        raise BaseException("No data provided")
    #Made newpost object
    newPost = {
        "postedOn": str(date.today()),
        "title": data['title'],
        "body": data['body'],
        "by": data['by'],
        "comments": []
    }
    #insert into db
    res = db.posts.insert_one(newPost)
    post = db.posts.find_one({"_id":res.inserted_id})
    if post is None:
        raise BaseException("Some error occured!")
    #post['_id'] = str(post['_id'])
    return True

#get all the users posts
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

#get single user's post
def getUserPosts(id):
    if not id:
        raise Exception("Something went wrong")
    #####
    cursor = db.posts.find({"by":id})
    posts = []
    for i in cursor:
        i['_id'] = str(i['_id'])
        posts.append(i)

    return posts

#get a single post
def getPost(id):
    id = ObjectId(id)
    post = db.posts.find_one({"_id":id})
    if post:
        post["_id"] = str(post["_id"])
    return post

#Create a comment made by a user
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
    #updating the comments of the post
    post['comments'].append(newComment)
    response = db.posts.update_one(
        {"_id":ObjectId(postId)},
        {"$set":{'comments':post['comments']}}
    )
    return response

#
def deletePost(postId):
    if postId is None:
        #print("Here")
        raise Exception("something went wrong!")
    #delete a post
    postId = ObjectId(postId)
    postDeleted = db.posts.delete_one({"_id":postId})
    #print("what about this")
    #print(postDeleted)
    #validating delete count
    if postDeleted.deleted_count > 0:
        return postDeleted.deleted_count
    else:
        #print("is it coming here")
        raise Exception("something went wrong!")

