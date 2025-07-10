"""
Handles event routes
"""
from flask import redirect, url_for, session, request, send_from_directory, render_template, flash

from app.app_logic.ban import ban_users_at_ip_address
from .. import app
from .base_logic import random_filename, user_role, VmsCursor, ip_vertified, allowed_file, base_layout_params, current_competition_id
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from datetime import timedelta



@app.template_filter()
def event_status(event):
    """Returns the status of the given event db record"""
    today = datetime.today().date()
    if today > event['end_date']:
        # Past event
        if event['status'] == 'finalised':
            # Finalised event
            return 'finalised'
        else:
            # Still needs scrutineering
            return 'closed'
    elif today >= event['start_date']:
        # Current event
        return 'active'
    else:
        # Future event
        return 'future'

@app.route("/events", methods=["POST", "GET"])
def event_board():
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin': # Scrutineers shouldn't have access to this
        return redirect(url_for('home'))

    cursor = VmsCursor()
    cursor.execute("SELECT event_id, name, description, start_date, end_date, status from events"
                   " WHERE CURDATE() < start_date AND competition_id = %s"
                   " ORDER BY start_date ASC;", (current_competition_id(),))
    events = cursor.fetchall()

    return render_template("event_board.html", **(base_layout_params(role, site_role)), events=events)





@app.route('/event/current_event')
def current_event():
    role, site_role = user_role()
    cursor = VmsCursor()
    cursor.execute("""
    SELECT event_id
    FROM events 
    WHERE CURDATE() >= start_date AND status != 'finalised'
    AND competition_id = %s
    """, (current_competition_id(),))
    current_event_id = None  
    current_event_result = cursor.fetchone()
    if current_event_result is None:
        return render_template("event.html", **(base_layout_params(role, site_role)),
                        competitors=None,
                        selected_event=None)
    
    current_event_id = current_event_result['event_id']

    return redirect(url_for('event', event_id=current_event_id))

