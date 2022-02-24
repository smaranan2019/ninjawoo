from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Driver(db.Model):
    __tablename__ = 'driver'

    driver_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_hp = db.Column(db.Integer, nullable=False)
    driver_tele_handle = db.Column(db.String(100))
    driver_date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    driver_date_modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'driver_id': self.driver_id,
            'driver_hp': self.driver_hp,
            'driver_tele_handle': self.driver_tele_handle,
            'driver_date_created': self.driver_date_created,
            'driver_date_modified': self.driver_date_modified
        }     
        return dto

class Package(db.Model):
    tracking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.Integer, nullable=False)
    customer_address = db.Column(db.String(100))
    shipper_name = db.Column(db.String(100))
    shipper_address = db.Column(db.String(100))
    package_status = db.Column(db.String(100))
    
    shipper_name = db.Column(db.DateTime, nullable=False, default=datetime.now)
    driver_date_modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'tracking_id': self.tracking_id,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'shipper_name': self.shipper_name,
            'driver_date_modified': self.driver_date_modified
        }     
        return dto
    
class Something(db.Model):
    __tablename__ = 'package'

    card_id = db.Column(db.ForeignKey(
        'card.card_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True, primary_key=True)
    seller_id = db.Column(db.Integer, nullable=False)
    seller_paypal_id = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(4,2), nullable=False)

    card = db.relationship(
        'Card', primaryjoin='Card_details.card_id == Card.card_id', backref='card_details')

    def json(self):
        return {'seller_id': self.seller_id, 'seller_paypal_id': self.seller_paypal_id, 'price': self.price, 'card_id': self.card_id}
    