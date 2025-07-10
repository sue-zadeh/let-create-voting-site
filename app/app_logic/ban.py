from app.view_logic.base_logic import current_competition_id, VmsCursor


def ban_a_user(user_id, competition_id, reason_for_ban):
    cursor = VmsCursor()
    # User is currently active, and we want to ban them.
    cursor.execute("INSERT INTO bans (user_id, competition_id, ban_date, reason) VALUES (%s, %s, NOW(), %s);", 
                    (user_id, competition_id, reason_for_ban))
    return "User has been banned successfully.", 'success'
    
def unban_a_user(user_id, competition_id):
    cursor = VmsCursor()
    # User is currently banned, and we want to activate them.
    cursor.execute("UPDATE bans SET active = 0 WHERE user_id= %s AND competition_id = %s ORDER BY ban_date DESC LIMIT 1;", (user_id, competition_id))
    return "User has been activated.", "success"
    
def ban_users_at_ip_address(ip_address, event_id, reason_for_ban):
    cursor = VmsCursor()
    competition_id = current_competition_id()
    cursor.execute("""SELECT DISTINCT u.user_id
                        FROM votes v
                        LEFT OUTER JOIN bans b
                            ON v.user_id = b.user_id AND b.competition_id = %s AND b.active = 1
                        JOIN users u ON v.user_id = u.user_id
                        WHERE v.ip_address = %s 
                            AND v.event_id = %s
                            AND b.user_id IS NULL
                   """, (competition_id, ip_address, event_id))
    user_ids = cursor.fetchall()
    had_error = False
    for user_id in user_ids:
        message, message_type = ban_a_user(user_id['user_id'], competition_id, reason_for_ban)
        if message_type != 'success':
            had_error = True
    if not had_error:
        return f"All users at the IP address have been banned successfully", "success"
    else:
        return "Something went wrong", "danger"
