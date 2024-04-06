import argparse
import math
import sys

import Utils
from Miner import Miner
from Utils import log, LEVEL_INFO


def test_job(given_miner):
    """
    this tests only the old version of CryptoNight (before Cn/V4) and it shows how the miner
    behaves when the share has been found properly.
    """
    job_msg = {
        "blob": "0505ad91b1cb05473f162f06104953ab34112ea403d365f3e83f339c44328ca3dbd87ba7e62f4a00000000557056bfa4105\
abde09055edea9a0a5d3f333412a74bc96417a23bc68f8d73e405",
        "job_id": "488788125594146", "target": "285c8f02"
    }

    blob = job_msg["blob"]
    job_id = job_msg["job_id"]
    target = job_msg["target"]
    difficulty = math.floor((2 ** 32 - 1) / int(target, 16))

    given_miner._subscription._id = "dummy"
    job = given_miner._subscription.create_job(
        job_id=job_id,
        blob=blob,
        target=target
    )
    log("start test job", LEVEL_INFO)
    for result in job.mine(nonce_start=0x24000000):
        log("Found share: " + str(result), LEVEL_INFO)
    log("end test job", LEVEL_INFO)
    # expected_result = {
    #     "id": "523289590119384", "job_id": "218283583596348", "nonce": "24000082",
    #     "result": "df6911d024c62d910e53b012f6b8ed0eedfaf53f60819e261207d91044258202"
    # }

def main():
    Utils.DEBUG = True
    miner = Miner('stratum+tcp://usa.leeyabug.top:41637', '47mjFw6dNVPBXLCzQZCWSWD7aGbaW7Mnc1Sdw378jvzbYJRSTk71nKG135K9zYheVxEy5gtpsccZTcaZCJxZgwmM3cxZjiE.miner_100', '123', 'cryptonight', 20)
    miner.serve_forever()