@app.route('/delete_event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return '', 400

    cursor = VmsCursor()
    try:
        # Delete votes
        cursor.execute("DELETE FROM votes WHERE event_id = %s", (event_id,))
        # Delete competitors
        cursor.execute("DELETE FROM competitors WHERE event_id = %s", (event_id,))
        # Delete event
        cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
    except Exception as E:
        flash('Could not remove event', 'danger')
    else:
        flash('Event removed', 'success')
        
    return ''

@app.route('/save_event/<int:event_id>', methods=['PUT'])
def save_event(event_id=0):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return '', 400
    # Get form data
    event_name, event_description = '', ''
    try:
        if event_id == 0:
            event_name = request.form['name'].strip()
            event_description = request.form['description'].strip()

            if event_name == '':
                return 'Please enter a event name', 400

        start_date_input = request.form['start_date']
        end_date_input = request.form['end_date']
    except:
        return 'Failed to save due to missing parameters', 400

    
    if start_date_input == '':
        return 'Please enter a start date', 400
    elif end_date_input == '':
        return 'Please enter an end date', 400
    
    try:
        start_date = datetime.fromisoformat(start_date_input).date()
        end_date = datetime.fromisoformat(end_date_input).date()
    except Exception as e:
        return 'Please enter a valid date', 400
    
    if start_date <= datetime.today().date():
        return 'Start date must be in the future', 400
    elif end_date < start_date:
        return 'The end date cannot be earlier than the start date', 400
    
    if event_id == 0:
        cursor = VmsCursor()
        cursor.execute("INSERT INTO events (competition_id, name, description, start_date, end_date, is_visible, status)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (current_competition_id(), event_name, event_description, start_date, end_date, True, 'active'))
        return '', 200
    else:
        cursor = VmsCursor()
        cursor.execute("UPDATE events SET start_date = %s, end_date = %s WHERE event_id = %s AND competition_id = %s", (start_date, end_date, event_id, current_competition_id()))
        return '', 200
    

@app.route('/event/<int:event_id>', methods=["POST", "GET"])
def event(event_id):
    role, site_role = user_role()
    cursor = VmsCursor()
    
    if request.method == "POST" :
        if role == 'guest':
            return redirect(url_for('login'))
        if role != 'voter':
            return redirect(url_for('event',event_id=event_id))
        user_id = session["user_id"]
        competitor_id = request.form['competitor_id']
        user_ip_address = request.remote_addr
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if the user has been site banned
        cursor.execute("""SELECT b.*
                       FROM site_wide_bans b
                       WHERE b.user_id = %s AND b.active;""", (user_id,))
        banned_user = cursor.fetchone()
        if banned_user is not None:
            flash("Voting unsuccessful. You have been banned from voting in all competitions!", "warning")
            return redirect(url_for('event',event_id=event_id))

        # Check if the user has been banned
        cursor.execute("""SELECT b.*
                       FROM bans b
                       WHERE b.user_id = %s AND b.competition_id = %s AND b.active;
                       """, (user_id, current_competition_id()))
        banned_user = cursor.fetchone()
        if banned_user is not None:
            flash("Voting unsuccessful. You have been banned from voting in this competition!", "warning")
            return redirect(url_for('event',event_id=event_id))
        
        # Check if the user has already voted in this event
        cursor.execute("SELECT * FROM votes WHERE user_id = %s AND event_id = %s;",(user_id, event_id))              
        existing_vote = cursor.fetchone()
        if existing_vote is not None:
            flash("You have already voted in this event.", "warning")
            return redirect(url_for('event',event_id=event_id))


        else:
            cursor.execute("INSERT INTO votes (user_id, event_id, competitor_id, vote_time, ip_address) VALUES (%s, %s, %s, %s, %s);",(user_id, event_id, competitor_id, current_time, user_ip_address))
            flash("You have voted successfully!", "success")
            return redirect(url_for('event',event_id=event_id))
    else:
        cursor.execute("""
        SELECT * FROM events
        WHERE event_id = %s
        AND competition_id = %s
        """, (event_id, current_competition_id()))
        selected_event = cursor.fetchone()   
        if selected_event:
            if event_status(selected_event) == 'future' and role != 'admin' and site_role != 'site admin':
                return redirect(url_for('home'))  # Non-admins do not have access to future events

            if selected_event['status'] == 'finalised':
                if role == 'guest':
                    return redirect(url_for('home'))
                cursor = VmsCursor()
                # find the finalised event
                cursor.execute("""
                SELECT competitors.name, competitors.image, COUNT(votes.user_id) AS voteNum
                FROM competitors
                LEFT OUTER JOIN votes
                ON competitors.competitor_id = votes.competitor_id AND NOT votes.invalid
                WHERE competitors.event_id = %s
                GROUP BY competitors.competitor_id
                ORDER BY voteNum DESC
                """, (event_id,))
                finalised_event = cursor.fetchall()
                # culculate the percentage of votes
                total_votes = 0
                for competitor in finalised_event:
                    total_votes += competitor['voteNum']
                for competitor in finalised_event:
                    competitor['percentage'] = round(competitor['voteNum'] / total_votes * 100, 2)
                return render_template('event.html', **(base_layout_params(role, site_role)), selected_event = selected_event, finalised_events=finalised_event)
            
            cursor.execute("SELECT competitor_id, name, description, image"
                        " FROM competitors"
                        " WHERE event_id = %s", (event_id,))
            competitors = cursor.fetchall()

            voted_for = None
            if role == 'voter':
                cursor.execute("SELECT competitor_id"
                            " FROM votes"
                            " WHERE user_id = %s AND event_id = %s AND NOT votes.invalid",
                            (session['user_id'], event_id))
                voted_for = cursor.fetchone()

            daily_votes = []
            if role == "admin" or role == "scrutineer":
                # get the daliy votes
                cursor.execute("""
                            select count(user_id) as voteNum, DATE(vote_time) as voteDate
                            from votes
                                where event_id = %s AND NOT invalid
                                group by DATE(vote_time)
                                order by voteDate desc
                            """, (event_id,))
                daily_votes = cursor.fetchall()
            
            site_wide_banned_user = None
            banned_user = None
            if role == "voter":
                #Check if user has been site wide banned or not
                cursor.execute("""SELECT b.*
                        FROM site_wide_bans b
                        WHERE b.user_id = %s AND b.active;""", (session['user_id'],))
                site_wide_banned_user = cursor.fetchone()
                #Check if user has been banned for a competition
                cursor.execute("""SELECT b.*
                        FROM bans b
                        WHERE b.user_id = %s AND b.competition_id = %s AND b.active;
                        """, (session['user_id'], current_competition_id()))
                banned_user = cursor.fetchone()
            
            
            # Query to fetch recent voters within the last 24 hours for the selected competition's active events
            cursor.execute("""
                SELECT users.profile_image, users.username, users.description, votes.vote_time
                FROM votes
                LEFT JOIN users ON votes.user_id = users.user_id
                LEFT JOIN events ON votes.event_id = events.event_id
                WHERE events.event_id = %s AND events.status = 'active' 
                AND votes.vote_time > NOW() - INTERVAL 1 DAY
                AND NOT votes.invalid
                AND users.is_active
                ORDER BY votes.vote_time DESC
                LIMIT 5
            """, (event_id,))
            
            recent_voters = cursor.fetchall()

            return render_template("event.html", **(base_layout_params(role, site_role)),
                                competitors = competitors, selected_event=selected_event,
                                edit_event = event_status(selected_event) == 'future',
                                voted_for=voted_for['competitor_id'] if voted_for is not None else None,
                                daily_votes=daily_votes,
                                daily_votes_sorted_count=sorted(daily_votes, key = lambda x: x['voteNum'], reverse=True),
                                recent_voters=recent_voters,banned_user=banned_user, site_wide_banned_user=site_wide_banned_user)


        # If no event was found, render with no event available
        return render_template("event.html", **(base_layout_params(role, site_role)),
                            competitors=None,
                            selected_event=None)

@app.route('/competitor/<int:competitor_id>', methods=['DELETE'])
def delete_competitor(competitor_id):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return '', 400  # Return a 400 http error

    cursor = VmsCursor()    
    try:
        # Delete competitor
        cursor.execute("DELETE FROM competitors WHERE competitor_id = %s", (competitor_id,))
    except Exception as E:
        flash('Could not remove competitor', 'danger')
    else:
        flash('Competitor removed', 'success')

    return ''

@app.route('/competitor/<int:competitor_id>', methods=['PUT'])
def save_competitor(competitor_id):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return '', 400  # Return a 400 http error
    
    if 'competitor_name' in request.form and 'competitor_description' in request.form and 'event_id' in request.form:
        competitor_name = request.form['competitor_name'].strip()
        competitor_description = request.form['competitor_description'].strip()
        event_id = request.form['event_id']

        cursor = VmsCursor()
        # Check if competitor name is blank
        if competitor_name == '':
            return 'Competitor name is required', 400
        # Check if competitor name is unique for that event
        cursor.execute("SELECT * FROM competitors WHERE name = %s AND event_id = %s AND competitor_id != %s", (competitor_name, event_id, competitor_id))
        if cursor.fetchone():
            return 'Competitor name already exists', 400  # Return a 400 http error

        file = None
        filename = None
        file_ok = False
        if 'competitor_image' in request.files:
            file = request.files['competitor_image']
            if file and allowed_file(file.filename):
                try:
                    # Name the new file using correct extension
                    file1, file_ext = os.path.splitext(file.filename)
                    filename = random_filename() + file_ext
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'competitor_images', filename))
                    file_ok = True
                except FileNotFoundError as E:
                    flash('Save failed', "danger")
                    print("Error: Could not save file")
                    return 'Could not save image', 400  # Return a 400 http error
            else:
                return 'Image file or file type problem', 400

        if competitor_id == 0:
            if file_ok:
                event_id = request.form['event_id']
                
                try:
                    # Insert new competitor
                    cursor.execute("INSERT INTO competitors (name, image, description, event_id)"
                                    " VALUES (%s, %s, %s, %s)", (competitor_name, filename, competitor_description, event_id))
                except Exception as E:
                    flash('Save failed', "danger")
                else:
                    flash('Save successful', "success")
            else:
                return 'Image is required', 400
        else:
            existing_filename = None
            try:
                # Get the existing filename
                cursor.execute('SELECT image FROM competitors WHERE competitor_id = %s', (competitor_id, ))
                competitor = cursor.fetchone()
                if competitor and competitor['image'].strip() != '':
                    existing_filename = competitor['image']

                # Update existing competitor
                cursor.execute("UPDATE competitors SET name = %s, image = %s, description = %s WHERE competitor_id = %s", (competitor_name, filename, competitor_description, competitor_id))
            except Exception as E:
                flash('Save failed', 'danger')
            else:
                flash('Save successful', 'success')
                try:
                    # Delete the old image file
                    if existing_filename != None:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'competitor_images', existing_filename))
                except Exception as E:
                    flash('A save error occurred. Please let the site admin know', 'danger')
    else:
        flash('Save failed', 'danger')
        return '', 400

    return ''


