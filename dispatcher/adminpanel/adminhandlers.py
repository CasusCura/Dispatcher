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
        id = self.get_argument('device_id', None)
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
        ret = None
        try:
            data = json.loads(self.request.body)
            device = data['device']
            ret = self._post(device)
        except Exception as e:
            print(e)
            raise e
            ret = {
                'status': 'FAILED',
                'code': 500,
                'error': 'ALL YOU BASE ARE BELONG TO US NOW',
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, params):
        if 'device_id' in params:
            id = params['device_id'].encode()
            with self.make_session() as session:
                device = None
                if params['used_by'] == 'nurse':
                    device = session.query(NurseDevice)\
                        .filter_by(id=id)\
                        .first()
                    device.status = params['status']
                    device.floor = params['floor']
                elif params['used_by'] == 'patient':
                    device = session.query(PatientDeviceType)\
                        .filter_by(id=id)\
                        .first()
                    device.status = params['status']
                    device.location = params['location']
                if device:
                    return {
                        'status': 'OK',
                        'device_id': device.id,
                        'code': 200,
                    }
            return {
                'status': 'FAILED',
                'code': 500,
                'error': 'CSGames was an inside job',
            }
        else:
            with self.make_session() as session:
                device = None
                if params['used_by'] == 'nurse':
                    device = NurseDevice(params['device_type'],
                                         'None',
                                         params['serial'])
                elif params['used_by'] == 'patient':
                    device = PatientDevice(params['device_type'],
                                           'None',
                                           params['serial'])
                session.add(device)
                if device:
                    return {
                        'status': 'OK',
                        'code': 200,
                        'device_id': str(device.id)[2:-1]
                    }
            return {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameters',
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
            if used_by == 'nurse':
                baked_query = session.query(NurseDevice)
            elif used_by == 'patient':
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
        id = self.get_argument('device_type_id', None)
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
        ret = None
        device_type = None
        try:
            data = json.loads(self.request.body)
            device_type = data['device_type']
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
                ret = self._post(device_type)
            except Exception as e:
                # TODO: Make this Json load specific
                ret = {
                    'status': 'BAD',
                    'code': 400,
                    'error': 'Invalid device type format',
                }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, params):
        """Inserts the new devicetype"""
        device_type = None
        if 'device_type_id' in params:
            id = params['device_type_id'].encode()
            with self.make_session() as session:
                if params['used_by'] is 'nurse':
                    device_type = session.query(NurseDeviceType)\
                        .filter_by(id=id)\
                        .first()
                    device_type.product_name = \
                        params['product_name']
                    device_type.product_description = \
                        params['product_description']
                elif params['used_by'] is 'patient':
                    device_type = session.query(PatientDeviceType)\
                        .filter_by(id=id)\
                        .first()
                    device_type.product_name = params['product_name'],
                    device_type.product_description = \
                        params['product_description']
                if device_type:
                    return {
                        'status': 'OK',
                        'device_type_id': device_type.id,
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
                device_type = None
                if params['used_by'] == 'nurse':
                    device_type = NurseDeviceType(
                            product_name=params['product_name'],
                            product_description=params['product_description'])
                elif params['used_by'] == 'patient':
                    device_type = PatientDeviceType(
                        product_name=params['product_name'],
                        product_description=params['product_description'])
                session.add(device_type)
                if device_type:
                    return {
                        'status': 'OK',
                        'code': 200,
                        'devicetype_id': str(device_type.id)[2:-1]
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
        with self.make_session() as session:
            if used_by == 'nurse':
                device_types = session.query(NurseDeviceType).all()
            elif used_by == 'patient':
                device_types = session.query(PatientDeviceType).all()
            else:
                device_types = session.query(DeviceType).all()
            if len(device_types) is 0:
                device_types_json = []
            else:
                device_types_json = [d_t.serialize() for d_t in device_types]
        return {
            'status': 'OK',
            'code': 200,
            'device_types': device_types_json,
        }


class RequestTypeHandler(RequestHandler, SessionMixin):
    """Handles returning and creating new request types."""
    def get(self):
        """Handle get requests when an id is provided."""
        id = self.get_argument('request_type_id', None)
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
        """Queries the dispatcher back end for the proper request type."""
        request_type = None
        with self.make_session() as session:
            request_type = session.query(RequestType)\
                .filter(RequestType.id == id)\
                .first()
            if request_type:
                    return {
                        'status': 'OK',
                        'code': 200,
                        'request_type': request_type.serialize(),
                    }
        return {
            'status': 'BAD',
            'code': 400,
            'error': 'Matching type not found'
        }

    def post(self):
        """Handles creating/updating a new Request type."""
        ret = None
        request_type = None
        try:
            data = json.loads(self.request.body)
            request_type = data['request_type']
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
                ret = self._post(request_type)
            except Exception as e:
                # TODO: Make this Json load specific
                raise e
                ret = {
                    'status': 'BAD',
                    'code': 400,
                    'error': 'Invalid request type format',
                }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _post(self, params):
        """Inserts the new devicetype"""
        request_type = None
        if 'request_type_id' in params:
            id = params['request_type_id'].encode()
            with self.make_session() as session:
                request_type = session.query(RequestType)\
                    .filter_by(id=id)\
                    .first()
                request_type.device_request_id = params['device_request_id']
                request_type.name = params['name']
                request_type.description = params['description']
                request_type.priority = params['priority']

                if request_type:
                    return {
                        'status': 'OK',
                        'requesttype_id': str(request_type.id)[2:-1],
                        'code': 200,
                    }
                return {
                    'status': 'FAILED',
                    'code': 500,
                    'error': 'CSGames was an inside job',
                }
        else:
            with self.make_session() as session:
                request_type = RequestType(
                        params['device_request_id'],
                        params['description'],
                        params['device_type_id'],
                        params['priority'])
                session.add(request_type)
                return {
                    'status': 'OK',
                    'code': 200,
                    'request_type_id': str(request_type.id)[2:-1]
                }
            return {
                'status': 'BAD',
                'code': 400,
                'error': 'Missing parameters',
            }


class RequestTypesHandler(RequestHandler, SessionMixin):
    def get(self):
        device_type = self.get_argument('device_type', None)
        ret = None
        if device_type:
            ret = self._get(device_type.encode())
        else:
            ret = {
                'status': 'BAD',
                'code': 400,
                'error': 'No parameters',
            }
        self.set_status(ret['code'])
        self.write(ret)
        self.finish()

    def _get(self, device_type):
        request_types_json = []
        with self.make_session() as session:
            request_types = session.query(RequestType)\
                .filter(RequestType.devicetype == device_type)\
                .all()
            if len(request_types) is 0:
                request_types_json = []
            else:
                request_types_json = [d_t.serialize() for d_t in request_types]
        return {
            'status': 'OK',
            'code': 200,
            'device_types': request_types_json,
        }


class CredentialsHandler(RequestHandler, SessionMixin):
    def get(self):
        pass
