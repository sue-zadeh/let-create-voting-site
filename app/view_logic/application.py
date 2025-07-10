from flask import redirect, url_for, render_template, session, request, flash
from .. import app
from .base_logic import user_role, VmsCursor, setup_session, cleanup_session, base_layout_params
from datetime import datetime
import re
from flask_hashing import Hashing
from .base_logic import base_layout_params



@app.route('/application', methods=["GET", "POST"])
def view_delete_applications():
    '''This function is used to display the list of applications that have been submitted by the user themselves.'''
    role, site_role = user_role()
    application_by_user = session['user_id']
    if role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    cursor = VmsCursor ()
    if request.method == "GET":
        cursor.execute('''
            SELECT name, description, status, application_time, reason, application_id
            FROM applications
            WHERE application_by_user = %s AND visible = 1
            ORDER BY application_time DESC
        ''', (application_by_user,))
        application_list = cursor.fetchall()
        for application in application_list:
            if not application['reason']:
                application['reason'] = ""     # Show empty rather than "None"


        return render_template('application.html', **(base_layout_params(role, site_role)), application_list=application_list, application_by_user = session['user_id'])
    else:
        application_id = request.form['application_id']
        cursor.execute("SELECT name, status FROM applications WHERE application_id = %s;", (application_id,))
        result = cursor.fetchone()
        current_status = result['status']
        cursor.execute("UPDATE applications SET visible = 0 WHERE application_id = %s;", (application_id,))
        application_name = result['name']
        flash(f'Your application "{application_name}" has been hidden.', 'success')
        if current_status == "pending":
            cursor.execute("UPDATE applications SET status = 'cancelled' WHERE application_id = %s;", (application_id,))
        return redirect (url_for ("view_delete_applications"))



@app.route('/application/new', methods=["GET", "POST"])
def create_application():
    '''This function is used for users to create an application for a new competition.'''
    role, site_role = user_role()
    if role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    application_by_user = session['user_id']
    cursor = VmsCursor ()
    # get the user_id of the user who is creating the application
    application_by_user = session['user_id']
    if request.method == "GET":
        return render_template('create_application.html', **(base_layout_params(role, site_role)))
    # Following code is for POST method
    # Check whether user is site-wide banned
    cursor.execute("SELECT * FROM site_wide_bans WHERE user_id = %s", (application_by_user,))
    result = cursor.fetchall()
    if len(result) > 0:
        flash ("You cannot create an application as you have been banned across the site.", "warning")
        return render_template('create_application.html', **(base_layout_params(role, site_role)))   
    else:
        app_name = request.form['app_name'].strip()
        app_name = "NZ " + app_name.title() + " of the Year"
        app_description = request.form['app_description']

    # Check if app_name already exists in the database
        cursor.execute('''
            SELECT * FROM applications
            WHERE name = %s AND status = 'pending'
        ''', (app_name,))
        app_result = cursor.fetchall()
        cursor.execute('''SELECT * FROM competitions WHERE name = %s''', (app_name,))
        competition_result = cursor.fetchall()
        if len(competition_result) > 0 or len(app_result) > 0:
            # The app_name exists in the database
            flash("Application could not be submitted: a competition with this name already exists or is already pending.", "warning")
            return render_template('create_application.html', **(base_layout_params(role, site_role)))
        else:
            cursor.execute ("INSERT INTO applications (name, description, application_by_user) VALUES (%s, %s, %s);", (app_name, app_description, application_by_user))
            flash("Application submitted successfully!", "success") 
            return render_template('create_application.html', **(base_layout_params(role, site_role))) 



@app.route('/process_applications', methods=["GET", "POST"])
def process_applications():
    '''This function is used for site admins to display and process the applications that have been submitted by users.
    When an application is approved, a competition is created with the same name as the application.'''
    role, site_role = user_role()
    if site_role != 'site admin':        
        flash("You don't have access to this.", "warning")
        return redirect(url_for('home'))
    user_id = session['user_id']
    cursor = VmsCursor ()
    if request.method == "GET":
        cursor.execute('''
            SELECT users.username, users.user_id, name, applications.description, status, application_time, reason, application_id
            FROM applications
            LEFT JOIN users ON applications.application_by_user = users.user_id
            WHERE visible = 1 
            ORDER BY application_time ASC
        ''')
        application_list = cursor.fetchall()
        return render_template('process_applications.html', **(base_layout_params(role, site_role)), application_list=application_list, user_id=user_id)
    # Handling POST requests for approving or rejecting applications
    elif request.method == "POST":
        action = request.form.get('action')  # Get the action (approve or reject)
        application_id = request.form.get('application_id')  # Get the application ID
        # Approve application by deleting the application and creating a competition
        if action == 'approve':
            cursor.execute('SELECT * FROM applications WHERE application_id = %s', (application_id,))
            application = cursor.fetchone()
            if application:
                competition_name = application['name']
                cursor.execute('SELECT * FROM competitions WHERE name = %s', (competition_name,))
                competition = cursor.fetchone()
                if competition: # If the competition with this application name already exists
                    flash ("Application could not be approved: a competition with this name already exists.", "warning")
                    return redirect(url_for('process_applications'))
                cursor.execute('''UPDATE applications SET status = 'approved' WHERE application_id = %s''', (application_id,))
                cursor.execute('''INSERT INTO competitions (name, description) VALUES (%s, %s)''', (competition_name, application['description'],))
                cursor.execute('''INSERT INTO user_competition_roles (user_id, competition_id, role) VALUES (%s, LAST_INSERT_ID(), 'admin')''', (application['application_by_user'],))
                flash(f"Application approved successfully! A '{competition_name}' competition has been created.", "success")
            return redirect(url_for('process_applications'))

        # Reject application
        elif action == 'reject':
            reason = request.form.get('reason')  # Get rejection reason
            cursor.execute('UPDATE applications SET status = "rejected", reason = %s WHERE application_id = %s',
                           (reason, application_id))
            flash("Application rejected successfully!", "success")
            return redirect(url_for('process_applications'))
        