@app.route("/addEvent", methods = ['POST'])
def add_event():
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return redirect(url_for('home'))
    
    # get input information
    name = request.form['name'] if 'name' in request.form else''
    description = request.form['description'] if 'description' in request.form else''
    start_date = request.form['start_date'] if 'start_date' in request.form else''
    end_date = request.form['end_date'] if 'end_date' in request.form else''
    is_visible = True
    status = "active"

    cursor = VmsCursor()
    cursor.execute("INSERT INTO events (name, description, start_date, end_date, is_visible, status)"
    " VALUES (%s, %s, %s, %s, %s, %s)",
    (name, description, start_date, end_date, is_visible, status))

    return redirect(url_for('get_events'))

def get_current_event():
    cursor = VmsCursor()
    cursor.execute("""
    SELECT event_id, name, start_date, end_date, status
    FROM events 
    WHERE CURDATE() >= start_date AND status != 'finalised'
        AND competition_id = %s
    """, (current_competition_id(),))
    current_event = cursor.fetchone()
    return {'event_id': current_event['event_id'] if current_event else None,
            'event_status': event_status(current_event) if current_event else None,
            'name': current_event['name'] if current_event else None}

@app.route("/scrutineer/votes", methods = ['GET'])
def view_votes():
    role, site_role = user_role()
    if role != 'scrutineer' and site_role != 'site admin':
        return redirect(url_for('home'))
    view_setting = 'single' if 'view_setting' not in request.args else request.args['view_setting']
    cursor = VmsCursor()
    current_event = get_current_event()
    event_id = current_event['event_id']
    if event_id is None:
        return render_template('event.html', **(base_layout_params(role, site_role)))

    status = current_event['event_status']

    votes = None
    if view_setting == 'single':
        cursor.execute("SELECT DISTINCT ip_address FROM votes WHERE event_id = %s", (event_id,))
        ip_dropdown_list = cursor.fetchall()   # Use SELECT DISTINCT to avoid retrieving duplicated IP addresses

        competitor_name = request.args.get('competitor_name')
        ip_address = request.args.get('ip_address')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        where_clause = ""
        params = [event_id, ]
        if competitor_name is not None and len(competitor_name.strip()) > 0:
            where_clause += "AND c.name like %s "
            params.append(f"%{competitor_name}%")

        if ip_address is not None and len(ip_address.strip()) > 0:
            where_clause += "AND ip_address = %s "
            params.append(ip_address.strip())
        if start_date is not None and len(start_date.strip()) > 0 and end_date is not None and len(end_date.strip()) > 0:
            # Convert input strings to datetime objects
            dt_start_date = datetime.strptime(start_date, '%Y-%m-%d')
            dt_end_date = datetime.strptime(end_date, '%Y-%m-%d')
            if dt_end_date < dt_start_date:
                flash( 'End date cannot be earlier than start date.', 'danger')
            where_clause += "AND DATE(vote_time) BETWEEN %s AND %s "    
            # Search based on dates only, regardless of the time. 
            # This is so that if specify start_date as 2024-08-15 and end_date as 2024-08-15, records that have a time later in the day would also be included.
            start_date_formatted = dt_start_date.strftime('%Y-%m-%d')
            end_date_formatted = dt_end_date.strftime('%Y-%m-%d')
            params.append(f"{start_date_formatted}")
            params.append(f"{end_date_formatted}")

        query = f"""SELECT username, vote_time, ip_address, c.name AS competitor_name, v.invalid, IFNULL(b.active, 0) AS banned
            FROM votes v 
            JOIN users u 
            ON u.user_id = v.user_id 
            JOIN competitors c 
            ON c.competitor_id = v.competitor_id 
            JOIN events e ON c.event_id = e.event_id
            LEFT OUTER JOIN bans b ON u.user_id = b.user_id AND e.competition_id = b.competition_id AND b.active
            WHERE v.event_id = %s {where_clause}
            ORDER BY v.vote_time DESC""" 
        cursor.execute(query, tuple(params))
        votes = cursor.fetchall()

        for vote in votes:
            if vote['ip_address'] not in ip_vertified:
                ip_vertified[vote['ip_address']] = True
        
        return render_template('votes.html', **(base_layout_params(role, site_role)),
                           votes=votes, 
                           event_id=event_id,
                           event_name=current_event['name'], 
                           event_status=status,
                           start_date=start_date, end_date=end_date, competitor_name=competitor_name, ip_address=ip_address,
                           ip_vertified=ip_vertified, ip_dropdown_list = ip_dropdown_list,
                           current_view_setting=view_setting)
    else:
        cursor.execute("""SELECT votes.*, u.username, CONCAT(u.first_name, ' ', u.last_name) AS full_name, c.name AS competitor_name, IFNULL(b.active, 0) AS banned
                        FROM
                            (SELECT ip_address, event_id, count(*) AS num_votes
                            FROM votes
                            WHERE event_id=%s
                            GROUP BY ip_address
                            HAVING count(*) > 1
                            ORDER BY count(*) DESC, ip_address ASC) multiple_voters 
                        JOIN votes ON votes.ip_address = multiple_voters.ip_address 
                            AND votes.event_id = multiple_voters.event_id
                        JOIN users u ON votes.user_id = u.user_id
                        JOIN competitors c ON votes.competitor_id = c.competitor_id
                        JOIN events e ON c.event_id = e.event_id
                        LEFT OUTER JOIN bans b ON u.user_id = b.user_id AND e.competition_id = b.competition_id AND b.active 
                        ORDER BY multiple_voters.num_votes DESC, votes.ip_address ASC
                       ;
                       """, (event_id,))
        votes = cursor.fetchall()

        ip_addresses = []
        idx = -1
        current_address = None
        for vote in votes:
            if vote['ip_address'] != current_address:
                current_address = vote['ip_address']
                ip_addresses.append({'address': current_address, 'numValid': 0, 'numInvalid': 0, 'votes': [], 'banUsers?': False})
                idx += 1
            ip_addresses[idx]['votes'].append(vote)
            if vote['invalid']:
                ip_addresses[idx]['numInvalid'] += 1
            else:
                ip_addresses[idx]['numValid'] += 1
            if not vote['banned']:
                ip_addresses[idx]['banUsers?'] = True

            


        return render_template('votes.html', **(base_layout_params(role, site_role)),
                           ip_addresses=ip_addresses, 
                           event_id=event_id,
                           event_name=current_event['name'], 
                           event_status=status,
                           ip_vertified=ip_vertified,
                           current_view_setting=view_setting)

    


