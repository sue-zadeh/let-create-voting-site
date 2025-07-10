from flask import redirect, url_for, render_template, session, request, flash, jsonify

from app.app_logic.ban import ban_a_user, unban_a_user
from .. import app
from .base_logic import user_role, VmsCursor, base_layout_params,current_competition_id
from datetime import datetime





@app.route('/banned_competition', methods=["GET"])
def view_banned_competitions():
    '''This function is used to display all the banned competitions for the user, including the site-wide ban.'''
    role, site_role = user_role()
    user_id = session['user_id']
    if role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    cursor = VmsCursor()
    cursor.execute('''
    SELECT 
        bans.ban_id, 
        bans.competition_id, 
        bans.user_id, 
        bans.ban_date, 
        bans.reason, 
        competitions.name AS competition_name, 
        appeals.reason AS appeal_reason, 
        appeals.status AS appeal_status, 
        appeals.appeal_date AS appeal_date, 
        appeals.response AS appeal_response,
        appeals.response_date AS response_date
    FROM 
        bans 
    LEFT JOIN 
        competitions ON bans.competition_id = competitions.competition_id
    LEFT JOIN
        appeals ON bans.ban_id = appeals.ban_id AND bans.competition_id = appeals.competition_id
    WHERE
        bans.user_id = %s and bans.active;
        ''', (user_id,))

    banned_competitions = cursor.fetchall()

    cursor.execute('''
    SELECT 
        swb.site_wide_ban_id AS swb_ban_id,
        swb.reason AS swb_ban_reason, 
        swb.ban_date AS swb_ban_date, 
        swa.appeal_date AS swb_appeal_date,
        swa.status AS swb_appeal_status,
        swa.reason AS swb_appeal_reason,
        swa.response_date AS swb_response_date,
        swa.response AS swb_appeal_response
    FROM 
        site_wide_bans AS swb
    LEFT JOIN 
        site_wide_ban_appeals AS swa ON swb.site_wide_ban_id = swa.site_wide_ban_id 
    WHERE 
        swb.user_id = %s AND swb.active
    ''', (user_id, ))
    site_wide_ban_info = cursor.fetchone()
       
    return render_template('banned_competition.html', **(base_layout_params(role, site_role)), banned_competitions=banned_competitions, site_wide_ban_info=site_wide_ban_info)


@app.route('/banned_competition/appeal', methods=["POST"])
def appeal_bans():
    '''This function is used for banned users to submit an appeal for a competition ban.'''
    role, site_role = user_role()
    if role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    # Check - who will not need this functionality?
    cursor = VmsCursor()
    appeal_reason = request.form['appeal_reason']
    ban_id = request.form['ban_id']
    competition_id = request.form['competition_id']
    cursor.execute(''' 
    INSERT INTO appeals (reason, competition_id, ban_id) VALUES (%s, %s, %s) ''' , (appeal_reason, competition_id, ban_id))
    flash ("Your appeal has been submitted successfully.", "success")
    return redirect(url_for('view_banned_competitions'))

@app.route('/banned_competition/site_wide_ban_appeal', methods=["POST"])
def appeal_site_wide_ban():
    '''This function is used for banned users to submit an appeal for a site-wide ban.'''
    logged_in_role, logged_in_site_role = user_role()
    if logged_in_role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    cursor = VmsCursor()
    appeal_reason = request.form['swb_appeal_reason']
    site_wide_ban_id = request.form['swb_ban_id']
    cursor.execute(''' 
    INSERT INTO site_wide_ban_appeals (site_wide_ban_id, reason) VALUES (%s, %s) ''' , (site_wide_ban_id, appeal_reason,))
    flash ("Your sitewide ban appeal has been submitted successfully.", "success")
    return redirect(url_for('view_banned_competitions'))

