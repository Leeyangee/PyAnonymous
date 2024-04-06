import time, struct, binascii, array


class Job(object):
    """Job from pool"""

    def __init__(self, subscription_id, job_id, blob, target, proof_of_work):

        # From job
        self._subscription_id = subscription_id
        self._job_id = job_id
        self._blob = blob
        self._target = target

        # PoW algorithm
        self._proof_of_work = proof_of_work

        # Flag to stop this job's mine coroutine
        self._done = False

        # Hash metrics (start time, delta time, total hashes)
        self._dt = 0.0
        self._hash_count = 0

    @property
    def job_id(self):
        return self._job_id

    @property
    def blob(self):
        return self._blob

    @property
    def target(self):
        return self._target

    @property
    def pow(self):
        return self._proof_of_work

    @property
    def hashrate(self):
        return self._hash_count / self._dt if self._dt > 0 else 0.0

    def stop(self):
        """Requests the mine coroutine stop after its current iteration"""
        self._done = True

    def mine(self, nonce_start=0, nonce_stride=13):
        t0 = time.time()

        blob_bin = binascii.unhexlify(self.blob)
        for nonce in range(nonce_start, 0x7fffffff, nonce_stride):
            if self._done:
                self._dt = time.time() - t0
                raise StopIteration()

            # PoW attempt
            nonce_bin = struct.pack('>I', nonce)
            data = blob_bin[:39] + nonce_bin + blob_bin[39 + len(nonce_bin):]
            pow = self.pow(data)

            tar = pow[-len(self.target):]
            tar = "".join([tar[i:i + 2] for i in range(0, len(tar), 2)][::-1])

            if tar <= self.target:
                result = {"id": self._subscription_id, "job_id": self._job_id, "nonce": "{0:0{1}x}".format(nonce, 8),
                          "result": pow}
                self._dt = time.time() - t0
                yield result
            self._hash_count += 1