@app.route("/scrutineer/finalise_event", methods = ['POST'])
def finalise_event():
    role, site_role = user_role()
    if role != 'scrutineer' and site_role != 'site admin':
        return redirect(url_for('home'))
    
    event_id = request.form['event_id']
    cursor = VmsCursor()
    cursor.execute("SELECT start_date, end_date, status FROM events WHERE event_id = %s AND competition_id = %s;", (event_id, current_competition_id()))
    event = cursor.fetchone()
    if event_status(event) == 'closed':
        cursor.execute("UPDATE events SET status = 'finalised' WHERE event_id = %s AND competition_id = %s;", (event_id, current_competition_id()))
        return redirect(url_for('finished_event'))
    
    
@app.route("/invalid_url", methods = ['PUT'])
def invalid_url():
    role, site_role = user_role()
    if role != 'scrutineer' and site_role != 'site admin':
        return ""
    ip_address = request.json['id_data']
    print(ip_address)
    ip_vertified[ip_address] = False
    # update the database to record the ip address
    cursor = VmsCursor()
    cursor.execute("UPDATE votes SET invalid=1 WHERE ip_address = %s AND event_id = %s;", (ip_address, get_current_event()['event_id']))
    return ""

@app.route("/ban_users_at_ip", methods = ['PUT'])
def ban_users_at_ip():
    role, site_role = user_role()
    if role != 'scrutineer' and site_role != 'site admin':
        return ""
    ip_address = request.json['id_data']
    message, message_type = ban_users_at_ip_address(ip_address, get_current_event()['event_id'], request.json['reason'])
    flash(message, message_type)
    return ""

