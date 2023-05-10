from flask import (Blueprint, redirect,render_template, url_for,request,session, Response)
from ..data import user as userData
from ..data import posts as postData
bp = Blueprint('user' , __name__ , url_prefix='/user')


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
        return render_template('error.html', error="404:Page Not Found")
    return render_template("profile.html", user = user, posts = posts, session=session)


##Signup route 
@bp.route('/signup', methods = ['GET','POST'])
def signup():
    #checking if a user is already logged in
    user_id = session.get('user_id')
    if not user_id is None:
        return redirect(url_for('index')) #redirect to main page
        
    if request.method == 'GET':
        return render_template('signup.html')
    
    elif request.method == 'POST':
        req = {
                "firstName": request.form['firstName'],
                "lastName" : request.form['lastName'],
                "email": request.form['email'],
                "password": request.form['password']
            }
        try:
            user = userData.signup(req)
        except BaseException as e:
            return render_template('signup.html',error=e) #will redirect back to signup page
        return redirect(url_for('.login'))
    else:
        return render_template('error.html', error="404:Page Not Found")

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
        except BaseException:
            return redirect(url_for(".login"))
        #creating session
        #https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions
        session['user_id'] = userLogin['_id']
        session['user_name'] = userLogin['firstName']
        return redirect(url_for('index'))
    else:
        return render_template('error.html', error="404:Page Not Found")

#clearing the user session   
# https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions 
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
