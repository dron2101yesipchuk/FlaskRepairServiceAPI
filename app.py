#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

devices_on_repair = [
    {
        'id': 1,
        'name': u'MacBook Pro',
        'issue': u'Unexpectedly shutting down',
        'can_be_repaired': True
    },
    {
        'id': 2,
        'name': u'MacbookPro',
        'issue': u'An odd stage light effect at the bottom of the display when the lid is fully opened',
        'can_be_repaired': False
    },
    {
        'id': 3,
        'name': u'iPad Pro',
        'issue': u'No sound',
        'can_be_repaired': True
    },
    {
        'id': 4,
        'name': u'iPhone XR',
        'issue': u'White screen',
        'can_be_repaired': False
    },
    {
        'id': 5,
        'name': u'MacBook Air',
        'issue': u'TouchID does not work',
        'can_be_repaired': True
    },
    {
        'id': 6,
        'name': u'iPhone 11 Pro Max Plus S',
        'issue': u'Dust on camera',
        'can_be_repaired': False
    }
]


@app.route('/repair_service/api/v1.0/devices_on_repair', methods=['GET'])
def get_devices():
    return jsonify({'devices_on_repair': devices_on_repair})


@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['GET'])


def get_device(device_id):
    device_on_repair = list(filter(lambda d: d['id'] == device_id, devices_on_repair))
    if len(device_on_repair) == 0:
        abort(404)
    return jsonify({'device_on_repair': device_on_repair[0]})


@app.route('/repair_service/api/v1.0/devices_on_repair', methods=['POST'])
def create_device():
    if not request.json or not 'name' in request.json or not 'issue' in request.json:
        abort(400)
    device = {
        'id': devices_on_repair[-1]['id'] + 1,
        'name': request.json['name'],
        'issue': request.json['issue'],
        'can_be_repaired': False
    }
    devices_on_repair.append(device)
    return jsonify({'device': device}), 201


@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    device = list(filter(lambda d: d['id'] == device_id, devices_on_repair))
    if len(device) == 0:
        abort(404)
    if not request.json:
        abort(400)
    device[0]['name'] = request.json.get('name', device[0]['name'])
    device[0]['issue'] = request.json.get('issue', device[0]['issue'])
    device[0]['can_be_repaired'] = request.json.get('can_be_repaired', device[0]['can_be_repaired'])
    return jsonify({'device': device[0]})


@app.route('/repair_service/api/v1.0/devices_on_repair/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    device = list(filter(lambda d: d['id'] == device_id, devices_on_repair))
    if len(device) == 0:
        abort(404)
    devices_on_repair.remove(device[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(debug=True)
