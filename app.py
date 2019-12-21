#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from repair_service import RepairService

app = Flask(__name__)

service = RepairService()

@app.route('/repair_service/api/v1.0/devices_on_repair', methods=['GET'])
def get_devices():
    return jsonify({'devices_on_repair': service.get_devices()})

@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device_on_repair = service.get_device_by_id(device_id)
    if len(device_on_repair) == 0:
        abort(404)
    return jsonify({'device_on_repair': device_on_repair[0]})

@app.route('/repair_service/api/v1.0/devices_on_repair', methods=['POST'])
def create_device():
    if not request.json or not 'name' in request.json or not 'issue' in request.json:
        abort(400)
    name = request.json['name']
    issue = request.json['issue']
    new_device = service.add_device(name, issue)
    return jsonify({'device': new_device}), 201

@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    if not request.json:
        abort(400)
    device = service.update_device(device_id, request.json.get('name'), request.json.get('issue'))
    if len(device) == 0:
        abort(404)
    return jsonify({'device': device[0]})

@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    if service.delete_device(device_id):
        return jsonify({'result': True})
    else:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)