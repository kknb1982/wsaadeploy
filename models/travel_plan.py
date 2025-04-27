from datetime import datetime
from yourapp import db  # Adjust if your db is imported differently
from flask_login import UserMixin

class TravelPlan(db.Model):
    __tablename__ = 'travel_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Assumes you have a 'User' model
    location_city = db.Column(db.String(100), nullable=False)
    location_country = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Cache latitude and longitude for the location
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)

    # Relationship (if you want to quickly access user info)
    user = db.relationship('User', back_populates='travel_plans')

    def __repr__(self):
        return f'<TravelPlan {self.location_city}, {self.location_country} ({self.start_date} to {self.end_date})>'
