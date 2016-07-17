import requests
import logging
import sys

from proto import request_pb2, response_pb2, pokemon_pb2
import api
import location

API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'

class PogoSession(object):
    def __init__(self, session, authProvider, accessToken, loc):
        self.session = session
        self.authProvider = authProvider
        self.accessToken = accessToken
        self.location = loc
        self.endpoint = None
        self.endpoint = 'https://' + self.createApiEndpoint() + '/rpc'

    def __str__(self):
        s = 'Access Token: {}\nEndpoint: {}\nLocation: {}'.format(self.accessToken,
                self.endpoint, self.location)
        return s

    def setLocation(self, loc):
        self.location = loc
        
    def createApiEndpoint(self):
        payload = []
        msg = request_pb2.Request.Payload()
        msg.type = request_pb2.Request.Payload.Type.Value('REQUEST_ENDPOINT')
        payload.append(msg)
        req = self.wrapInRequest(payload);
        res = self.request(req, API_URL)
        if res is None:
            logging.critical('Servers seem to be busy. Exiting.')
            sys.exit(-1)
        return res.endpoint
        

    def wrapInRequest(self, payload):
        req = request_pb2.Request()
        req.payload.extend(payload)
        req.type = request_pb2.Request.Type.Value('TWO')
        req.rpc_id = api.getRPCId()

        req.latitude, req.longitude, req.altitude = location.encodeLocation(self.location)

        req.unknown12 = 18446744071615

        req.auth.provider = self.authProvider
        req.auth.token.contents = self.accessToken
        req.auth.token.unknown13 = 59

        return req

    def requestOrThrow(self, req, url=None):
        if url is None:
            url = self.endpoint
        rawResponse = self.session.post(url, data=req.SerializeToString())
        response = response_pb2.Response()
        response.ParseFromString(rawResponse.content)
        return response

    def request(self, req, url=None):
        try:
            return self.requestOrThrow(req, url)
        except Exception, e:
            logging.error(e)
            return None
        
    def wrapAndRequest(self, payload):
        res = self.request(self.wrapInRequest(payload))
        if res is None:
            logging.critical('Servers seem to be busy. Exiting.')
            sys.exit(-1)
        logging.debug('{} payloads'.format(len(res.payload)))
        return res

    def getProfile(self):
        msg = request_pb2.Request.Payload()
        msg.type = request_pb2.Request.Payload.Type.Value('REQUEST_ENDPOINT')
        payload = [msg]
        res = self.wrapAndRequest(payload)
        profile = pokemon_pb2.ClientProfile().ParseFromString(res.payload[0].data)
        return profile