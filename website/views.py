# to make the routes 
from flask import Blueprint ,render_template ,request, flash
from flask_login import  login_required , current_user
from .models import Note ,db

views=Blueprint('views',__name__,template_folder='templates_folder')

@views.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note)<1:
            flash('note is too small..',category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            
            flash('note added succesfully..',category='success')
        
    return render_template('home.html',user=current_user)
    
