"""
Handles profile routes
"""
from flask import redirect, url_for, session, request, send_from_directory, flash, render_template
from .. import PASSWORD_SALT, app
from .base_logic import allowed_file, random_competition, random_filename, user_role, VmsCursor, base_layout_params, current_competition_id, base_layout_params
import os
from werkzeug.utils import secure_filename
from flask_hashing import Hashing
import random



hashing = Hashing(app)

QUERY_USER_ROLES = """SELECT u.user_id, c.competition_id, c.name AS competition_name, IFNULL(ucr.role,'voter') AS role, IF(ISNULL(ucm.user_id), 'No', 'Yes') AS is_moderator
                    FROM users u 
                    CROSS JOIN competitions c 
                    LEFT JOIN user_competition_roles ucr ON u.user_id = ucr.user_id 
                        AND c.competition_id = ucr.competition_id 
                    LEFT JOIN user_competition_moderators ucm ON u.user_id = ucm.user_id
                        AND c.competition_id = ucm.competition_id
                    WHERE u.user_id=%s
                    ORDER BY c.name ASC;"""

QUERY_MY_COMP_USER_ROLES = """SELECT ucr.user_id, my_comps.competition_id, comp.name AS competition_name, IF(my_comps.role='scrutineer', 'hidden', IFNULL(ucr.role,'voter')) AS role, IF(ISNULL(ucm.user_id), 'No', 'Yes') AS is_moderator
                            FROM users comp_admin
                            JOIN user_competition_roles my_comps ON comp_admin.user_id = my_comps.user_id AND (my_comps.role='admin' OR my_comps.role='scrutineer')
                            LEFT OUTER JOIN user_competition_roles ucr ON my_comps.competition_id = ucr.competition_id AND ucr.user_id = %s
                            LEFT OUTER JOIN user_competition_moderators ucm ON my_comps.competition_id = ucm.competition_id AND ucm.user_id = %s
                            LEFT OUTER JOIN competitions comp ON my_comps.competition_id = comp.competition_id
                            WHERE comp_admin.user_id=%s
                            ORDER BY comp.name ASC;"""

