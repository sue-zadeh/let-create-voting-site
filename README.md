# Tree of the Year

A site for running NZ Native Tree of the Year events.

## How to run locally

1. Download via Github Desktop option in Code dropdown at top-right of page.
2. Open folder in VS Code.
3. Create a virtual environment and select the requirements.txt file to install dependencies.
4. In debug options, select create launch.json, and pick Python Debugger -> Flask -> **init**.py.
5. In the launch.json file change it to "FLASK_APP": "app", so without the **init**.py bit.
6. Create a database in your database server and run the CreateDatabase.sql (and PopulateDatabase.sql for example data) scripts on that database.
7. Set up a connect.py file as per the Configuration section below.
8. The app should now run via Start Debugging.

## Configuration

The user must add a connect.py file to the app folder that has the following lines, edited by the user with appropriate values specific to their setup:

```
db_user = "mysqlUsername" # put your MySQL username here
db_pass = "the password for the above account"
db_host = "the database server, if running locally would be 'localhost'"
db_port = "the database port, often 3306"
db_name = "vms" # the name of the database schema you've run the create database scripts in

UPLOAD_FOLDER = 'app/static' # This should not be changed except by prepending folder names at the start, for instance on PythonAnywhere the venv is one folder higher so the project folder name is also needed.
```

## Usage

On the website main page, the user can see the home page/dashboard for their user role, e.g. visitor, voter, scrutineer, admin.

Anyone using the site can see a list of previous events, and the current event.

### Visitors

Visitors can register as a voter using the register link, and then filling in their details. This creates a voter account, which they can then log in to, to vote in events.

### Voters

Voters have the option of voting for a competitor in the current event, but they can only vote once for each event.

### Scrutineers

Scrutineers can view the list of votes and approve events.

### Admins

Admins can create and delete future events; add, edit, delete competitors in future events.

#### Add, edit, deleting competitors

On a event page that is in the future, there is a button in the top-right to create a competitor. This lets
them fill in name, image and description for a new competitor. The name and image are required. An admin can edit or remove
an existing competitor by clicking on the '...' dropdown button at the bottom-right of the competitor's image. All of a competitor's
details may be edited.

## Example usernames and passwords set up by the PopulateDatabase.sql script

```
Voters:

voter1: Voter1pa$s
voter2: Voter2pa$s
voter3: Voter3pa$s
voter4: Voter4pa$s
voter5: Voter5pa$s
voter6: Voter6pa$s
voter7: Voter7pa$s
voter8: Voter8pa$s
voter9: Voter9pa$s
voter10: Voter10pa$s
voter11: Voter11pa$s
voter12: Voter12pa$s
voter13: Voter13pa$s
voter14: Voter14pa$s
voter15: Voter15pa$s
voter16: Voter16pa$s
voter17: Voter17pa$s
voter18: Voter18pa$s
voter19: Voter19pa$s
voter20: Voter20pa$s
voter21: Voter21pa$s
voter22: Voter22pa$s
voter23: Voter23pa$s
voter24: Voter24pa$s
voter25: Voter25pa$s
voter26: Voter26pa$s
voter27: Voter27pa$s
voter28: Voter28pa$s
voter29: Voter29pa$s
voter30: Voter30pa$s

Scrutineers:
scrutineer1: Scrut1pa$s
scrutineer2: Scrut2pa$s
scrutineer3: Scrut3pa$s
scrutineer4: Scrut4pa$s
scrutineer5: Scrut5pa$s

Admins:
admin1: Admin1pa$s
admin2: Admin2pa$s

Site_admin:
site_admin1: Siteadmin1pa$s
```

## Structure

The `__init__.py` sets up the Flask app and imports the webpage routes via the views.py file. The views.py file currently imports the following pages from the view_logic folder:

- home
- profile

New types of pages can be added to the view_logic folder and set up to be used by adding an import in the views.py file.  
Templates are in the templates folder.  
JavaScript files are in the static/js folder.

## References:

Example images are from:

1. My Native Forest. (n.d.). _Native trees of New Zealand_. Retrieved August 9, 2024, from https://www.mynativeforest.com/nz-native-trees
2. Trees That Count. (n.d.). _Aotearoa New Zealand's native trees_. Retrieved August 9, 2024, from https://treesthatcount.co.nz/native-trees
3. Kauri Tree Day. (2024, June 17). _HolidaySmart_. Retrieved August 12, 2024, from https://www.holidaysmart.com/holidays/daily/kauri-tree-day
4. Bird of the Year (n.d.). _Forest & Bird - Bird of the Year_. Retrieved October 28, 2024, from https://www.birdoftheyear.org.nz/ (Image credit - Steve Attwood)
5. Flickr (2018, September 25). _Jake Osborne_. Retrieved October 28, 2024, from https://www.flickr.com/photos/theylooklikeus/44902122001/in/photolist-2bpR7vg-6kVtBj-25ipEJv-2cuduHT-9vUUKZ-2iaP2j-2exWLNh-c7sE8N-a2rzW5-qDbWHw-dALeQj-DUupL-ESYu5D-5NSxfk-5wZYQA-27JBwTj-8aAUT1-baTSrX-2eEKK5Q-2dfzvjL-A4Lks-aiDdFA-biGLMz-24Sjewq-N18XGB-D6GbnD-5k7VGH-2hzbUe-4dGsnt-T2E3K7-buoiTt-95Btuq-5jtwqA-baU1Ve-2aoSxRD-4oEU7d-8yFi5Q-6mQK2p-28eEnXi-2cAosME-biGLVi-29xiHxU-R3mXgK-2exWHiS-2aq8VcE-c9DLg-26VMJbT-9z4EGu-28BhTDR-es2wb
6. Conservation Blog (2013, October 16). _Photo of the week: Tokoeka kiwi_. Retrieved October 28, 2024, from https://blog.doc.govt.nz/tag/southern-brown/
‌
