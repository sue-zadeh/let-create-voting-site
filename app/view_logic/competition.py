"""
Handles some routes
"""
from flask import redirect, url_for, render_template, session, request, flash, jsonify
from .. import app
from .base_logic import user_role, VmsCursor, setup_session, cleanup_session,allowed_file, app,base_layout_params
from datetime import datetime, timedelta
import re
import os
from flask_hashing import Hashing
from werkzeug.utils import secure_filename


PASSWORD_SALT = '42##Z*f6EH1dQx~'
DEFAULT_USER_ROLE = 'voter'



@app.route("/competition/<int:competition_id>")
def competition(competition_id):
    session['competition_id'] = competition_id
    return redirect(url_for('current_event'))


def save_profile_photo(photo):
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], 'assets', filename)
        photo.save(photo_path)
        return filename
    return None  # Return None if no photo is uploaded or the file is invalid

# NOTE: COMMENTED OUT AS THERE IS DUPLICATION WITH "CREATE APPLICATION" FUNCTION
# Add this route definition to handle 'create_competition'
# @app.route('/create_competition', methods=['GET', 'POST'])
# def create_competition():
#     if request.method == 'POST':
#         # Handle form data here
#         competition_name = request.form.get('competition_name')
#         description = request.form.get('description')
#         # Add other logic here (e.g., save to the database)

#         flash('Competition created successfully!', 'success')
#         return redirect(url_for('home'))

#     return render_template('create_competition.html', **(base_layout_params()))
  
@app.route("/select_competition")
def no_competition():
    return render_template('no_competition.html', **base_layout_params(*user_role()))
  
@app.route('/competition_results')
def competition_results():
    return render_template('competition_results.html', **(base_layout_params(*user_role())))  

@app.route('/explore')
def explore():

    return render_template('explore.html', **(base_layout_params(*user_role())))  

