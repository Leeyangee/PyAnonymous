import math
import socket
import threading
from Cryptonight import SubscriptionCryptonight
from JsonRpc2Client import *
import defs


SubscriptionByAlgorithm = {
    "cryptonight": SubscriptionCryptonight,
}


class Miner(JsonRpc2Client):
    """Simple mining client"""

    class MinerWarning(JsonRpc2Client.RequestReplyWarning):
        def __init__(self, message, reply, request=None):
            JsonRpc2Client.RequestReplyWarning.__init__(self, 'Mining Sate Error: ' + message, reply, request)

    class MinerAuthenticationException(JsonRpc2Client.RequestReplyException):
        pass

    def __init__(self, url, username, password, algorithm, nb_threads):
        JsonRpc2Client.__init__(self)
        self._url = url
        self._username = username
        self._password = password
        self.nb_threads = nb_threads
        self._subscription = SubscriptionByAlgorithm[algorithm]()
        self._job = None
        self._submitted_shares = 0
        self._accepted_shares = 0

    def handle_reply(self, request, reply):
        if reply.get("method") == "job":
            self._handle_job(reply)
        elif request:
            if request.get("method") == "submit":
                self._handle_submit(reply, request)
            elif request.get("method") == "login":
                self._handle_login(reply)
            else:
                raise Exception("Bad message state - no request", reply)
        else:
            raise Exception("Unknown message", reply, request)

    def _handle_job_msg(self, job_msg):
        blob = job_msg["blob"]
        job_id = job_msg["job_id"]
        target = job_msg["target"]
        target = "".join([target[i:i + 2] for i in range(0, len(target), 2)][::-1])
        difficulty = math.floor((2 ** 32 - 1) / int(target, 16))
        self._spawn_job_thread(job_id, blob, target)

        log("New job: job_id={} - difficulty={}".format(job_id, difficulty), LEVEL_DEBUG)

    @staticmethod
    def _testif_job_msg_matches_spec(given_jobmsg):
        if "params" not in given_jobmsg:
            return False
        params = given_jobmsg["params"]
        for exp_key in ("blob", "job_id", "target", "height", "seed_hash"):
            if exp_key not in params:
                return False
        return True

    def _handle_job(self, reply):
        if not Miner._testif_job_msg_matches_spec(reply):
            raise self.MinerWarning("Malformed job message", reply)
        self._handle_job_msg(reply["params"])

    def _handle_submit(self, reply, request):
        if "result" not in reply or not reply["result"]:
            log("Share - Invalid", LEVEL_INFO)
            raise self.MinerWarning("Failed to accept submit", reply, request)

        self._accepted_shares += 1
        log("Accepted shares: {} / {}".format(self._accepted_shares, self._submitted_shares), LEVEL_INFO)

    def _login(self):
        # TODO: define user agent properly
        params = {"login": self._username, "pass": self._password, "agent": defs.AGENT_LABEL}
        self.send(method="login", params=params)

    def _handle_login(self, reply):
        if "result" not in reply or "id" not in reply["result"]:
            raise self.MinerWarning('Reply to login is malformed', reply)
        result = reply["result"]
        identifier = result["id"]
        log("Login success. Subscription ID={}".format(identifier), LEVEL_DEBUG)
        self._subscription.set_subscription(identifier)
        self._handle_job_msg(result["job"])

    def _spawn_job_thread(self, job_id, blob, target):
        """Stops any previous job and begins a new job."""

        # Stop the old job (if any)
        if self._job:
            self._job.stop()

        # Create the new job
        self._job = self._subscription.create_job(
            job_id=job_id,
            blob=blob,
            target=target
        )

        def run(job, nonce_start, nonce_stride):
            # try:
            for result in job.mine(nonce_start=nonce_start, nonce_stride=nonce_stride):
                self.send(method="submit", params=result)
                self._submitted_shares += 1
                log("Found share: " + str(result), LEVEL_DEBUG)
                log("Hashrate: {}".format(human_readable_hashrate(job.hashrate)), LEVEL_INFO)

        # except Exception as e:
        # log("ERROR: {}".format(e), LEVEL_ERROR)
        for n in range(self.nb_threads):
            thread = threading.Thread(target=run, args=(self._job, n, self.nb_threads))
            thread.daemon = True
            thread.start()

    def serve_forever(self) -> None:
        """
        quick 'n' dirty url parsing
        The assumed format for field self._url
        is:
        stratum+tcp://foobar.com:3333
        """
        tmp = self._url.split('//')[1]
        hostname, port = tmp.split(':')
        port = int(port)  # type casting
        log("Starting server on {}:{}".format(hostname, port), LEVEL_INFO)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        self.connect(sock)
        self._login()
        while True:
            time.sleep(10)