@app.route('/profile/<int:user_id>')
def profile(user_id):
    logged_in_role, logged_in_site_role = user_role()
    if logged_in_role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    else:
        cursor = VmsCursor()
        
        query = "SELECT u.*, IFNULL(r.role, 'voter') AS role FROM users u LEFT OUTER JOIN user_competition_roles r ON r.competition_id = %s AND u.user_id = r.user_id WHERE u.user_id=%s"
        if user_id == session['user_id'] or logged_in_site_role == 'site admin' or have_admin_privileges():
           # Viewing own profile or # Site admin can view any profile or # Those with admin privileges (incl. scrutineer) can view any profile
           cursor.execute(query, (current_competition_id(), user_id))
        elif logged_in_role == 'voter':
           return redirect(url_for('home'))
        
        user = cursor.fetchone()
        if user:
            username = user['username']
            email = user['email']
            firstname = user['first_name']
            lastname = user['last_name']
            location = user['location']
            description = user['description']
            profileimage = user['profile_image']
            status = user['is_active']   
            site_role = user['site_role']
            role = user['role']

            # To get user role in each competition
            if logged_in_site_role == 'site admin':
                cursor.execute(QUERY_USER_ROLES,(user_id,))
            elif session['user_id'] == user_id:
                # Get all roles when viewing own profile
                cursor.execute(QUERY_USER_ROLES, (user_id,))
            # To get user role in admin's competitions
            else:
                cursor.execute(QUERY_MY_COMP_USER_ROLES, (user_id, user_id, session['user_id']))
        
            #Create all_competitions to distinguish itself from **(base_layout_params()) as it is for site admin
            all_competitions = cursor.fetchall()
            
            ban_list = []
            if user_id == session['user_id'] or logged_in_site_role == 'site admin':
                # Get bans for user viewing own profile or site admin viewing profile
                cursor.execute('''
                    SELECT *
                    FROM user_ban_status ubs 
                    WHERE ubs.user_id=%s AND ubs.banned;
                    ''', (user_id,))
                ban_list = cursor.fetchall()
            elif logged_in_role == 'admin' or logged_in_role == 'scrutineer':
                #Get user ban status for competitions admin or scrutineer administers
                cursor.execute('''
                    SELECT ubs.*
                    FROM user_ban_status ubs
                    LEFT JOIN user_competition_roles ucr ON ucr.competition_id = ubs.competition_id
                    WHERE ubs.user_id = %s AND ucr.user_id = %s AND ubs.banned;             
                    ''',(user_id,session['user_id']))   
                ban_list = cursor.fetchall()
            
            vote_histories = None
            if logged_in_site_role == 'site admin':
                #Get user vote histories
                cursor.execute('''
                SELECT
                    v.user_id,
                    e.name AS event_name,
                    c.name AS competitor_name,
                    v.vote_time AS vote_time,
                    v.ip_address AS ip_address
                FROM events e
                LEFT JOIN competitors c ON e.event_id = c.event_id
                LEFT JOIN votes v ON v.competitor_id = c.competitor_id AND NOT v.invalid
                WHERE v.user_id = %s
                ORDER BY v.vote_time DESC;
                ''',(user_id,))
                vote_histories = cursor.fetchall()

            #Check if user has been site banned or not
            cursor.execute("SELECT user_id FROM site_wide_bans WHERE user_id=%s AND active = 1;",(user_id,))
            site_wide_ban_user = cursor.fetchone()
            #Check if user is the moderator or not
            cursor.execute("SELECT user_id FROM user_competition_moderators WHERE user_id=%s AND competition_id=%s;",(user_id, current_competition_id()))
            moderator_user = cursor.fetchone()
            
            return render_template("profile.html", logged_in = True if 'logged_in' in session else False,
                                username=username, email=email, firstname=firstname, lastname=lastname, location=location,
                                description=description, profileimage=profileimage, status=status,user_id=user_id,
                                logged_in_id=session["user_id"], site_role = site_role, role=role, all_competitions=all_competitions,
                                ban_list=ban_list, vote_histories=vote_histories, site_wide_ban_user=site_wide_ban_user,
                                **(base_layout_params(logged_in_role, logged_in_site_role)), moderator_user=moderator_user,
                                have_admin_privileges=have_admin_privileges())
        else:
           flash("Profile not found", 'warning')
           return redirect(url_for('home'))
        
        
