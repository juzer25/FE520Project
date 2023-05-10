from flask import (current_app,Blueprint, redirect,render_template, url_for,request,session,Response,make_response)
from ..data import user as userData
from ..data import posts as postData
from .user import checkSession
from werkzeug.exceptions import HTTPException
bp = Blueprint('posts' , __name__ , url_prefix='/posts')

#Getting the discussion page
@bp.route('/discussions', methods=['GET'])
def discussions():
    posts =  postData.getAllPosts()
    user = checkSession()
    #if user:
     #   user = user.get('user_id')
    return render_template('discussions.html', posts=posts, session=user if user else None)

#route to create a post
@bp.route('/', methods=['GET','POST'])
def createPost():
    try:
        #Checking session
        user = session.get('user_id')
        if user is None:
            return redirect(url_for('index'), code=401)
        if request.method == 'GET':
            return render_template("posts.html", session=session)
        elif request.method == 'POST':
            #Validating the inputs
            if request.form['title'] is None or request.form['title'] == ' ':
                return render_template('post.html', error="title cannot be empty")
            title = request.form['title']
            if request.form['body'] is None or request.form['body'] == ' ':
                return render_template('post.html', error="Body cannot be empty")
            body = request.form['body']
          
            payload = {"title":title, "body":body, "by":user}

            data = postData.createPost(payload)  
            if data: 
                return redirect(url_for('.discussions'))
        else:
            render_template("error.html", error="404")    
    except IOError as e:
        render_template("error.html")

#Allows users to make comments
@bp.route("/comment", methods=["POST"])
def createComment():
    user = session.get("user_id")

    if user is None:
       return redirect(url_for('.discussions'), code=401) 
    comment = request.form.get("comment")
    postId = request.form.get("postId")
    if comment is None:
        return redirect(url_for('.discussions'), code=400)
    if comment.isspace():
        return redirect(url_for('.discussions'), code=400)
    if postId is None:
        return redirect(url_for('.discussions'), code=400)
    if postId.isspace():
        return redirect(url_for('.discussions'), code=400)
    
    data = {
        "comment":comment,
        "postId":postId,
        "userId": user
    }
    comment = postData.createComment(data)
    return redirect(url_for('.discussions'))

