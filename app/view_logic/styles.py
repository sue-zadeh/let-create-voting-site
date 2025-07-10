
from flask import request, render_template, redirect, url_for, flash, session, jsonify

from datetime import datetime
from flask import request, render_template, redirect, url_for, flash, session

from .base_logic import VmsCursor, base_layout_params, random_filename, user_role, current_competition_id
from .. import app
import os
from .. import connect
import base64

# Helper function to construct styles dictionary
def construct_styles(name, bg_color, topic_color, topic_size, main_color, main_size):
        return {
            'theme_name': name,
            'background_color': bg_color,
            'topic_text_color': topic_color,
            'topic_font_size': topic_size,
            'main_text_color': main_color,
            'main_font_size': main_size
        }

@app.route('/admin/customise_style', methods=['GET', 'POST'])
def customise_style():
    # Get user roles and competition information
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        flash("You are not an admin of that competition", "warning")
        return redirect(url_for('home'))

    competition_id = current_competition_id()

    cursor = VmsCursor()
    if not cursor:
        flash("Database connection failed.", "danger")
        return redirect(url_for('customise_style'))

    # Fetch themes from 'gallery_themes' table
    cursor.execute("""
        SELECT * FROM gallery_themes 
        WHERE competition_id = 0 OR competition_id = %s 
        ORDER BY gallery_id DESC
    """, (competition_id,))
    themes_gallery = cursor.fetchall()


    theme_name = request.form.get('theme_name', '')  
    topic_text_color = request.form.get('topic_font_color')
    topic_font_size = request.form.get('topic_font_size')
    main_text_color = request.form.get('main_font_color')
    main_font_size = request.form.get('main_font_size')
    background_color = request.form.get('background_color')
    
    params = base_layout_params(role, site_role)
    if request.method == 'POST':
        if request.form.get('preview') == 'true':
            # Replace current_style (i.e. ['styles']) of render arguments with posted settings
            params['styles'] = construct_styles(theme_name, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size)
        elif request.form.get('save') == 'true':
            params['themes_gallery'] = themes_gallery
            try:
                cursor.execute(""" 
                    INSERT INTO themes (competition_id, theme_name, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (competition_id, theme_name, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size))
                flash('Styles applied successfully!', 'success')
                style = construct_styles(theme_name, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size)
                params['styles'] = style
            except Exception as e:
                flash(f'Error saving styles: {e}', 'danger')
            return render_template('styles.html', **params)
        
        elif request.form.get('reset'):
            # Pass default theme to the template for preview without saving
            style = construct_styles('', '#FFFFFF', '#000000', '2rem', '#000000', '1rem')
            flash('Styles reset to default for preview only! Save the changes to apply the style.', 'info')
            # Add the default styles directly into base layout parameters to avoid multiple 'styles' keys
            params = base_layout_params(role, site_role)
            params['themes_gallery'] = themes_gallery
            params['styles'] = style  
            return render_template('styles.html', **params)

        
    current_style = params['styles']
    # when request method is GET
    return render_template('styles.html', **params,
                           themes_gallery=themes_gallery,
                           theme_name=current_style['theme_name'] if current_style and 'theme_name' in current_style else '')




@app.route('/admin/save_to_gallery', methods=['POST'])
def save_to_gallery():
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return jsonify(success=False, message="You are not an admin of that competition")
    
    theme_name = request.form.get('theme_name')
    background_color = request.form.get('background_color')
    topic_text_color = request.form.get('topic_font_color')
    topic_font_size = request.form.get('topic_font_size')
    main_text_color = request.form.get('main_font_color')
    main_font_size = request.form.get('main_font_size')

    # Check if a screenshot file is uploaded
    screenshot = request.files.get('screenshot')
    if not screenshot:
        return jsonify(success=False, message='Screenshot not provided!')

    # Save the screenshot to the 'theme_screenshots' folder
    screenshot_filename = random_filename() + '.png'
    screenshot_path = os.path.join(app.config['UPLOAD_FOLDER'], 'theme_screenshots', screenshot_filename)
    screenshot.save(screenshot_path)

    cursor = VmsCursor()
    if not cursor:
        return jsonify(success=False, message="Database connection failed.")

    try:
       
        # Check if the total number of themes in the gallery is already 6
        cursor.execute("""
            SELECT COUNT(*) AS theme_count FROM gallery_themes 
            WHERE competition_id = %s
        """, (current_competition_id(),))
        theme_count = cursor.fetchone()['theme_count']

        if theme_count >= 6:
            return jsonify(success=False, message='The gallery can only contain 6 competition-specific themes.')

        # Check if the theme name already exists
        cursor.execute("""
            SELECT * FROM gallery_themes 
            WHERE theme_name = %s AND (competition_id = %s OR competition_id = 0)
        """, (theme_name, current_competition_id()))
        existing_theme = cursor.fetchone()

        if existing_theme:
            return jsonify(success=False, message='Theme name must be unique.')


        # Insert the new theme into the gallery_themes table
        cursor.execute("""
            INSERT INTO gallery_themes (
                competition_id, theme_name, screenshot_path, 
                background_color, topic_text_color, topic_font_size, 
                main_text_color, main_font_size
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            current_competition_id(), theme_name, f'theme_screenshots/{screenshot_filename}',
            background_color, topic_text_color, topic_font_size, 
            main_text_color, main_font_size
        ))
        return jsonify(success=True, message='Theme saved to gallery successfully!')
    except Exception as e:
        return jsonify(success=False, message=f'Error saving theme to gallery: {e}')


