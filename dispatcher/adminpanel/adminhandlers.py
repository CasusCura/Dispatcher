from tornado.web import RequestHandler
from tornado_sqlalchemy import SessionMixin
from dispatcher.models import (Device,
                               DeviceStatus,
                               DeviceType,
                               NurseDevice,
                               NurseDeviceType,
                               PatientDevice,
                               PatientDeviceType,
                               RequestType)
import json


class PanelHandler(RequestHandler, SessionMixin):
    def get(self):
        """Render the panel."""
        self.render('static/admin.html')


class DeviceHandler(RequestHandler, SessionMixin):
    def get(self):
        """Get all values for a given device"""
        id = self.get_argument('id', None)
        ret = None
        if id:
            ret = self._get(id.encode())
        else:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'No id provided'
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _get(self, id):
        device = None
        with self.make_session() as session:
            device = session.query(Device)\
                .filter(Device.id == id)\
                .first()
            if device:
                return {
                    'status': 'OK',
                    'device': device.serialize(),
                    'code': 200,
                }
        return {
            'status': 'BAD',
            'code': 400,
        }

    def post(self):
        """POST - update the values for the given device id."""
        device_json = self.get_argument('device', None)
        device = None
        ret = None
        try:
            device = json.load(device_json)
            ret = self._post(device)
        except Exception as e:
            ret = {
                'status': 'FAILED',
                'code': 500,
                'error': 'ALL YOU BASE ARE BELONG TO US NOW',
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, device_json):
        devicetype_id = None
        location = None
        try:
            devicetype_id = device_json['devicetype'].encode()
            location = device_json['location']
        except Exception as e:
            return {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameters; Require location and \
                device type'
            }

        patientdevice = None
        with self.make_session() as session:
            devicetype = session.query(DeviceType)\
                .filter(DeviceType.id == devicetype_id)\
                .first()
            if devicetype is None:
                return {
                    'status': 'BAD',
                    'code': 400,
                    'error': 'DeviceType doesn\'t exist'
                }
            patientdevice = PatientDevice(devicetype.id, location)
            session.add(patientdevice)
        if patientdevice:
            return {
                'status': 'OK',
                'code': 204,
                'device_id': patientdevice.id
            }
        else:
            return {
                'status': 'FAILED',
                'code': 500,
                'error': 'Must construct additional pylons & devs',
            }


class DevicesHandler(RequestHandler, SessionMixin):
    def get(self):
        """GET - returns all devices who's status satisfy the filter."""
        status = self.get_argument('status', None)
        used_by = self.get_argument('used_by', None)
        ret = None
        if used_by:
            if status:
                try:
                    status = DeviceStatus[str(status)].value
                except KeyError as e:
                    status = None
            ret = self._get(status, str(used_by))
        else:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameter status'
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _get(self, status, used_by):
        device_json = []
        with self.make_session() as session:
            baked_query = None
            if used_by is 'nurse':
                baked_query = session.query(NurseDevice)
            elif used_by is 'patient':
                baked_query = session.query(PatientDevice)
            else:
                baked_query = session.query(Device)
            if status and status is not 'ALL':
                devices = baked_query\
                    .filter(Device.status == status)\
                    .all()
            else:
                devices = baked_query.all()
            print(devices)
            if len(devices) is 0:
                device_json = []
            else:
                device_json = [d_t.serialize() for d_t in devices]
        return {
            'status': 'OK',
            'code': 200,
            'devices': device_json,
        }


class DeviceTypeHandler(RequestHandler, SessionMixin):
    """Handles returning and creating new device types."""
    def get(self):
        """Handle get requests when an id is provided."""
        id = self.get_argument('id', None)
        ret = None
        if id:
            ret = self._get(id.encode())
        else:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'No id provided',
            }

        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _get(self, id):
        """Queries the dispatcher back end for the proper device type."""
        device_type = None
        with self.make_session() as session:
            device_type_q = session.query(DeviceType)\
                .filter(DeviceType.id == id)\
                .first()
            if device_type_q:
                device_type = device_type_q.serialize()

        if device_type:
            return {
                'status': 'OK',
                'code': 200,
                'device_type': device_type,
            }
        else:
            return {
                'status': 'BAD',
                'code': 400,
                'error': 'Matching type not found'
            }

    def post(self):
        """Handles creating/updating a new device type."""
        data = json.loads(self.request.body)
        ret = None
        device_type = None
        used_by = None
        print(data)
        try:
            device_type = data['device_type']
            used_by = device_type['used_by']
        except KeyError as ke:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameters',
            }
        except Exception as e:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'Too many parameters',
            }

        if ret is None:
            try:
                ret = self._post(device_type, used_by)
            except Exception as e:
                # TODO: Make this Json load specific
                print(e.printstacktrace())
                ret = {
                    'status': 'BAD',
                    'code': 400,
                    'error': 'Invalid device type format',
                }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, params, used_by):
        """Inserts the new devicetype"""
        device_type = None
        if 'id' in params:
            id = params['id'].encode()
            with self.make_session() as session:
                if used_by is 'nurse':
                    device_type = session.query(NurseDeviceType)\
                        .filter_by(id=id)\
                        .first()
                    device_type.update(
                        product_name=params['product_name'],
                        product_description=params['product_description'],
                        used_by=used_by)
                elif used_by is 'patient':
                    device_type = session.query(PatientDeviceType)\
                        .filter_by(id=id)\
                        .first()
                    device_type.product_name = params['product_name'],
                    device_type.product_description = \
                        params['product_description']
                if device_type:
                    return {
                        'status': 'OK',
                        'devicetype_id': device_type.id,
                        'code': 200,
                    }
                else:
                    return {
                        'status': 'FAILED',
                        'code': 500,
                        'error': 'CSGames was an inside job',
                    }
        else:
            with self.make_session() as session:
                e = DeviceType
                if used_by is 'nurse':
                    e = NurseDeviceType
                elif used_by is 'patient':
                    e = PatientDeviceType
                device_type = e(
                    product_name=params['product_name'],
                    product_description=params['product_description'])
                session.add(device_type)
            if device_type:
                return {
                    'status': 'OK',
                    'code': 200,
                }
            return {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameters',
            }


class DeviceTypesHandler(RequestHandler, SessionMixin):
    def get(self):
        used_by = self.get_argument('used_by', None)
        ret = None
        if used_by:
            ret = self._get(str(used_by))
        else:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'No parameters',
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _get(self, used_by):
        device_types_json = None

        print(used_by)
        with self.make_session() as session:
            if used_by is 'nurse':
                device_types = session.query(NurseDeviceType).all()
            elif used_by is 'patient':
                device_types = session.query(PatientDeviceType).all()
            else:
                device_types = session.query(DeviceType).all()
            device_types_json = [d_t.serialize() for d_t in device_types]
            print(device_types_json)
        if device_types_json:
            return {
                'status': 'OK',
                'code': 200,
                'device_types': device_types_json,
            }
        else:
            return {
                'status': 'FAILED',
                'code': 500,
                'error': 'pay me IN BITCOIN',
            }


class CredentialsHandler(RequestHandler, SessionMixin):
    def get(self):
        pass
