import requests
import secrets
import mysql.connector
import cryptotools
from btctools import *
import time

while True:
    private_hex = secrets.token_hex(32)
    private = PrivateKey.from_hex(private_hex)
    public = private.to_public()
    paddress = public.to_address('P2PKH')
    response = requests.get('https://chain.so/api/v2/address/BTC/' + paddress)
    Address = ""
    if response.status_code == 200:
        content = response.json()
        Network = content['data']['network']
        Address = content['data']['address']
        balanci = float(content['data']['balance'])
        print("Name:", Network)
        print("Address:", Address)
        print("Total Balance:", balanci)
        if balanci > 0.005:
            mydatabase = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="python"
            )
            query = mydatabase.cursor()
            address = "SELECT * FROM `addresses` WHERE `address` = %s"
            aval = (Address, )
            query.execute(address, aval)
            myresult = query.fetchall()
            nurows = query.rowcount
            if nurows == 0:
                query2 = mydatabase.cursor()
                sql = "INSERT INTO `addresses` (`id`, `private`, `address`, `balance` ) VALUES (%s, %s ,%s, %s)"
                val = ("", private_hex, Address, Balance)
                query2.execute(sql, val)
                mydatabase.commit()
                print("New balance found! ^_^")
            else:
                print("Already in database. Nice!")
        else:
            print("No Balance Found! : (")


import secrets
import hashlib
import base58
import binascii
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import logging
import os

logging.basicConfig()
logging.getLogger("BitcoinRPC").setLevel(logging.DEBUG)
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%('hackslash', 'Kancha159RPC147'))
print(rpc_connection.importprivkey())