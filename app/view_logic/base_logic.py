"""
Base view providing useful functions for all the other views
"""
import random
from uuid import uuid4
from flask_hashing import Hashing
from flask import session
from collections import defaultdict
from .. import app
import mysql.connector 
from .. import connect
import os

ip_vertified = defaultdict(lambda: True)

# pooled connection seems to work ok
db_connection_pool = None
def get_cursor2(dictionary=True, buffered=True):
    global db_connection_pool
 
    try:
        if db_connection_pool is None:
            db_connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                user = connect.db_user,
                password = connect.db_pass,
                host = connect.db_host,
                database = connect.db_name,
                connection_timeout=300,
                autocommit = True)
            print("Connection successful")
    
        connection = db_connection_pool.get_connection()
        cursor = connection.cursor(dictionary=dictionary, buffered=buffered)

        return cursor, connection
    except mysql.connector.Error as e:
         print("Error while connecting to MySQL", e)
         return None, None

# In the comments, there are some debug variables if people
# are concerned whether a cursor gets closed promptly
#numberC = 1
class VmsCursor:
    def __init__(self):
        """Get a cursor connection to database"""
        #global numberC
        #self.num = numberC = numberC + 1
        #print("Constructor called: " + str(self.num))
        self.cursor, self.connection = get_cursor2()

    def execute(self, query_string, tuple_data=()):
        """Execute a query"""
        self.cursor.execute(query_string, tuple_data)

    def fetchone(self):
        """Fetch a record from the result set"""
        return self.cursor.fetchone()

    def fetchall(self):
        """Fetch all of the records from the result set"""
        return self.cursor.fetchall()

    def __del__(self):
        """Close the cursor and connection to release the connection back to the pool for re-use"""
        #print("Destructor called: " + str(self.num))
        self.cursor.close()
        self.connection.close()

def setup_session(user_id, username):
    """Setup the user session variables after login"""
    session['user_id'] = user_id
    session['username'] = username

def cleanup_session():
    """Remove user session variables because user has been logged out"""
    session.pop('user_id', None)
    session.pop('username', None)

def base_layout_params(role_competition, role_site):
    """A function to include the parameters that the base_layout.html page needs.

    Include a call to this function in every render_template call, and pass in the user_role(), and site_role() as
    variables. They were not called in this function because typically the caller has already queried for them, so
    don't need to do another query.
    """
    cursor = VmsCursor()
    competition_id = current_competition_id()

    # Fetch competition-specific styles
    cursor.execute("""
        SELECT theme_name, background_color, topic_text_color, topic_font_size, 
               main_text_color, main_font_size 
        FROM themes 
        WHERE competition_id = %s 
        ORDER BY date_created DESC LIMIT 1
    """, (competition_id,))

    styles = cursor.fetchone() or {}


     # Fetch competition-specific themes from the gallery
    cursor.execute("""
        SELECT gallery_id, theme_name, screenshot_path, background_color, 
               topic_text_color, topic_font_size, main_text_color, main_font_size
        FROM gallery_themes 
        WHERE competition_id = %s
    """, (competition_id,))
    themes_gallery = cursor.fetchall()

    # Other params
    cursor.execute("SELECT competition_id, name FROM competitions ORDER BY name ASC")
    competitions = cursor.fetchall()

    current_competition = None
    for competition in competitions:
        if competition['competition_id'] == competition_id:
            current_competition = competition['name']
            break

    return {
        'competitions': competitions,
        'current_competition': current_competition,
        'current_competition_id': competition_id,
        'logged_in_role': role_competition,
        'logged_in_site_role': role_site,
        'current_user_id': session['user_id'] if 'user_id' in session else 0,
        'styles': styles,  # Pass the styles to templates
    }
#  {'competition-background-color': 'white'}}


def current_competition_id():
    if 'competition_id' not in session:
        session['competition_id'] = 0

    return session['competition_id']

def random_competition():
    cursor = VmsCursor()
    cursor.execute("SELECT competition_id, name, description FROM competitions ORDER BY name ASC")
    competitions = cursor.fetchall()
    if competitions:
        random.shuffle(competitions)
        return competitions[0]['competition_id']
    else:
        return 0    

def random_filename():
    return str(uuid4())

def user_site_role():
    """Returns user's site_role if the user account is active, otherwise returns 'guest'"""
    if 'user_id' not in session:
        return 'guest'
    
    # Check user access every time
    cursor = VmsCursor()
    cursor.execute("SELECT site_role, is_active FROM users WHERE user_id = %s;",(session['user_id'],))
    user = cursor.fetchone()
    if user and user['is_active'] == 1:
        return user['site_role']
    else:
        cleanup_session()
        return 'guest'

def user_role():
    """Check the user's role"""
    site_role = user_site_role()
    if site_role == 'guest':
        return 'guest', 'guest'
    
    cursor = VmsCursor()

    cursor.execute("SELECT role FROM user_competition_roles WHERE user_id = %s AND competition_id = %s;",(session['user_id'], current_competition_id()))
    user_competition_role = cursor.fetchone()
    if user_competition_role:
        return user_competition_role['role'], site_role
    else:
        return 'voter', site_role

@app.template_filter()
def format_date(date):
    return date.strftime("%d %b %Y")

@app.template_filter()
def format_datetime(datetime):
    return datetime.strftime("%d %b %Y %H:%M")

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

