from flask import redirect, url_for, render_template, session, request, flash, jsonify
from .. import app
from .base_logic import VmsCursor, user_role, VmsCursor, base_layout_params
from collections import defaultdict
from datetime import datetime


@app.route('/view_message_box', methods=["GET"])
def view_message_box():
    '''This function is used to display the message box page. 
    It retrieves the messages sent to and by the current user. 
    The messages are grouped by the sender, and sorted by the sent time in ascending order. '''
    role, site_role = user_role()
    user_id = session['user_id']
    if role == 'guest':
        flash("You have not been logged in yet.", "warning")
        return redirect(url_for('home'))
    cursor = VmsCursor()
    cursor.execute('''
    SELECT 
        users.user_id, 
        username, 
        COALESCE(user_competition_roles.role, site_role) AS site_role
    FROM 
        users
    LEFT JOIN
        user_competition_roles
    ON 
        users.user_id = user_competition_roles.user_id
    WHERE 
        users.user_id != %s
    ''', (user_id,))
    
    user_list = cursor.fetchall()
    combined_grouped_messages = defaultdict(list)


    # get the messages sent to the current user
    cursor.execute('''
    SELECT 
        from_user, 
        from_user as other_user_id,
        to_user, 
        message,
        users.username as username,
        users.username as display_username,
        users.site_role as site_role,
        sent
    FROM 
        instant_messages
    LEFT JOIN 
        users
    ON
        users.user_id = instant_messages.from_user
    WHERE 
        to_user = %s
    ORDER BY 
        sent DESC
    ''', (user_id,))
    # display_username is used to display the other user's name in the message history
    incoming_messages = cursor.fetchall()

    for each_message in incoming_messages:
        combined_grouped_messages[(each_message['username'], each_message['site_role'], each_message['other_user_id'])].append(each_message)


    # get the messages sent by the current user
    cursor.execute('''
    SELECT 
        from_user, 
        to_user,
        to_user as other_user_id, 
        message,
        'me' as display_username,
        users.username,
        users.site_role as site_role,
        sent
    FROM
        instant_messages
    LEFT JOIN
        users
    ON
        users.user_id = instant_messages.to_user
    WHERE
        from_user = %s
    ORDER BY
        sent DESC
    ''', (user_id,))
    # display_username is used to display current user' name, showing as 'me' in the message history
    outgoing_messages = cursor.fetchall()

    for each_message in outgoing_messages:
        combined_grouped_messages[(each_message['username'], each_message['site_role'], each_message['other_user_id'])].append(each_message)

    # sort the messages by the sent time in ascending order
    for key, messages in combined_grouped_messages.items():
        messages.sort(key=lambda x: x['sent'], reverse=False)
        
    combined_grouped_messages = dict(combined_grouped_messages)

    return render_template('message_box.html', user_list=user_list, messages=combined_grouped_messages, **(base_layout_params(role, site_role)))



import logging
# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/send_message', methods=['POST'])
def send_message():
    '''This function is used to send a message to another user.'''
    try:
        receiver_id = request.json['receiver_id']
        message = request.json['message']
        sender_id = session['user_id']

        cursor = VmsCursor()  
        query = "INSERT INTO instant_messages (from_user, to_user, message) VALUES (%s, %s, %s)"
        cursor.execute(query, (sender_id, receiver_id, message))
        return jsonify(success=True, sender_id=sender_id)
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify(success=False, error=str(e)), 500  # Return an error response
    finally:
        pass
        #cursor.close()  # Ensure the cursor is closed


# user_last_viewed = {}
# @app.route('/check_new_messages', methods=['POST'])
# def check_new_messages():
#     '''This function is used to check for new messages sent to the current user after the last viewed time.'''
#     try:
#         user_id = request.json['user_id']
#         last_viewed_time = user_last_viewed.get(user_id, datetime.min)
        
#         cursor = VmsCursor()
#         cursor.execute('''
#             SELECT * FROM instant_messages
#             WHERE to_user = %s AND sent > %s
#         ''', (user_id, last_viewed_time))
#         new_messages = cursor.fetchall()