@app.route("/profile_list", methods=['POST', 'GET'])
def profile_list():
    role, site_role = user_role()
    current_user_id = session['user_id']

    # Pick a competition at random if no current competition
    if current_competition_id() == 0:
        session['competition_id'] = random_competition()
    # if logged_in_role != 'admin' and logged_in_role != 'scrutineer' and logged_in_site_role != 'site admin':
    #     flash('You have no authority to access this function.','warning')
    #     return redirect(url_for('home'))

    query = "SELECT u.*, IFNULL(r.role, 'voter') AS role FROM users u" \
            " LEFT OUTER JOIN user_competition_roles r ON r.competition_id = %s AND u.user_id = r.user_id"
    params = []
    params.append(current_competition_id())

    # Build up a SQL WHERE query
    query_where = ''
    def add_query_condition(condition):
        nonlocal query_where
        if query_where == '':
            query_where = ' WHERE ' + condition
        else:
            query_where += ' AND ' + condition

    has_admin_privileges = have_admin_privileges() or site_role == 'site admin'
    if not has_admin_privileges:
        add_query_condition("u.publicly_visible")    

    username, firstname, lastname, email = '', '', '', ''
    if request.method == "POST":
        username = request.form['username'].lower()
        firstname = request.form['firstname'].capitalize()
        lastname = request.form['lastname'].capitalize()
        email = request.form['email']

        if username:
            add_query_condition("username LIKE %s")
            params.append("%" + username + "%")
        if firstname:
            add_query_condition("first_name LIKE %s")
            params.append("%" + firstname + "%")
            if not has_admin_privileges:
                add_query_condition("first_name_visible")
        if lastname:
            add_query_condition("last_name LIKE %s")
            params.append("%" + lastname + "%")
            if not has_admin_privileges:
                add_query_condition("last_name_visible")
        if email:
            add_query_condition("email LIKE %s")
            params.append("%" + email + "%")
            if not has_admin_privileges:
                add_query_condition("email_visible")
        
    cursor = VmsCursor()
    cursor.execute(query + query_where, tuple(params))
    users = cursor.fetchall()
    for user in users:
        #TODO: Change this to be in query
        user['profile_image'] = user['profile_image']if user['profile_image'] is not None and user['profile_image'] != '' else 'default.jpg'
        #get recent message
        cursor.execute("""SELECT posts.content
                       FROM (SELECT content, created_at
                       FROM messages
                       WHERE user_id=%s
                       UNION
                       SELECT content, created_at
                       FROM replies
                       WHERE user_id = %s) AS posts
                       ORDER BY posts.created_at DESC
                       LIMIT 2""",(user['user_id'],user['user_id']))
        messages = cursor.fetchall()
        user['message'] = ' ... '.join([message['content'] for message in messages])
        # get user recent participate competition
        cursor.execute('''SELECT c.name
                    FROM votes
                    JOIN events e ON votes.event_id = e.event_id
                    JOIN competitions c ON e.competition_id = c.competition_id
                    WHERE votes.user_id = %s
                    AND votes.vote_time > NOW() - INTERVAL 1 DAY
                    AND NOT votes.invalid
                    ORDER BY votes.vote_time DESC
                    LIMIT 3
            ''', (user['user_id'],))
        recent_votes = cursor.fetchall()
        names = ', '.join([vote['name'] for vote in recent_votes])
        user['competition'] = names
        # process the not visible field
        has_admin_privileges = have_admin_privileges()
        if not (has_admin_privileges or site_role == 'site admin'):
            HIDDEN_FIELD_TEXT = '*****'
            if not user['email_visible']:
                user['email'] = HIDDEN_FIELD_TEXT
            if not user['location_visible']:
                user['location'] = HIDDEN_FIELD_TEXT
            if not user['first_name_visible']:
                user['first_name'] = HIDDEN_FIELD_TEXT
            if not user['last_name_visible']:
                user['last_name'] = HIDDEN_FIELD_TEXT
        user['all_name'] = user['first_name'] + ' ' + user['last_name']
    if users is None or len(users) == 0:
        flash("No data found, please try again.",'warning')
    

    return render_template("profile_list.html", user_list_url = url_for('profile_list'), users=users, have_admin_privileges=has_admin_privileges,
            username=username, firstname=firstname, lastname=lastname, email=email, **(base_layout_params(role, site_role)))
    
@app.route("/profile/update/<int:user_id>", methods=['GET', 'POST'])    
def profile_update(user_id):
    role, site_role = user_role()
    if role != 'guest' and user_id == session['user_id']:
        if request.method == 'GET':
        
            cursor = VmsCursor()
            cursor.execute("SELECT * FROM users WHERE user_id=%s",(user_id,))
            user = cursor.fetchone()
            
            username = user['username']
            username_visible = user['username_visible']
            email = user['email']
            email_visible = user['email_visible']
            firstname = user['first_name']
            first_name_visible = user['first_name_visible']
            lastname = user['last_name']
            last_name_visible = user['last_name_visible']
            location = user['location']
            location_visible = user['location_visible']
            description = user['description']
            description_visible = user['description_visible']
            profileimage = user['profile_image']
            status = user['is_active']  
            publicly_visible = user['publicly_visible']
        
            return render_template("update_profile.html", **(base_layout_params(role, site_role)), publicly_visible=publicly_visible,
                         username=username, email=email, firstname=firstname, lastname=lastname, location=location, description=description, profileimage=profileimage, status=status,user_id=user_id,
                         username_visible=username_visible, email_visible=email_visible, first_name_visible=first_name_visible, last_name_visible=last_name_visible, description_visible=description_visible, location_visible=location_visible)
        
                    
        else:
            print(request.form)
            email = request.form['email']
            email_visible = 1 if 'email_visible' in request.form and request.form['email_visible'] else 0
            firstname = request.form['firstname'].capitalize()
            firstname_visible = 1 if 'first_name_visible' in request.form and request.form['first_name_visible'] else 0
            lastname = request.form['lastname'].capitalize()
            lastname_visible = 1 if 'last_name_visible' in request.form and request.form['last_name_visible'] else 0
            description = request.form['description']
            description_visible = 1 if 'description_visible' in request.form and request.form['description_visible'] else 0
            location = request.form['location'].capitalize()
            location_visible = 1 if 'location_visible' in request.form and request.form['location_visible'] else 0
            visible = 1 if 'publicly_visible' in request.form and request.form['publicly_visible'] else 0
            
            #check if email already exist in the system
            cursor = VmsCursor()
            cursor.execute("SELECT email FROM users WHERE user_id != %s;", (user_id,))
            check_emails = cursor.fetchall()
            current_emails = [item['email'] for item in check_emails]
            
            if email in current_emails:
                flash("Could not update email as it already exists in the system","warning")
                return render_template("update_profile.html", **(base_layout_params(role, site_role)), username=session['username'], firstname=session['firstname'],lastname=session['lastname'], email=session['email'], description=session['description'], location=session['location'], profileimage=session['profileimage'],
                                       #status=session['is_active'],
                                       user_id=user_id)
            print("firstname_visible",firstname_visible, "lastname_visible", lastname_visible)
            cursor.execute("UPDATE users SET first_name=%s, last_name=%s, description=%s, email=%s, location=%s, publicly_visible=%s, email_visible=%s, first_name_visible=%s, last_name_visible=%s, description_visible=%s, location_visible=%s WHERE user_id=%s;",
                            (firstname, lastname, description, email, location, visible, email_visible, firstname_visible, lastname_visible, description_visible, location_visible, user_id))
            
            session['firstname'] = firstname
            session['lastname'] = lastname
            session['description'] = description
            session['email'] = email
            session['location'] = location
            session['publicly_visible'] = visible
            
            flash("User Information has been updated successfully!","success")
            return redirect(url_for('profile', user_id=user_id))
    elif role != 'guest':
        flash("Cannot update another's profile", "warning")
        return redirect(url_for('home'))
    else:
        flash("Please log in","warning")
        return redirect(url_for('login'))
    
