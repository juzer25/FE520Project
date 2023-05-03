from flask import (Blueprint, redirect,render_template, url_for,request,session)
from ..data import user as userData
from ..data import posts as postData
bp = Blueprint('user' , __name__ , url_prefix='/user')


#### need to add checks but for now all this works

##get user
@bp.route('/<id>', methods = ['GET'])
def getUser(id):
    try:
        if id is None or not isinstance(id,str):
            return redirect(url_for('index'))
        user = session.get('user_id')
        if not user:
            return redirect(url_for('index'))
        if user != id:
            return redirect(url_for('index'))
        user = userData.userInfo(id)
        #print(user)
        posts = postData.getUserPosts(id)
    except BaseException:
        return "404"
    return render_template("profile.html", user = user, posts = posts, session=user)


##Signup route 
@bp.route('/signup', methods = ['GET','POST'])
def signup():
    #reference from flask tutorial
    user_id = session.get('user_id')
    if not user_id is None:
        return redirect(url_for('index')) #redirect to main page
        
    if request.method == 'GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        req = {
                "name": request.form['name'],
                "email": request.form['email'],
                "password": request.form['password']
            }
        try:
            user = userData.signup(req)
        except BaseException:
            return "somewhere" #will redirect back to signup page
        return redirect(url_for('.login'))
    else:
        return {"404":"does not exist"}

##Login route
@bp.route('/login', methods = ['GET','POST'])
def login():
    #reference from flask tutorial
    user_id = session.get('user_id')
    if not user_id is None:
        return redirect(url_for('index')) #redirect to main page
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        ##login stuff
        req = { 
            "email": request.form['email'],
            "password" : request.form['password']
            }
        try:
            userLogin = userData.login(req)
        except IOError:
            return "loginpage"
        session['user_id'] = userLogin['_id']
        return redirect(url_for('index'))
    else:
        return {"404":"does not exist"}
    
@bp.route('/logout', methods = ['GET'])
def logout():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('index')) #redirect to main page
    
    session.clear()
    return redirect(url_for('index'))

def checkSession():
    user_id = session.get('user_id')
    if user_id is None:
        return None
    return session