#         # Update the last viewed time to the current time
#         user_last_viewed[user_id] = datetime.now()
#         return jsonify(new_messages=new_messages, new_message_count=len(new_messages))
#     except Exception as e:
#         logging.error(f"Error checking new messages: {e}")
#         return jsonify(success=False, error=str(e)), 500
#     finally:
#         cursor.close()  # Ensure the cursor is closed

        


# @app.route('/check_new_messages', methods=['POST'])
# def check_new_messages():
#     '''This function checks for new messages sent to the current user after the last viewed time.'''
#     cursor = VmsCursor()  
#     try:
#         user_id = request.json['user_id']

#         # try getting the last viewed time for the user from the 'user_last_viewed' table
#         cursor.execute('''
#             SELECT last_viewed_time FROM user_last_viewed WHERE user_id = %s
#         ''', (user_id,))
#         row = cursor.fetchone()
        
#         if row:
#             last_viewed_time = row['last_viewed_time']  # If user exists in the table, it returns the corresponding time.

#         else:
#             last_viewed_time = datetime.min   # If user does not exist, it returns datetime.min which represents the minimum date value (0001-01-01 00:00:00).

        
#         # Get new messages sent to the user after the last viewed time
#         cursor.execute('''
#             SELECT * FROM instant_messages
#             WHERE to_user = %s AND sent > %s
#         ''', (user_id, last_viewed_time))
#         new_messages = cursor.fetchall()

#         # Update the last viewed time to the current time
#         current_time = datetime.now()
#         if row:    # If the row exists, update the last viewed time.
#             cursor.execute('''
#                 UPDATE user_last_viewed SET last_viewed_time = %s WHERE user_id = %s
#             ''', (current_time, user_id))
#         else:    # If the row does not exist, insert the user_id and last viewed time.
#             cursor.execute('''
#                 INSERT INTO user_last_viewed (user_id, last_viewed_time) VALUES (%s, %s)
#             ''', (user_id, current_time))

#         return jsonify(new_messages=new_messages, new_message_count=len(new_messages))
#     except Exception as e:
#         logging.error(f"Error checking new messages: {e}")
#         return jsonify(success=False, error=str(e)), 500
#     finally:
#         cursor.close()  # Ensure the cursor is closed


@app.route('/check_new_messages', methods=['POST'])
def check_new_messages():
    '''This function checks for new messages sent to the current user. 
    It retrieves the messages sent to the user after the last viewed message ID.'''
    cursor = VmsCursor()  
    try:
        user_id = request.json['user_id']

        # Try getting the last message ID for the user from the 'user_last_message' table
        cursor.execute('''
            SELECT last_message_id FROM user_last_message WHERE user_id = %s
        ''', (user_id,))
        row = cursor.fetchone()
        
        last_message_id = None
        if row:
            last_message_id = row['last_message_id']  # If user exists in the table, it returns the corresponding ID.
        else:
            last_message_id = None  # If user does not exist, initialise as None.

        # Get new messages sent to the user after the last viewed message ID
        if last_message_id is not None:
            cursor.execute('''
                SELECT * FROM instant_messages
                WHERE to_user = %s AND im_id > %s
            ''', (user_id, last_message_id))
        else:
            cursor.execute('''
                SELECT * FROM instant_messages
                WHERE to_user = %s
            ''', (user_id,))

        new_messages = cursor.fetchall()




        # Update the last viewed message ID to the highest ID of the newly fetched messages
        if new_messages:
            new_last_message_id = max(message['im_id'] for message in new_messages)
            if row:  # If the row exists, update the last message ID.
                cursor.execute('''
                    UPDATE user_last_message SET last_message_id = %s WHERE user_id = %s
                ''', (new_last_message_id, user_id))
            else:  # If the row does not exist, insert the user_id and last message ID.
                cursor.execute('''
                    INSERT INTO user_last_message (user_id, last_message_id) VALUES (%s, %s)
                ''', (user_id, new_last_message_id))

        return jsonify(new_messages=new_messages, new_message_count=len(new_messages))
    except Exception as e:
        logging.error(f"Error checking new messages: {e}")
        return jsonify(success=False, error=str(e)), 500
    finally:
        pass
        #cursor.close()  # Ensure the cursor is closed
