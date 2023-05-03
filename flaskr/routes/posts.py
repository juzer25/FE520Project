from flask import (Blueprint, redirect,render_template, url_for,request,session)
from ..data import user as userData
from ..data import posts as postData
bp = Blueprint('posts' , __name__ , url_prefix='/posts')

@bp.route('/discussions', methods=['GET'])
def discussions():
    posts =  postData.getAllPosts()
    return render_template('discussions.html', posts=posts)


@bp.route('/', methods=['GET','POST'])
def createPost():
    try:
        #Checking session
        user = session.get('user_id')
        if user is None:
            return redirect(url_for('index'))
        if request.method == 'GET':
            return render_template("posts.html", session=user)
        elif request.method == 'POST':
            if request.form['title'] is None or request.form['title'] == ' ':
                return render_template('post.html', error="title cannot be empty")
            title = request.form['title']
            if request.form['body'] is None or request.form['body'] == ' ':
                return render_template('post.html', error="Body cannot be empty")
            body = request.form['body']
          
            payload = {"title":title, "body":body, "by":user}
            '''payload = request.json
            
            payload["by"] = "6445bee4d71c730555259af4"
            '''
            data = postData.createPost(payload)  
            if data: 
                return redirect(url_for('.discussions')) 
        
        else:
            render_template("error.html", error="404")    
    except IOError as e:
        render_template("error.html")

@bp.route("/comment", methods=["POST"])
def createComment():
    print(request.form)
    return redirect(url_for('.discussions'))