#--- apply theme------------

@app.route('/admin/apply_theme/<int:theme_id>', methods=['POST'])
def apply_theme(theme_id):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return jsonify(success=False, message="You are not an admin of that competition")
    
    cursor = VmsCursor()
    if not cursor:
        return jsonify(success=False, message="Database connection failed.")

    try:
        # Fetch the theme details from gallery_themes
        cursor.execute("""
            SELECT theme_name, background_color, topic_text_color, topic_font_size, 
                   main_text_color, main_font_size 
            FROM gallery_themes 
            WHERE gallery_id = %s
        """, (theme_id,))
        theme = cursor.fetchone()

        if theme:
            # Update the competition's theme in the themes table
            cursor.execute(""" 
                    INSERT INTO themes (competition_id, theme_name, background_color, topic_text_color, topic_font_size, main_text_color, main_font_size) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (current_competition_id(), theme['theme_name'],
                    theme['background_color'], theme['topic_text_color'], 
                    theme['topic_font_size'], theme['main_text_color'], 
                    theme['main_font_size']
                ))
            # cursor.execute("""
            #     UPDATE themes SET 
            #         background_color = %s, 
            #         topic_text_color = %s, 
            #         topic_font_size = %s, 
            #         main_text_color = %s, 
            #         main_font_size = %s
            #     WHERE competition_id = %s
            # """, (
            #     theme['background_color'], theme['topic_text_color'], 
            #     theme['topic_font_size'], theme['main_text_color'], 
            #     theme['main_font_size'], current_competition_id()
            # ))
            return jsonify(success=True, message='Theme applied successfully!')
        else:
            return jsonify(success=False, message='Theme not found!')
    except Exception as e:
        return jsonify(success=False, message=f'Error applying theme: {e}')



# ----delete a theme ---

@app.route('/admin/delete_theme/<int:theme_id>', methods=['POST'])
def delete_theme(theme_id):
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        return jsonify(success=False, message="You are not an admin of that competition")
    
    cursor = VmsCursor()
    if not cursor:
        return jsonify(success=False, message="Database connection failed.")

    try:
        cursor.execute("DELETE FROM gallery_themes WHERE gallery_id = %s AND competition_id = %s", (theme_id, current_competition_id()))

        return jsonify(success=True, message="Theme deleted successfully!")
    except Exception as e:
        return jsonify(success=False, message=f"Error deleting theme: {e}")

@app.route('/admin/styles_history', methods=['GET'])
def view_styles_history():
    '''This function is used to view the history of style changes made by the user.
    It displays the latest 20 style changes for the competition.'''
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        flash("You are not an admin of that competition", "warning")
        return redirect(url_for('home'))
    competition_id = current_competition_id()

    cursor = VmsCursor()

    # Fetch latest 20 style changes for the competition
    cursor.execute("""
        SELECT themes.*, competitions.*
        FROM themes 
        JOIN competitions ON themes.competition_id = competitions.competition_id
        WHERE themes.competition_id = %s
        ORDER BY themes.date_created DESC
        LIMIT 20;
    """, (competition_id,))
    styles_history = cursor.fetchall()
    # styles_history.sort(key=lambda x: x['style_id'])   # Sort by style_id so that the list won't change order when rolling back a style
    params = base_layout_params(role, site_role)


    return render_template('styles_history.html', **base_layout_params(role, site_role), styles_history=styles_history)

@app.route('/admin/rollback_styles/<int:style_id>', methods=['GET'])
def rollback_styles(style_id):
    '''This function is used to rollback to a previous style.
    The style_id is passed as an argument to the function.'''
    #get user roles
    role, site_role = user_role()
    if role != 'admin' and site_role != 'site admin':
        flash("You are not an admin of that competition", "warning")
        return redirect(url_for('home'))
    # validate the user role
    # Fetch the style details from the database
    cursor = VmsCursor()
    cursor.execute("SELECT * FROM themes WHERE style_id = %s", (style_id,))
    style = cursor.fetchone()

    if not style:
        return redirect(url_for('view_styles_history'))

    # Update the 'themes' table with the selected style
    # Update the date for a specific style
    current_time = datetime.now()
    cursor.execute("UPDATE themes SET date_created = %s WHERE style_id = %s", (current_time, style['style_id']))
    return redirect(url_for('view_styles_history'))


