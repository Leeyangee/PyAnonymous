
# ReadableCryptoMiner

*The project is to write a fully functionnal XMR miner, in pure python 3.*

Why? Such a Monero CPU miner can be useful for for learning purpose.

The source-code provided is heavily inspired by:
https://github.com/ricmoo/nightminer/ but I plan to use JSON RPC 2.0 and the
new RandomX algorithm.

**Warning 1:**
Initially Monero used the so-called CryptoNight PoW algorithm. The project was designed
accordingly.
But (as far as I know) from year 2019, November 30th monero uses the PoW algorithm:
RandomX.
The current miner needs to be patched in order to mine accordingly to the hard fork that
occured. By now (2024, March) this is still a work-in-progress.

**Warning 2:**
This miner is extremely slow and therefore not suited for mercantile use.



## Command Line Interface

    ggminer.py [-h] [-a {cryptonight}] [-o URL] [-u USERNAME] [-p PASSWORD] [-t THREAD] [-d DEBUG]

    optional arguments:
      -h, --help                       show this help message and exit
      -a, --algo                       hashing algorithm to use for proof of work {cryptonight}
      -o URL, --url URL                stratum mining server url (eg: stratum+tcp://foobar.com:3333)
      -u USERNAME, --user USERNAME     username for mining server
      -p PASSWORD, --pass PASSWORD     password for mining server
      -t THREAD, --thread THREAD       number of mining threads to start
      -d, --debug                      show extra debug information

Example of possible mining pools:

- Location	| Server  Host	| Stratum Port	| SSL/TLS Port
- Europe	xmr-eu1.nanopool.org	10300	10343
- Europe	xmr-eu2.nanopool.org	10300	10343
- US East	xmr-us-east1.nanopool.org	10300	10343
- US West	xmr-us-west1.nanopool.org	10300	10343
- Asia	xmr-asia1.nanopool.org	10300	10343
- Japan	xmr-jp1.nanopool.org	10300	10343
- Australia	xmr-au1.nanopool.org	10300	10343

Using a SSL connection is highly recommended. It's
more safe and stable than stratum.

## Dive in head first

To get started easily you can, for example, use the command line:
```shell
python ggminer.py --url stratum+tcp://xmr-eu1.nanopool.org:10300 --debug 2
```

## Structure the config file:

```json
{
  "wallet": "YOUR_XMR_ADDRESS",
  "rigName": "YOUR_WORKER",
  "email": "YOUR_EMAIL"
}
```


## License

The code is licensed under MIT + LGPLv3, see LICENSE file for more info.
