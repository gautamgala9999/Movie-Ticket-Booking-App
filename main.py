from datetime import datetime
from flask import Flask,  render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required, login_user, logout_user, LoginManager, UserMixin
import pytz

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///ticket.db'
app.secret_key = 'ticket_booking_website'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore


class Show(db.Model):# type: ignore
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    rating = db.Column(db.String(25))
    tag = db.Column(db.String(75))
    datetime = db.Column(db.String(75), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)

class Venue(db.Model): # type: ignore
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

class User(UserMixin, db.Model):# type: ignore
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
 
class Ticket(db.Model):# type: ignore
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    date_purchased = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Kolkata')))

tshows=Show.query.all()
tvenues=Venue.query.all()
tall=tshows+(tvenues)
print(tall)
    
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET', 'POST'])
def home():
    tshows=Show.query.all()
    tvenues=Venue.query.all()
    tall=tshows+(tvenues)
    print(tall)
    return render_template('home.html',user=current_user ,tall=tall) # type: ignore

@app.route('/login/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email=='admin@domain.com' and password=='admin@123':
            return render_template('admin_login.html',user=current_user ,tall=tall)
    return render_template('admin.html',user=current_user ,tall=tall)

@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if ( user.password== password): # type: ignore
                
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                return 'Incorrect password, try again!'
        else:
            print('User does not exist.')
    return render_template("login.html", user=current_user ,tall=tall)

    # return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    print('You have logged out.')
    return redirect(url_for('login'))

    # return render_template('logout.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # user = User.query.filter_by(email=email).first()
        # if user:
        #     print('Email is already taken, try another email.')
        if len(name) < 3: # type: ignore
            print('Full name must be greater than 2 characters.')
        elif len(email) < 6: # type: ignore
            print('Email must be greater than 5 characters.')
        elif len(password1) < 7: # type: ignore
            print('Password must be at least 7 characters.')
        elif password1 != password2:
            print('Passwords don\'t match.')
        else:

            # Add user to the database
            new_user = User(name=name, email=email, password=password1) # type: ignore
            db.session.add(new_user)
            db.session.commit()
            print('Successfully signed up.')

    # return render_template("home.html", user=current_user ,tall=tall)
    return render_template('signup.html')

@app.route('/create_shows', methods=['GET', 'POST'])
# @login_required
def create_shows():
    # current_user_id=current_user.id # type: ignore
    venues=Venue.query.all()
    if True:
        if request.method == 'POST':
            name=request.form.get('name')
            description=request.form.get('description')
            rating=request.form.get('rating')
            tag=request.form.get('tag')
            datetime=request.form.get('datetime')
            venue_id=request.form.get('venue_id')
            new_show = Show(name=name, description=description, rating=rating, tag=tag,datetime=datetime,venue_id=venue_id) #venue_id foreign key 
            db.session.add(new_show)
            db.session.commit()
            return redirect(url_for('show_shows'))
        return render_template('create_shows.html',venues=venues,user=current_user ,tall=tall)
    else:
        return render_template('error.html')

@app.route('/show_shows', methods=['GET', 'POST'])
def show_shows():
    
    shows=Show.query.all()
    return render_template('show_shows.html',shows=shows,user=current_user ,tall=tall)

@app.route('/update_shows/<int:show_id>', methods=['GET', 'POST'])
# @login_required
def update_shows(show_id):
    # current_user_id=current_user.id # type: ignore
    if True:
        this_show=Show.query.get(show_id)
        venues=Venue.query.all()
        if request.method == 'POST':
            name=request.form.get('name')
            description=request.form.get('description')
            rating=request.form.get('rating')
            tag=request.form.get('tag')
            datetime=request.form.get('datetime')

            this_show.name=name
            this_show.description=description
            this_show.rating=rating
            this_show.tag=tag
            this_show.datetime=datetime
            
            db.session.commit()
            print('Show updated successfully')
            return redirect(url_for('show_shows'))
        return render_template('update_shows.html',show=this_show,venues=venues,user=current_user ,tall=tall)
    else:
        return render_template('error.html')

@app.route('/delete_shows/<int:show_id>', methods=['GET', 'POST'])
# @login_required
def delete_shows(show_id):
    # current_user_id=current_user.id # type: ignore
    if True:
        this_show=Show.query.get(show_id)
        db.session.delete(this_show)
        db.session.commit()
        print('Show deleted successfully')
        return redirect(url_for('show_shows',user=current_user ,tall=tall))
    else:
        return render_template('error.html')
    # return render_template('delete_shows.html')

@app.route('/create_venue', methods=['GET', 'POST'])
# @login_required
def create_venue():
    # current_user_id=current_user.id # type: ignore
    if True:
        if request.method == 'POST':
            name=request.form.get('name')
            location=request.form.get('location')
            capacity=request.form.get('capacity')

            new_venue=Venue(name=name, location=location, capacity=capacity)
            db.session.add(new_venue)
            db.session.commit()
            return redirect(url_for('show_venue',user=current_user ,tall=tall))
        return render_template('create_venue.html',user=current_user ,tall=tall)
    else:
        return render_template('error.html')

@app.route('/show_venue', methods=['GET', 'POST'])
def show_venue():
    venues=Venue.query.all()
    return render_template('show_venue.html',venues=venues,user=current_user ,tall=tall)

@app.route('/update_venue/<int:venue_id>', methods=['GET', 'POST'])
def update_venue(venue_id):
    # current_user_id=current_user.id # type: ignore
    if True:
        this_venue=Venue.query.get(venue_id)
        if request.method == 'POST':
            name=request.form.get('name')
            location=request.form.get('location')
            capacity=request.form.get('capacity')

            this_venue.name=name
            this_venue.location=location
            this_venue.capacity=capacity
            
            db.session.commit()
            print('Venue updated successfully')
            return redirect(url_for('show_venue',user=current_user ,tall=tall))
        
        return render_template('update_venue.html',venue=this_venue,user=current_user ,tall=tall)
    else:
        return render_template('error.html')

@app.route('/delete_venue/<int:venue_id>', methods=['GET', 'POST'])
# @login_required
def delete_venue(venue_id):
    # current_user_id=current_user.id # type: ignore
    if True:
        this_venue=Venue.query.get(venue_id)
        db.session.delete(this_venue)
        db.session.commit()
        print('Venue deleted successfully')
        return redirect(url_for('show_venue',user=current_user ,tall=tall))
        # return render_template('delete_venue.html')
    else:
        return render_template('error.html')

@app.route('/book_tickets/<show_id>', methods=['GET', 'POST'])
def book_tickets(show_id):
    
    show = Show.query.get(show_id)
    venue_id=show.venue_id
    thisvenue=Venue.query.get(venue_id)
    try:
        if True:
            if request.method == 'POST':
                show_id=show_id
                tickets = (request.form.get('tickets')) # type: ignore
                user_id = current_user.id # type: ignore 
            
                tickets=(int(tickets)) # type: ignore
                show = Show.query.get(show_id)
                if not show:
                    return "Invalid show ID"
                if tickets > (thisvenue.capacity):
                    print("Not enough tickets available")
                    return redirect(url_for('profile',user=current_user ,tall=tall))
                thisvenue.capacity-=tickets
                list_tickets = []
                for i in range(tickets): # type: ignore
                    ticket = Ticket(show_id=show_id, user_id=user_id)
                    list_tickets.append(ticket)
                    db.session.add(ticket)
                db.session.commit()  
                # print(list_tickets)          
                return redirect(url_for('profile',user=current_user ,tall=tall))
            return render_template('book_tickets.html',show=show,user=current_user ,tall=tall)
    except:
         return render_template('login.html',user=current_user ,tall=tall)
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        this_user_id=current_user.id # type: ignore
        num_tickets=Ticket.query.filter(Ticket.user_id==this_user_id).all()
        num_tickets=reversed(num_tickets)
        # print(num_tickets)
        # print(current_user) # type: ignore
        # print(current_user) # type: ignore
        return render_template('profile.html',user=current_user ,tall=tall,num_tickets=num_tickets)
        # return 'profile'
    except:
        return render_template('login.html')
    



if __name__=='__main__':
    
    
    db.create_all()
    app.run(debug=True, port = 8000)