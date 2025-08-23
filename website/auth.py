from flask import Blueprint , render_template , request, flash , redirect , url_for
from .models import User ,db ,Note
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import login_user , login_required , logout_user , current_user

auth=Blueprint('auth',__name__,template_folder='templates_folder')

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        
        if user :
            if check_password_hash(user.password,password):
                flash('logged in succesfully..',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            
            else:
                flash('incorrect password try again..',category='error')
        else:
            flash('this email not in the system try to sign-up',category='error')
        
    return render_template("login.html",user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        fullname=request.form.get("fullname")
        email=request.form.get("email")
        phone=request.form.get("phone")
        password=request.form.get("password")
        password2=request.form.get("password2")
        
        user=User.query.filter_by(email=email).first()
        
        if user:
            flash('user already exist..',category='error')
            
        elif len(email) < 4 or '@gmail.com' not in email:
            flash('email must be greater than 4 letters and have @gmail.com in it..',category='error')
            
        elif password != password2:
            flash('the passwords do not match..',category='error')
            
        elif len(fullname) <=10:
            flash('must have at least 11 letter..',category='error')
            
        elif len(password)<6 or password.isalpha():
            flash('the password must contain numbers and at least 7 letters..',category='error')
            
        else:
            new_user=User(fullname=fullname,email=email,password=generate_password_hash(password,method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            
            flash('Account created!',category='success')
            
            return redirect(url_for('views.home'))
    
    return render_template("signup.html",user=current_user)


@auth.route('/delete_note/<int:note_id>' ,methods=['POST'])
def delete_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash('you cannot delete this note..',category='error')
        return redirect(url_for('views.home'))
    db.session.delete(note)
    db.session.commit()
    flash('note deleted succesfully' , category='success')
    return redirect(url_for('views.home'))
        

@auth.route('/update_note/<int:note_id>' ,methods=['POST'])
def update_note(note_id):
    note=Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash('cannot update this note',category='error')
        return redirect(url_for('views.home'))
    
    new_data=request.form.get("note")
    if new_data:
        note.data=new_data
        db.session.commit()
        flash('note updatd succesfully..',category='success')
    return redirect(url_for('views.home'))