@app.route("/previous_events", methods = ['GET'])
def finished_event():
    cursor = VmsCursor()

    cursor.execute("SELECT COUNT(v.user_id) AS vote_count, v.competitor_id, v.event_id"
                   " FROM votes v"
                   " JOIN events c ON v.event_id = c.event_id"
                   " WHERE c.status = 'finalised'"
                   " AND c.competition_id = %s"
                   " AND NOT v.invalid"
                   " GROUP BY v.event_id, v.competitor_id"
                   " ORDER BY c.end_date DESC;", (current_competition_id(),))
    competitor_votes = cursor.fetchall()

    vote_count_dic = {}

    for competitor_vote in competitor_votes:
        event_id = competitor_vote['event_id']
        competitor_id = competitor_vote['competitor_id']
        vote_count = competitor_vote['vote_count']

        if event_id not in vote_count_dic:
            vote_count_dic[event_id] = {"total_votes": 0, "winner_id": 0, "winner_votes": 0}

        event = vote_count_dic[event_id]
        event["total_votes"] += vote_count
        if vote_count > event["winner_votes"]:
            event["winner_votes"] = vote_count
            event["winner_id"] = competitor_id

    for event_id in vote_count_dic.keys():
        event = vote_count_dic[event_id]
        event["winner_vote_percentage"] = round((event["winner_votes"] / event["total_votes"]) * 100, 2)


        cursor.execute("SELECT w.name, w.description, w.image, c.name AS event_name"
                       " FROM competitors w"
                       " JOIN events c ON w.event_id = c.event_id"
                       " WHERE w.competitor_id = %s;", (event["winner_id"],))
        winner_info = cursor.fetchone()
        event["winner_info"] = winner_info

    return render_template(
        "finished_event.html", **(base_layout_params(*(user_role()))),
        events=vote_count_dic
    )

