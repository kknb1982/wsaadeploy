import requests
from flask import request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
import db, TravelPlan

@app.route('/api/add-travel', methods=['POST'])
# @login_required
def api_add_travel():
    city = request.form.get('city')
    country = request.form.get('country')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    
    new_travel = TravelPlan(
        user_id=current_user.id,
        location_city=city,
        location_country=country,
        start_date=start_date,
        end_date=end_date
    )
    db.session.add(new_travel)
    db.session.commit()

    return jsonify({'success': True})
