# Exit codes:
# -1: Unspecified error
# 0: All clear
# 1: Invalid argument
# 2: Connection error
# 3: Chunk upload unsuccessful

import json, requests, sys

sys.path.append("..")

from common.common import log, countdown

def get_consts(token_path):
	raw = json.load(open(token_path, "rb"))
	API_KEY = raw["tokens"]["telegram"]["http_api_key"]
	
	IMG_SEND_ENDPOINT = f"https://api.telegram.org/bot{API_KEY}/sendPhoto"
	TIMEOUT = 60
	
	return {
		"IMG_SEND_ENDPOINT" : IMG_SEND_ENDPOINT,
		"TIMEOUT"           : TIMEOUT
	}

def post(path, caption, token_path, n=1):
	consts = get_consts(token_path)
	
	params = {
		"chat_id" : "@LainBot13",
		"caption" : caption
	}
	
	files = {
		"photo" : open(path, "rb")
	}

	queue = []
	
	try:
		r = requests.post(consts["IMG_SEND_ENDPOINT"], files=files, data=params, timeout=consts["TIMEOUT"])
		log(f"Received code {r.status_code}.")
		if r.status_code != 200: log(f"{json.dumps(r.json(), sort_keys=True, indent=8)}")
		else: log(f"OK? {json.dumps(r.json()['ok'], sort_keys=True, indent=8)}")
		print()
	except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):	
		log(f"Connection Error! Could not upload frame {path} to Telegram!")
		log(f"Trying again in {n} seconds. (Press any button to try again now.)", flush=True)
		countdown(n)
		print()
		post(path, caption, token_path, n=n*2)