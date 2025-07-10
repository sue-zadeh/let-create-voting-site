"""
Handles some routes
"""
from flask import redirect, url_for, render_template, session, request, flash
from .. import app, hashing, PASSWORD_SALT


from .base_logic import user_role, VmsCursor, setup_session, cleanup_session, base_layout_params

from datetime import datetime
import re

DEFAULT_USER_ROLE = 'voter'
DEFAULT_PROFILE_IMAGE = 'default.jpg'
DEFAULT_SITE_ROLE = "voter"

@app.route("/")
def home():
    role, site_role = user_role()

    # CAS-117, when user goes to home page, the current event navbar links should disappear
    #   because the user should pick a competition first on the home page before looking at any
    #   competition
    session['competition_id'] = 0

    if role != 'guest':
        # Check if 'username' exists in the session before accessing it
        return render_template(
            "home.html", **(base_layout_params(role, site_role)),
            logged_in_username=session['username'], user_id=session['user_id'])
    else:
        return render_template("home.html", **(base_layout_params(role, site_role)))
# @app.route('/')
# def home():
    
#     role = user_role()
#     cursor = VmsCursor()
    
#     # Fetch the current event
#     cursor.execute("""
#     SELECT event_id
#     FROM events 
#     WHERE YEAR(start_date) = YEAR(CURDATE()) 
#     AND status = 'active'
#     ORDER BY start_date DESC LIMIT 1
#     """)
#     current_event = cursor.fetchone()
#     event_id = current_event['event_id'] if current_event else None
    
#     # Fetch past and future events
#     cursor.execute("""
#     SELECT * FROM events
#     WHERE YEAR(start_date) = YEAR(CURDATE())
#     AND event_id != %s
#     ORDER BY start_date
#     """, (event_id,))
#     other_events = cursor.fetchall()

#     return render_template("home.html", **(base_layout_params()),
#                            event_id=event_id,
#                            other_events=other_events,
#                            logged_in_id = session['user_id'] if 'logged_in' in session else 0,
#                            logged_in_role = role,
#                            username=session['username'] if 'logged_in' in session else 0)


@app.route('/change_competition', methods=['PUT'])
def change_competition():
    session['competition_id'] = int(request.json['competition_id'])
    return ''

@app.route('/register', methods=['GET', 'POST'])
def register():
    role, site_role = user_role()
    if role != 'guest':
        return redirect(url_for('home'))
    # Output message if something goes wrong or successfully registered...
    msg=''

    if request.method == 'POST':
            print(request.form)
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            confirm_password = request.form['confirm_password'] 
            firstname = request.form['first_name']
            lastname = request.form['last_name']
            location = request.form['location']
            publicly_visible = request.form['visible'] if 'visible' in request.form else 0
            username_visible = request.form['username_visible'] if 'username_visible' in request.form else 0
            email_visible = request.form['email_visible'] if 'email_visible' in request.form else 0
            location_visible = request.form['location_visible'] if 'location_visible' in request.form else 0
            first_name_visible = request.form['first_name_visible'] if 'first_name_visible' in request.form else 0
            last_name_visible = request.form['last_name_visible'] if 'last_name_visible' in request.form else 0
            

            if not username or not password or not email:
                msg = 'Please fill out the form!'
                return render_template('register.html', **(base_layout_params(role, site_role)), msg=msg)
            if confirm_password!= password:
                msg = 'Passwords must match!'
            else:
                # Check if username or email exists
                cursor = VmsCursor()
                cursor.execute('SELECT username, email FROM users WHERE username = %s OR email = %s', (username, email))
                account = cursor.fetchone()

                # If account exists, show error and validation checks
                if account:
                    if account['username'] == username:
                        msg += 'Username already exists! '
                    if account['email'] == email:
                        msg += 'Email already exists! '
                else:
                    # Account doesn't exist and the form data is valid, now insert new account into accounts table
                    password_hash = hashing.hash_value(password, PASSWORD_SALT)
                    cursor.execute('INSERT INTO users (username, password_hash, email, first_name, last_name, location, profile_image, site_role, publicly_visible, username_visible, email_visible, location_visible, first_name_visible, last_name_visible) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)', (username, password_hash, email, firstname, lastname, location, DEFAULT_PROFILE_IMAGE, DEFAULT_SITE_ROLE, publicly_visible, username_visible, email_visible, location_visible, first_name_visible, last_name_visible))
                    msg = 'You have successfully registered!'
                    # If something went wrong, return the form with the user's previous input and error message
                    return render_template('register.html', **(base_layout_params(role, site_role)), msg=msg)  # Clear the form after successful registration
                # If there's an error, re-render the form with existing input
                return render_template('register.html', **(base_layout_params(role, site_role)), msg=msg, username=username, email=email, first_name=firstname, last_name=lastname, location=location)

    # Show registration form with message (if any)
    return render_template('register.html', **(base_layout_params(role, site_role)), msg=msg)

@app.route("/login", methods = ["POST", "GET"])
def login():
    role, site_role = user_role()
    if role != 'guest':
        return redirect(url_for('home'))
    #get the form data
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
       
    
        # if not username or not password:
        #     flash("Please fill out the form.","warning")
        #     return redirect(url_for('login'))
        
        cursor = VmsCursor()
        cursor.execute("SELECT * FROM users WHERE username = %s;",(username,))
        user = cursor.fetchone()
        if user is not None:
            password_hash = user['password_hash']
            if hashing.check_value(password_hash, password, PASSWORD_SALT):
                setup_session(user['user_id'],user['username'])
                session['firstname'] = user['first_name']
                session['lastname'] = user['last_name']
                session['description'] = user['description']
                session['location'] = user['location']
                session['profileimage'] = user['profile_image']
                session['email'] = user['email']
                session['password'] = user['password_hash']


                if user['is_active'] == 1:
                    return redirect(url_for("home"))
                else:
                    flash("Sorry, your account is inactive.", "warning")
                    return redirect(url_for("login"))

                
            else:
                flash("Incorrect password. Please try again.", "warning")
                return redirect(url_for("login")) 
        else:
            flash("Sorry, username doesn't exist, please try again or register.", "warning")
            return redirect(url_for("login"))
    else:

        return render_template('login.html', **(base_layout_params(role, site_role)))

    
@app.route("/logout")
def logout():
    cleanup_session()
    return redirect(url_for('home'))


