from flask import Flask, render_template,url_for,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from email.message import EmailMessage
import json,smtplib
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'aksdjapi09842023840@994809324'
local_server = True
with open('conf.json','r') as c:
    params = json.load(c)["params"]

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)

if(local_server==True):
    app.config['SQLALCHEMY_DATABASE_URI']=params['local_server']
else:
    app.config['SQLALCHEMY_DATABASE_URI']=params['Production_server']    

db = SQLAlchemy(app)

class skills(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50), nullable=False)
    expert = db.Column(db.Integer, nullable=False)

class clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clients = db.Column(db.Integer, nullable=False)
    project = db.Column(db.Integer, nullable=False)
    workhour = db.Column(db.Integer, nullable=False)
    award = db.Column(db.Integer, nullable=False)

class contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namez = db.Column(db.String(50), nullable=False)
    subjects = db.Column(db.String(50), nullable=False)
    msg = db.Column(db.String(200), nullable=False)
    dates = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class ports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typew = db.Column(db.String(50), nullable=False)
    type1 = db.Column(db.String(50), nullable=False)
    namez = db.Column(db.String(80), nullable=False)
    image = db.Column(db.String(80), nullable=True)
    link = db.Column(db.String(300), nullable=False)


@app.route('/',methods=['POST','GET'])
def main():
    s = skills.query.all()
    work = ports.query.all()
    c = clients.query.filter_by(id=1).first()
    if(request.method=='POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = contacts(namez=name, subjects = subject, msg = message, dates= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
        msg = EmailMessage()
        msg.set_content('Blog Website Programming With Zaryab' '\n' 'Message From: ' + name + '\n' 'Message: ' + message + '\n' 'Subject: '+ subject)
        msg['Subject'] = 'New Message :)'
        msg['From'] =  email
        msg['To'] =params['gmail-user']
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(params['gmail-user'], params['gmail-password'])
        server.send_message(msg)
    return render_template('index.html',params=params,s=s,c=c,work=work),404
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if ('user' in session and session['user'] == params['UserName']):
        s = skills.query.all()
        work = ports.query.all()
        c = clients.query.filter_by(id=1).first()
        return render_template('dashboard.html', params=params, s=s,work=work,c=c)
    if request.method=='POST':
        username = request.form.get('uname')
        userpass = request.form.get('pass')
        if (username == params['UserName'] and userpass == params['Password']):
            session['user'] = username
            s = skills.query.all()
            work = ports.query.all()
            c = clients.query.filter_by(id=1).first()
            return render_template('dashboard.html', params=params, s=s,work=work,c=c)
    return render_template('login.html', params=params)

@app.route('/NewPost',methods=['POST','GET'])
def NewPost():
    if(request.method=='POST'):
        typew = request.form.get('typew')
        type1 = request.form.get('type1')
        namez = request.form.get('namez')
        image = request.form.get('image')
        link = request.form.get('link')
        entry = ports(typew=typew,type1=type1,namez=namez,image=image,link=link)
        db.session.add(entry)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit1.html'),404

@app.route('/NewSkill',methods=['POST','GET'])
def NewSkill():
    if(request.method=='POST'):
        skill = request.form.get('skill')
        expert = request.form.get('expert')
        entry = skills(skill=skill,expert=expert)
        db.session.add(entry)
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit2.html'),404

@app.route('/editskill/<id>',methods=['POST','GET'])
def NewSkill2(id):
    s = skills.query.filter_by(id=id).first()
    if(request.method=='POST'):
        skill = request.form.get('skill')
        expert = request.form.get('expert')
        s.skill = skill
        s.expert = expert
        db.session.commit()
        return redirect('/dashboard')
    return render_template('editskill.html',s=s),404

@app.route("/editproject/<id>",methods=['POST','GET'])
def editproject(id):
    work = ports.query.filter_by(id=id).first()
    if (request.method=='POST'):
        typew = request.form.get('typew')
        type1 = request.form.get('type1')
        namez = request.form.get('namez')
        image = request.form.get('image')
        link = request.form.get('link')
        work.typew = typew
        work.type1 = type1
        work.namez = namez
        work.image = image
        work.link = link
        db.session.commit()
        return redirect('/dashboard')
    return render_template('editproject.html',work=work),404

@app.route("/edit/<int:id>",methods=['POST','GET'])
def edit(id):
    c = clients.query.filter_by(id=id).first()
    if (request.method=='POST'):
        client = request.form.get('client')
        project = request.form.get('project')
        workhour = request.form.get('workhour')
        award = request.form.get('award')
        print(c.clients)
        c.clients=client
        c.project=project
        c.workhour=workhour
        c.award=award
        db.session.commit()
        return redirect('/dashboard')
    return render_template('edit.html',c=c),404

@app.route("/delete/<int:id>", methods = ['GET', 'POST'])
def delete(id):
    if ('user' in session and session['user'] == params['UserName']):
        work = ports.query.filter_by(id=id).first()
        db.session.delete(work)
        db.session.commit()
    return redirect('/dashboard')

@app.route("/Skill/delete/<int:id>", methods = ['GET', 'POST'])
def delete2(id):
    if ('user' in session and session['user'] == params['UserName']):
        s = skills.query.filter_by(id=id).first()
        db.session.delete(s)
        db.session.commit()
    return redirect('/dashboard')

@app.route("/logout")
def logout():
    session.pop('user',None)
    return redirect('/dashboard')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)