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
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    shipper_name = db.Column(db.String(100), nullable=False)
    shipper_address = db.Column(db.Text, nullable=False)
    package_status = db.Column(db.String(100), nullable=False)
    
    package_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    package_modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'tracking_id': self.tracking_id,
            'customer_name': self.customer_name,
            'customer_address': self.customer_address,
            'shipper_name': self.shipper_name,
            'shipper_address': self.shipper_address,
            'package_status': self.package_status,
            'package_created': self.package_created,
            'package_modified': self.package_modified
        }     
        return dto
    
class Driver_package(db.Model):
    __tablename__ = 'driver_package'
    
    driver_package_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracking_id = db.Column(db.ForeignKey(
        'package.tracking_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    driver_id = db.Column(db.ForeignKey(
        'driver.driver_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    package_pickup_date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    package_pickup_date_modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)


    driver = db.relationship(
        'Driver', primaryjoin='Driver_package.driver_id == Driver.driver_id', backref='driver_package')
    package = db.relationship(
        'Package', primaryjoin='Driver_package.tracking_id == Package.tracking_id', backref='driver_package')

    def json(self):
        dto = {
            'driver_package_id': self.driver_package_id,
            'tracking_id': self.tracking_id,
            'driver_id': self.driver_id,
            'package_pickup_date_created': self.package_pickup_date_created,
            'package_pickup_date_modified': self.package_pickup_date_modified
        }          
        return dto
    
class Remarks(db.Model):
    remark_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    driver_id = db.Column(db.Integer, nullable=False)
    remark_problem_description = db.Column(db.Text, nullable=False)
    estimated_delay_day = db.Column(db.Integer)
    estimated_delay_hour = db.Column(db.Integer)
    estimated_delay_minute = db.Column(db.Integer)
    
    remark_date_created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    remark_date_modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.now, onupdate=datetime.now)

    def json(self):
        dto = {
            'remark_id': self.remark_id,
            'driver_id': self.driver_id,
            'remark_problem_description': self.remark_problem_description,
            'estimated_delay_day': self.estimated_delay_day,
            'estimated_delay_hour': self.estimated_delay_hour,
            'estimated_delay_minute': self.estimated_delay_minute,
            'remark_date_created': self.remark_date_created,
            'remark_date_modified': self.remark_date_modified
        }     
        return dto
    