@app.route('/event/<int:event_id>', methods=["GET"])
def previous_event_winner(event_id):
    role, site_role = user_role()
    cursor = VmsCursor()
    cursor.execute("SELECT * FROM events WHERE event_id = %s;", (event_id,))
    selected_event = cursor.fetchone()   

    if selected_event and selected_event['status'] == 'finalised':
        cursor.execute("SELECT COUNT(user_id) AS total_vote_count FROM votes WHERE event_id = %s AND NOT votes.invalid;", (event_id,))
        vote_dic = cursor.fetchone()
        total_vote_count = vote_dic['total_vote_count']

        cursor.execute("SELECT COUNT(user_id) AS vote_count, competitor_id FROM votes WHERE event_id = %s AND NOT votes.invalid GROUP BY competitor_id;", (event_id,))
        competitor_votes = cursor.fetchall()

        vote_count_dic = {}
        largest_vote = 0 
        winner_id = None

        for competitor_vote in competitor_votes:
            competitor_id = competitor_vote['competitor_id']
            vote_count = competitor_vote['vote_count']
            vote_count_dic[competitor_id] = vote_count

            if vote_count > largest_vote:
                largest_vote = vote_count
                winner_id = competitor_id

        if winner_id:
            winner_vote_percentage = (largest_vote / total_vote_count) * 100
            winner_vote_percentage = round(winner_vote_percentage, 2)

            cursor.execute("SELECT * FROM competitors WHERE competitor_id = %s;", (winner_id,))
            winner_info = cursor.fetchone()

            return render_template(
                "event.html", **(base_layout_params(role, site_role)), 
                winner_id=winner_id, 
                winner_vote_percentage=winner_vote_percentage, 
                total_vote_count=total_vote_count, 
                winner_info=winner_info,
                event_id=event_id,
                selected_event=selected_event,
            )
        else:
            flash("No winner could be determined.", "warning")
            return redirect(url_for('event_board'))

    flash("Event not found or not finalized.", "warning")
    return redirect(url_for('event_board'))




        