@app.route("/profile/update_password",methods=['GET', 'POST'])
def profile_update_password():
    role, site_role = user_role()
    if role != 'guest':    
        if request.method == "POST" and 'password' in request.form and 'newpassword' in request.form and 'confirmnewpassword' in request.form:
            password = request.form['password']
            newpassword = request.form['newpassword']
            confirmnewpassword = request.form['confirmnewpassword']
            hash_password = hashing.hash_value(password, PASSWORD_SALT)
            hash_newpassword = hashing.hash_value(newpassword, PASSWORD_SALT)
            hash_confirmnewpassword = hashing.hash_value(confirmnewpassword, PASSWORD_SALT)
            
            
            if hash_password != session['password']:
                flash("Incorrect current password, please try again","warning")
                return redirect(url_for('profile_update_password'))
            elif hash_password == hash_newpassword:
                flash("New password must be different from current pasword, please try again","warning")
                return redirect(url_for('profile_update_password'))
            elif hash_newpassword != hash_confirmnewpassword:
                flash("new password doesn't match, please try again","warning")
                return redirect(url_for('profile_update_password'))
            
            
            cursor = VmsCursor()
            cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s;", (hash_newpassword, session['user_id']))
            flash("Your password has been updated.","success")
            session['password'] = hash_newpassword
            return redirect(url_for('profile',user_id=session['user_id']))
        elif request.method == "POST":
            flash('Please fill out this form completely.','warning')
            return redirect(url_for('profile_update_password'))
        else:
            return render_template('update_password.html', **(base_layout_params(role, site_role)))
             
    else:
        return render_template('login.html', **(base_layout_params(role, site_role)))
    
    
    