@app.route("/appeal", methods=["GET", "POST"])
def check_appeals():
  role, site_role = user_role()
  cursor = VmsCursor()
  if role == 'guest' or (role == 'voter' and site_role != 'site admin'):
     flash("You have no access to this function.", "warning")
     return redirect(url_for('home'))
  else:
    if request.method == "GET":
      
      cursor.execute('''
      SELECT 
          bans.ban_id, 
          bans.competition_id, 
          bans.user_id, 
          bans.ban_date, 
          bans.reason, 
          competitions.name AS competition_name, 
          IFNULL(appeals.reason,'') AS appeal_reason,
          appeals.appeal_id AS appeal_id,
          IFNULL(appeals.status, '') AS appeal_status, 
          appeals.appeal_date AS appeal_date, 
          IFNULL(appeals.response, '') AS appeal_response,
          appeals.response_date AS response_date,
          users.username AS username
      FROM 
          bans 
      LEFT JOIN 
          competitions ON bans.competition_id = competitions.competition_id
      JOIN
          appeals ON bans.ban_id = appeals.ban_id AND bans.competition_id = appeals.competition_id
      LEFT JOIN
          users ON bans.user_id = users.user_id  
      WHERE bans.competition_id=%s AND bans.active
      ORDER BY appeals.appeal_date DESC;
          ''',(current_competition_id(),))
      appeals = cursor.fetchall()

      cursor.execute('''
      SELECT 
          sw_bans.site_wide_ban_id AS ban_id,
          sw_bans.user_id, 
          sw_bans.ban_date, 
          sw_bans.reason, 
          IFNULL(sw_appeals.reason,'') AS appeal_reason,
          sw_appeals.appeal_id AS appeal_id,
          IFNULL(sw_appeals.status, '') AS appeal_status, 
          sw_appeals.appeal_date AS appeal_date, 
          IFNULL(sw_appeals.response, '') AS appeal_response,
          sw_appeals.response_date AS response_date,
          users.username AS username
      FROM 
          site_wide_bans sw_bans
      JOIN
          site_wide_ban_appeals sw_appeals ON sw_bans.site_wide_ban_id = sw_appeals.site_wide_ban_id
      LEFT JOIN
          users ON sw_bans.user_id = users.user_id
      WHERE sw_bans.active
      ORDER BY sw_appeals.appeal_date DESC;
          ''')
      site_appeals = cursor.fetchall()
      
      return render_template('appeal.html', appeals=appeals, **(base_layout_params(role, site_role)), site_appeals=site_appeals)  
    
    else:
      if "appeal_id" in request.form and "deny_reason" in request.form:
        appeal_id = request.form['appeal_id']
        uphold_reason = request.form['deny_reason']
        
        cursor.execute("UPDATE appeals SET response = %s, status= 'denied', response_date = %s WHERE appeal_id=%s", (uphold_reason, datetime.now(), appeal_id))
        
        flash("User's appeal has been denied.", 'success')
        return redirect(url_for('check_appeals'))   
      
      elif "appeal_id" in request.form:
        appeal_id = request.form['appeal_id']
        cursor.execute('''UPDATE appeals 
                          JOIN bans on bans.ban_id = appeals.ban_id
                          SET appeals.status = 'approved', response_date = %s ,bans.active = 0 WHERE appeal_id = %s;
                       ''', (datetime.now(), appeal_id))
        
        flash("The appeal has been approved successfully.", 'success')
        return redirect(url_for('check_appeals'))    
    
@app.route("/approve_appeal", methods=['PUT'])
def approve_appeal():
    role, site_role = user_role()
    if site_role != 'site admin':
        return ''
    try:
        cursor = VmsCursor()
        cursor.execute("""UPDATE site_wide_ban_appeals AS appeals
                          JOIN site_wide_bans AS bans ON appeals.site_wide_ban_id = bans.site_wide_ban_id  
                            SET appeals.status = 'approved', appeals.response_date = %s, bans.active = 0
                            WHERE appeal_id = %s""",
                        (datetime.now(), int(request.json['id_data'])))
    except:
        flash("Approve user's appeal failed.", "danger")
    else:
        flash("User's appeal has been approved successfully.", 'success')
    return ''

@app.route("/deny_appeal", methods=['PUT'])
def deny_appeal():
    role, site_role = user_role()
    if site_role != 'site admin':
        return ''
    try:
        cursor = VmsCursor()
        cursor.execute("""UPDATE site_wide_ban_appeals
                    SET response = %s, status = 'denied', response_date = %s
                    WHERE appeal_id = %s""",
                        (request.json['reason'], datetime.now(), int(request.json['id_data'])))
    except:
        flash("Deny user's appeal failed.", "danger")
    else:
        flash("User's appeal has been denied.", 'success')
    return ''

@app.route("/ban_list", methods=['GET'])
def ban_list():
    logged_in_role, logged_in_site_role = user_role()  
    if logged_in_site_role == 'site admin':
        cursor = VmsCursor()
        cursor.execute('''
         SELECT 
            u.username AS username,
            u.user_id,
            COUNT(b.ban_id) AS total_bans
        FROM users u
        LEFT JOIN bans b ON b.user_id = u.user_id
        WHERE b.active
        GROUP BY u.user_id, u.username
        ORDER BY COUNT(b.ban_id) DESC;
        ''')
        ban_lists = cursor.fetchall()
        return render_template("ban_list.html", ban_lists=ban_lists, **(base_layout_params(logged_in_role, logged_in_site_role)))
    
    else:
        flash("You are not authorised to use this function.","warning")
        return redirect(url_for("home"))
        

