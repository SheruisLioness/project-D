from flask import Flask,render_template,Blueprint,redirect,url_for


abtusbp = Blueprint('abtusbp',__name__)

@abtusbp.route('/aboutus',methods=['GET','POST'])
def aboutusindex():
    return render_template('aboutus.html')