@app.route('/profile/upload_profile_image', methods=["POST"])    
def upload_profile_image():
    logged_in_role = user_role
    if logged_in_role != "guest":
        if request.method == "POST" and 'profile_image' in request.files:
            file = request.files['profile_image']
            if file.filename == '':
                flash("No selected file", "warning")
                return redirect(url_for('profile',user_id=session['user_id']))
            
            cursor = VmsCursor()

            filename = None
            if allowed_file(file.filename):
                try:
                    # Name the new file using correct extension
                    file1, file_ext = os.path.splitext(file.filename)
                    filename = random_filename() + file_ext
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'user_images', filename))
                except FileNotFoundError as E:
                    flash('Could not upload image', "danger")
                    return redirect(url_for('profile',user_id=session['user_id']))
            else:
                flash('Image file type not allowed. Please use a png, jpg or jpeg', 'danger')
                return redirect(url_for('profile',user_id=session['user_id']))

            existing_filename = None
            try:
                # Get the existing filename
                cursor.execute('SELECT profile_image FROM users WHERE user_id = %s', (session['user_id'], ))
                user = cursor.fetchone()
                if user and user['profile_image'].strip() != '':
                    existing_filename = user['profile_image']
                cursor.execute("UPDATE users SET profile_image = %s WHERE user_id = %s;",(filename, session['user_id']))
            except Exception as E:
                flash('Save failed', 'danger')
            else:
                flash("Profile image updated successfully", "success")
                session['profileimage'] = filename
                
                try:
                    # Delete the old image file
                    if existing_filename != None:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'user_images', existing_filename))
                except Exception as E:
                    flash('A save error occurred. Please let the site admin know', 'danger')

                return redirect(url_for('profile',user_id=session['user_id']))
        else:
            flash("No file found", "warning")
            return redirect(url_for('profile_update',user_id=session['user_id']))
    
    else:
        return redirect(url_for('login'))

@app.route('/profile/delete_profile_image', methods=["POST"])    
def delete_profile_image():
    logged_in_role = user_role
    if logged_in_role != "guest":
        if request.method == "POST":
            cursor = VmsCursor()
            cursor.execute("SELECT profile_image FROM users WHERE user_id = %s;", (session['user_id'],))
            result = cursor.fetchone()
            
            if result and result['profile_image']:
                filename = result['profile_image']
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'user_images', filename)
                
                # Check if the file exists on the server
                if os.path.exists(file_path):
                    # cannot remove because might be used by someone else. os.remove(file_path)  # Remove the file from the server
                    
                    # Update the database to remove the image reference
                    cursor.execute("UPDATE users SET profile_image = '' WHERE user_id = %s;", (session['user_id'],))
                    flash("Profile image removed successfully", "success")
                    
                    # Update session variable
                    
                    session['profileimage'] = ''
                    return redirect(url_for('profile_update',user_id=session['user_id']))
                    
                else:
                    flash("Profile image not found on the server.", "warning")
                    return redirect(url_for('profile_update',user_id=session['user_id']))
            else:
                flash("No profile image to delete.", "warning")
                return redirect(url_for('profile_update',user_id=session['user_id']))
        else:
            flash("No file found", "warning")
            return redirect(url_for('profile_update',user_id=session['user_id']))
    
    else:
        return redirect(url_for('login')) 
    
def have_admin_privileges():
    cursor = VmsCursor()
    cursor.execute('''
                   SELECT ucr.user_id
                   FROM user_competition_roles ucr WHERE ucr.user_id = %s
                   ;''', (session['user_id'],))
    if cursor.fetchone():
        return True
    return False

