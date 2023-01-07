from flask import render_template

def render_error_page(error_msg):
    return render_template('error_page.html', error=error_msg)