from flask import render_template
from HoundSploit.searcher.engine.updates import get_last_db_update_date
  
  
def render_settings(db_update_alert, sw_update_alert, no_updates_alert):
    return render_template('settings.html', latest_db_update=get_last_db_update_date(),
                        db_update_alert=db_update_alert, sw_update_alert=sw_update_alert,
                        no_updates_alert=no_updates_alert)