@app.route("/profile/management/update/<int:user_id>", methods=["POST", "GET"])
def profile_role_status_update(user_id):
    role, site_role = user_role()
    if role == 'guest':
        flash("You are not authorised.",'warning')
        return redirect(url_for('home'))
    
    logged_in_id = session['user_id']
    
    if have_admin_privileges() or site_role == 'site admin':
        if request.method == "GET":
            cursor = VmsCursor()
            cursor.execute("SELECT u.*, IFNULL(r.role, 'voter') AS role FROM users u LEFT OUTER JOIN user_competition_roles r ON r.competition_id = %s AND u.user_id = r.user_id WHERE u.user_id=%s;",
                            (current_competition_id(), user_id))
            user = cursor.fetchone()
            
            if site_role == 'site admin':
                cursor.execute(QUERY_USER_ROLES,(user_id,))
            else:
                cursor.execute(QUERY_MY_COMP_USER_ROLES, (user_id, user_id, session['user_id']))
            
            all_competitions = cursor.fetchall() 
            
            return render_template("update_role_status.html", **(base_layout_params(role, site_role)), user=user, logged_in_id=logged_in_id,
                                   user_id=user_id, all_competitions=all_competitions, have_admin_privileges=have_admin_privileges())
        
        else:
            cursor = VmsCursor()

            if site_role == 'site admin' and user_id != logged_in_id:
                if 'status' in request.form:
                    status = request.form['status']
                    cursor.execute("UPDATE users SET is_active=%s WHERE user_id=%s;",(status, user_id))

                if 'user_site_role' in request.form:
                    user_site_role = request.form['user_site_role']
                    cursor.execute("UPDATE users SET site_role=%s WHERE user_id=%s;",(user_site_role, user_id))

            #Site admin can change roles for any competition                
            if 'roles_for_site_admin[]' in request.form and user_id != logged_in_id:
                roles_for_site_admin = request.form.getlist('roles_for_site_admin[]')
                single_competition_ids = request.form.getlist('single_competition_ids[]')
                for competition_id, users_role in zip(single_competition_ids, roles_for_site_admin):
                    if site_role != 'site admin':
                        # If I'm not site admin then ensure I am admin for the competition being updated, otherwise move on to next record
                        cursor.execute('SELECT r.user_id FROM user_competition_roles r WHERE r.competition_id = %s AND r.user_id = %s AND r.role = "admin";', (competition_id, logged_in_id))
                        if not cursor.fetchone():
                            continue

                    cursor.execute("SELECT r.user_id FROM user_competition_roles r WHERE r.competition_id = %s AND r.user_id = %s", (competition_id, user_id))
                    if cursor.fetchone():
                        # There is an admin or scrutineer record in the database
                        if users_role == 'voter':
                            cursor.execute("DELETE FROM user_competition_roles WHERE competition_id = %s AND user_id = %s", (competition_id, user_id))
                        else:
                            cursor.execute("UPDATE user_competition_roles SET role = %s WHERE competition_id = %s AND user_id = %s", (users_role, competition_id, user_id))  
                    else:
                        # No record
                        if users_role != 'voter':
                            # insert an admin or scrutineer record
                            cursor.execute("INSERT INTO user_competition_roles (user_id, competition_id, role) VALUES (%s, %s, %s)", (user_id, competition_id, users_role))
            
            #promote and demote moderator
            if 'moderators[]' in request.form:
                single_competition_ids = request.form.getlist('single_competition_ids[]')
                moderators = request.form.getlist('moderators[]')
                for competition_id, moderator in zip(single_competition_ids,moderators):
                    # Ensure I am admin or scrutineer for the competition being updated, otherwise move on to next record
                    cursor.execute('SELECT r.user_id FROM user_competition_roles r WHERE r.competition_id = %s AND r.user_id = %s;', (competition_id, logged_in_id))
                    if not cursor.fetchone():
                        continue
                    if moderator == "Yes":
                        cursor.execute("SELECT * FROM user_competition_moderators WHERE user_id=%s AND competition_id=%s;",(user_id, competition_id))
                        existing_moderator = cursor.fetchone()
                        if existing_moderator is None:
                            cursor.execute("INSERT IGNORE INTO user_competition_moderators (user_id, competition_id) VALUES(%s, %s);",(user_id, competition_id))
                            
                    else:
                        cursor.execute("DELETE FROM user_competition_moderators WHERE user_id=%s AND competition_id=%s;", (user_id, competition_id))

            flash("Information has been updated successfully!","success")

            return redirect(url_for('profile', user_id=user_id))          
    else:
        flash("You are not authorised.",'warning')
        return redirect(url_for('home'))
    

@app.route("/moderator_management/<int:user_id>", methods=["POST"])
def moderator_management(user_id):

    logged_in_role, logged_in_site_role = user_role()

    cursor = VmsCursor()
    if logged_in_role == 'admin' or logged_in_role == 'scrutineer':
        if request.method == "POST" and 'promote_user_id' in request.form:
            promote_user_id = request.form['promote_user_id']
           
            cursor.execute("INSERT INTO user_competition_moderators (user_id, competition_id) VALUES(%s, %s);",(promote_user_id,current_competition_id()))
            flash("User has been promoted to be a moderator.",'success')
            return redirect(url_for('profile', user_id=promote_user_id))
        elif request.method == "POST" and 'demote_user_id' in request.form:
            demote_user_id = request.form['demote_user_id']
            cursor.execute("DELETE FROM user_competition_moderators WHERE user_id=%s AND competition_id=%s;",(demote_user_id,current_competition_id()))
            flash("User has been demoted from a moderator.",'warning')
            return redirect(url_for('profile', user_id=demote_user_id))
    
    else:
        flash("You are not authorised to use function.", 'warning')
        return redirect(url_for("profile", user_id=user_id))
    
