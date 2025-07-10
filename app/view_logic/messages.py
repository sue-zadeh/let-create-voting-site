"""
Handles messages routes, e.g. listing messages and replies, posting new messages/replies, deleting messages/replies
"""
from flask import flash, redirect, url_for, render_template, session, request
from .. import app
from .base_logic import current_competition_id, user_role, VmsCursor, base_layout_params
from datetime import datetime

@app.route("/message_board")
def message_list():
    role, site_role = user_role()
    if role == 'guest':
        return redirect(url_for('login'))
    elif current_competition_id() == 0:
        return redirect(url_for("no_competition"))
    
    validation={"message_title": ["", ""], "message_content": ["", ""], "reply_content": ["", ""]}
    message={"title": '', "content": ''}
    
    cursor = VmsCursor()
    
    cursor.execute(
        "SELECT m.message_id AS msg_id, m.user_id AS msg_user_id, msg_u.username AS msg_username, m.title AS msg_title, m.content AS msg_content, m.created_at AS msg_created_at,"
        "   r.reply_id, r.user_id AS reply_user_id, reply_u.username AS reply_username, r.content AS reply_content, r.created_at AS reply_created_at"
        " FROM messages m"
        " LEFT OUTER JOIN replies r ON m.message_id = r.message_id"
        " LEFT OUTER JOIN users msg_u ON m.user_id = msg_u.user_id"
        " LEFT OUTER JOIN users reply_u ON r.user_id = reply_u.user_id"
        " WHERE m.competition_id = %s"
        " ORDER BY m.created_at DESC, r.created_at ASC;",
        (current_competition_id(),)
    )

    messages = []
    for record in cursor.fetchall():
        if len(messages) == 0 or messages[len(messages)-1]['id'] != record['msg_id']:
            messages.append({'id': record['msg_id'], 'user_id': record['msg_user_id'],
                             'username': record['msg_username'], 'title': record['msg_title'],
                             'content': record['msg_content'], 'created_at': record['msg_created_at'], 'replies': []})
        if record['reply_id'] is not None:
            messages[len(messages)-1]['replies'].append({'id': record['reply_id'], 'user_id': record['reply_user_id'],
                                                  'username': record['reply_username'], 'content': record['reply_content'],
                                                  'created_at': record['reply_created_at']})
        
    
    return render_template("messages.html",
                           **(base_layout_params(role, site_role)),
                           logged_in_id = session['user_id'] if 'user_id' in session else 0,
                           is_moderator = is_moderator(), 
                           messages = messages, new_message=message,
                           validation=validation)

@app.route('/message', methods=['POST'])
def post_message():
    role, site_role = user_role()
    if role == 'guest':
        return '', 400
    
    cursor = VmsCursor()
    message={"title": '', "content": ''}

    if "message_content" in request.form and "message_title" in request.form:
        message['title'] = request.form["message_title"].strip()
        message['content'] = request.form["message_content"].strip()

        if message['title'] != '':
            cursor.execute("INSERT INTO messages (user_id, competition_id, title, content)"
                        " VALUES (%s, %s, %s, %s);", (session['user_id'], current_competition_id(), message['title'], message['content']))
            message['title'] = ''
            message['content'] = ''

    return '', 200

@app.route('/reply', methods=['POST'])
def post_reply():
    role, site_role = user_role()
    if role == 'guest':
        return '', 400
    
    cursor = VmsCursor()
    
    if 'message_id' in request.form and "reply_content" in request.form:
        reply_message_id = request.form['message_id']
        reply_content = request.form["reply_content"]

        if reply_content != '':
            cursor.execute("INSERT INTO replies (message_id, user_id, content, created_at)"
                           " VALUES (%s, %s, %s, %s);", (reply_message_id, session['user_id'], reply_content, datetime.now()))

    return '', 200

def is_moderator():
    cursor = VmsCursor()
    cursor.execute("SELECT user_id FROM user_competition_moderators WHERE competition_id = %s AND user_id = %s", (current_competition_id(), session['user_id']))
    if cursor.fetchone():
        return True 
    return False

@app.route('/reply/<reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    role, site_role = user_role()
    if role == 'guest':
        return '', 400

    cursor = VmsCursor()    
    if role != "admin" and site_role != 'site admin' and not is_moderator():
        cursor.execute("SELECT user_id FROM replies WHERE reply_id = %s", (reply_id,))
        reply_info = cursor.fetchone()
        if reply_info['user_id'] != session['user_id']:
            flash('You are unable delete the reply', 'danger')
            return '', 400

    cursor.execute("DELETE FROM replies WHERE reply_id = %s", (reply_id,))
    flash('The reply has been deleted', 'success')

    return '', 200

@app.route('/message/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    role, site_role = user_role()
    if role == 'guest':
        return '', 400

    cursor = VmsCursor()
    if role != "admin" and site_role != 'site admin' and not is_moderator():
        cursor.execute("SELECT user_id FROM messages WHERE message_id = %s", (message_id,))
        message_info = cursor.fetchone()
        if message_info['user_id'] != session['user_id']:
            flash('You are unable to delete the message', 'danger')
            return '', 400

    cursor.execute("DELETE FROM messages WHERE message_id = %s", (message_id,))

    return '', 200