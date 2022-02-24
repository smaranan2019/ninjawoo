from check_remarks import Package, Driver_package, Remarks
from flask import jsonify


def serviceIsRunning():
    return "Service is running!"

def show_all_remarks_from_tracking_id(tracking_id):
    package = Package.query.filter_by(tracking_id = tracking_id).order_by(Package.tracking_id.desc()).first()
    if package:
        driver_package = Driver_package.query.filter_by(tracking_id=tracking_id).order_by(Driver_package.driver_package_id.desc()).first()
        if driver_package:
            remarkList = Remarks.query.filter(Remarks.remark_date_created >= package.package_created).all()
            if len(remarkList):
                return jsonify(
                    {
                        "code": 200,
                        "data": {
                            "package": package.json(),
                            "remarks": [remark.json() for remark in remarkList]
                        }
                    }
                )
            return jsonify(
        {
            "code": 404,
            "message": "There are no remarks from driver ID "+driver_package.driver_id+"assigned to the package with this tracking ID " + tracking_id
        }
        ), 404
            
        return jsonify(
        {
            "code": 404,
            "message": "There are no drivers assigned to the package with this tracking ID " + tracking_id
        }
        ), 404
            
    return jsonify(
        {
            "code": 404,
            "message": "There are packages with this tracking ID " + tracking_id
        }
    ), 404

