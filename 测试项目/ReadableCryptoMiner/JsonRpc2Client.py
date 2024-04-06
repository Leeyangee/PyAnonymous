import threading, json, sys
from Utils import *

class JsonRpc2Client(object):
	"""Simple Json RPC Client"""

	class ClientException(Exception): pass

	class RequestReplyException(Exception):
		def __init__(self, message, reply, request = None):
			Exception.__init__(self, message)
			self._reply = reply
			self._request = request
			self.message = message

		@property
		def request(self): return self._request
		@property
		def reply(self): return self._reply


	class RequestReplyWarning(RequestReplyException):
		'''Sub-classes can raise this to inform the user of JSON-RPC server issues.'''
		pass


	def __init__(self):
		self._socket = None
		self._lock = threading.RLock()
		self._rpc_thread = None
		self._message_id = 1
		self._requests = {}


	def _handle_incoming_rpc(self):
		data = ""
		while True:
			if '\n' in data:
				line, data = data.split('\n', 1)
			else:
				data += self._socket.recv(1024).decode()
				continue

			log('JSON-RPC Server > ' + line, LEVEL_PROTOCOL)

			try:
				reply = json.loads(line)
			except Exception as e:
				log("JSON-RPC Error: Failed to parse JSON %r (skipping)" % line, LEVEL_ERROR)
		
			try:
				request = None
				with self._lock:
					if 'id' in reply and reply['id'] in self._requests:
						request = self._requests[reply['id']]
					self.handle_reply(request, reply)
			except self.RequestReplyWarning as e:
				output = e.message
				if e.request:
					output += '\n  ' + str(e.request)
				output += '\n  ' + str(e.reply)
				log(output, LEVEL_ERROR)


	def handle_reply(self, request, reply):
		raise self.RequestReplyWarning('Override this method')


	def send(self, method, params):
		if not self._socket:
			raise Exception("Not connected")

		request = {"id": self._message_id, "method": method, "params": params}
		msg = json.dumps(request)
		log("Send request {}: {}".format(self._message_id, msg), LEVEL_DEBUG)
		with self._lock:
			self._requests[self._message_id] = request
			self._message_id += 1
			self._socket.send((msg + '\n').encode())


	def connect(self, socket):
		if self._rpc_thread:
			raise Exception("Already connected")

		self._socket = socket
		self._rpc_thread = threading.Thread(target=self._handle_incoming_rpc)
		self._rpc_thread.daemon = True
		self._rpc_thread.start()