@app.route("/site_wide_ban/<int:user_id>", methods=['POST'])
def site_wide_ban(user_id):
    logged_in_role, logged_in_site_role = user_role()
    if logged_in_site_role == 'site admin' and user_id != session['user_id']:
        cursor  = VmsCursor()
       
        if request.method == "POST":
            site_wide_ban_status = request.form.get('site_wide_ban_status')
            site_wide_ban_reason = request.form.get('reason_for_site_wide_ban')
            action = request.form.get('action')
            site_wide_ban_id = request.form.get('site_wide_ban_id')
            
            if site_wide_ban_reason and action == 'ban':
                
                cursor.execute("INSERT INTO site_wide_bans (user_id, ban_date, reason) VALUES(%s, NOW(),%s);",(user_id, site_wide_ban_reason))
                flash("User has been site wide banned.",'success')
                
            if action == "activate" and site_wide_ban_status == "Banned":

                cursor.execute("UPDATE site_wide_bans SET active = 0 WHERE site_wide_ban_id = %s and user_id = %s", (site_wide_ban_id,user_id))
                flash("User has been activated.", 'success')
            return redirect(url_for('ban_single_user', user_id=user_id))
            
        

        
    
    else:
        flash("You are not authorised to use this function.","warning")
        return redirect(url_for("home"))
    
    
    

    
    
    
    
    
    
    
        
    
    
    
    

def get_all_competitions():
    cursor = VmsCursor()
    query = "SELECT competition_id, name FROM competitions"
    cursor.execute(query)
    competitions = cursor.fetchall()
    return competitions



# Ban user POST route
@app.route('/ban_user', methods=['POST'])
def ban_user():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        competition_id = data.get('competition_id')
        ban_type = data.get('ban_type')
        reason = data.get('reason')  # Get the reason

        cursor = VmsCursor()

        if ban_type == 'competition':
            query = "INSERT INTO bans (user_id, competition_id, ban_date, reason) VALUES (%s, %s, NOW(), %s)"
            cursor.execute(query, (user_id, competition_id, reason))
        elif ban_type == 'site':
            query = "INSERT INTO site_wide_bans (user_id, ban_date, reason) VALUES (%s, NOW(), %s)"
            cursor.execute(query, (user_id, reason))

      # Return success
        return jsonify({"status": "success", "message": "User banned successfully!"}), 200  
    except Exception as e:
        print(f"Error: {str(e)}")
        # Return error if there's an exception
        return jsonify({"status": "error", "message": "Failed to ban user."}), 500  

@app.route("/ban_users/<int:user_id>", methods=["POST", "GET"])
def ban_single_user(user_id):
    logged_in_role, logged_in_site_role = user_role()
    if logged_in_role == "voter" and logged_in_site_role == 'voter':
        flash("You are not authorised to use this function.",'warning')
        return redirect("home")
    
    cursor = VmsCursor()
    if request.method == "GET":
        if logged_in_site_role == 'site admin':
            #Get all competition ban information for site admin
            cursor.execute('''
                SELECT ubs.*
                FROM user_ban_status ubs
                WHERE ubs.user_id = %s;             
                ''',(user_id,))
        else:
            #Get user ban status for competitions admin or scrutineer administers
            cursor.execute('''
                SELECT ubs.*
                FROM user_ban_status ubs
                LEFT JOIN user_competition_roles ucr ON ucr.competition_id = ubs.competition_id
                WHERE ubs.user_id = %s AND ucr.user_id = %s;             
                ''',(user_id,session['user_id']))             
        ban_lists = cursor.fetchall()
        
        # Get site wide ban status
        cursor.execute('''
        SELECT 
            swb.site_wide_ban_id AS site_wide_ban_id,
            u.user_id AS user_id,
            CASE
                WHEN swb.user_id IS NOT NULL AND swb.active = 1 THEN 'Banned'
                ELSE 'Active'
            END AS status,
            IFNULL(swb.reason,'N/A') AS reason,
            swb.ban_date AS ban_date
        FROM users u
        LEFT JOIN site_wide_bans swb ON u.user_id = swb.user_id
            AND swb.active
        WHERE u.user_id=%s;              
        ''', (user_id,))
        site_wide_ban = cursor.fetchone()

        cursor.execute('''
                        SELECT username
                        FROM users
                        WHERE user_id = %s;''', (user_id,))
        user=cursor.fetchone()
        username = None
        if user:
            username = user['username']
        else:
            flash("User not found", 'warning')
            return redirect(url_for('home'))
            
        return render_template("ban_single_user.html", ban_lists=ban_lists, **(base_layout_params(logged_in_role, logged_in_site_role)),site_wide_ban=site_wide_ban, username=username)
    else:
        competition_id = None
        ban_status = None
        reason_for_ban = None
        if "competition_id" in request.form:
            competition_id = request.form['competition_id']
            ban_status = request.form['ban_status']
            reason_for_ban = request.form.get('reason_for_ban')
        elif logged_in_site_role == 'site admin' and 'site_admin_competition_id' in request.form:
            competition_id = request.form['site_admin_competition_id']
            ban_status = request.form['site_admin_ban_status']
            reason_for_ban = request.form.get('site_admin_reason_for_ban')

        if competition_id is not None:
            if ban_status == "Banned":            
                message, message_type = unban_a_user(user_id, competition_id)
            else:
                message, message_type = ban_a_user(user_id, competition_id, reason_for_ban)
            flash(message, message_type)
            
        
        return redirect(url_for("ban_single_user", user_id=user_id))
            
