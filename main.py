import schedule
import time
import requests
import json

NEWRL_PATH = '/Users/kousthub/projects/asqisys/newrl/data_mainnet'
CALL_BACK_URL = 'https://webhook.site/f3b36505-06a5-4c14-8477-ea8d93537c02'

def scan_blocks():
    with open('last_scanned_block.txt','r') as fd:
        last_scanned_block = fd.read()
        last_scanned_block = int(last_scanned_block)
        print(last_scanned_block)

    try:
        with open(f'{NEWRL_PATH}/archive/block_{last_scanned_block}.json') as fp:
            block = json.load(fp)
            for transaction in block['text']['transactions']:
                print(transaction)
                requests.post(CALL_BACK_URL, json=transaction)

        with open('last_scanned_block.txt','w') as fd:
            last_scanned_block += 1
            fd.write(f'{last_scanned_block}')
    except Exception as e:
        print('Block does not exist. Waiting...')

schedule.every(1).seconds.do(scan_blocks)

while 1:
   schedule.run_pending()
   time.sleep(1)