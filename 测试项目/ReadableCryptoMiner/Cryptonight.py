import binascii  # TODO: move outside ?

from Job import Job
from crypto_primitives import slow_hash_lgplv3


c_pow = slow_hash_lgplv3.slow_hash_glue_func


# TODO: move into other file if another implementation is done
# Subscription state
class Subscription(object):
    """Encapsulates the Subscription state from the JSON-RPC2 server"""

    def __init__(self):
        self._id = None
        # self._difficulty = None
        # self._target = None
        self._worker_name = None
        self._mining_thread = None

    # Subclasses should override this
    def ProofOfWork(self, header):
        raise Exception('Do not use the Subscription class directly, subclass it')

    class StateException(Exception):
        pass

    @property
    def id(self):
        return self._id

    @property
    def worker_name(self):
        return self._worker_name

    # @property
    # def difficulty(self): return self._difficulty
    # @property
    # def target(self): return self._target

    def set_worker_name(self, worker_name):
        if self._worker_name:
            raise self.StateException('Already authenticated as %r (requesting %r)' % (self._username, username))
        self._worker_name = worker_name

    def set_subscription(self, subscription_id):
        if self._id is not None:
            raise self.StateException('Already subscribed')
        self._id = subscription_id

    def create_job(self, job_id, blob, target):
        """Creates a new Job object populated with all the goodness it needs to mine"""

        if self._id is None:
            raise self.StateException('Not subscribed')

        return Job(
            subscription_id=self.id,
            job_id=job_id,
            blob=blob,
            target=target,
            proof_of_work=self.ProofOfWork
        )

    def __str__(self):
        return '<Subscription id={}, worker_name={}>'.format(self.id, self.worker_name)


class SubscriptionCryptonight(Subscription):
    """Subscription for Cryptonight-based coins, like XMR (Monero)"""

    # overriden method
    def ProofOfWork(self, header):
        def cryptonight_proof_of_work(x):
            output = [None for k in range(32)]  # create a buffer (list type)
            intli_form_data = list(x)
            c_pow(output, intli_form_data, 76)  # 76 is the input buffer len
            binstr_form_output = bytes(output)
            outputhex = binascii.hexlify(binstr_form_output).decode()  # TODO: move outside?
            return outputhex

        return cryptonight_proof_of_work(header)
