import json_duplicate_keys as jdks
import requests
import os


# Sending message notification to Discord
def toDiscord(bot_name, message, SidebarColor=0xcc0500, ConfigFile=None):
	if type(bot_name) != str: bot_name = ""

	if type(ConfigFile) == str and len(ConfigFile) > 0:
		NotifyConf = jdks.load(ConfigFile)
	else:
		if not os.path.isfile(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json")):
			if not os.path.isdir(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify")):
				os.makedirs(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify"))
			jdks.JSON_DUPLICATE_KEYS({
				"Discord": {
					"<BOT_NAME>": {
						"WEBHOOK-URL": "https://discord.com/api/webhooks/<WEBHOOK_ID>/<WEBHOOK_TOKEN>"
					}
				}
			}).dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		NotifyConf = jdks.load(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"))


	if NotifyConf:
		if NotifyConf.get("Discord") == "JSON_DUPLICATE_KEYS_ERROR" or type(NotifyConf.get("Discord")) != dict:
			NotifyConf.delete("Discord")
			NotifyConf.set("Discord", {"<BOT_NAME>": {"WEBHOOK-URL": "https://discord.com/api/webhooks/<WEBHOOK_ID>/<WEBHOOK_TOKEN>"}})
			NotifyConf.dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		WEBHOOK_URL = NotifyConf.get("Discord||"+bot_name+"||WEBHOOK-URL")
		if (type(message) == str and len(message) > 0) and (type(WEBHOOK_URL) == str and WEBHOOK_URL not in ["", "JSON_DUPLICATE_KEYS_ERROR"]):
			json_data = {"embeds": [{"description": message}]}
			if type(SidebarColor) == int:
				json_data["embeds"][0]["color"] = SidebarColor

			try:
				requests.post(WEBHOOK_URL, json=json_data)
			except Exception as e:
				print(e)



# Sending message notification to Telegram
def toTelegram(bot_name, message, MessageFormat=None, ConfigFile=None):
	if type(bot_name) != str: bot_name = ""

	if type(ConfigFile) == str and len(ConfigFile) > 0:
		NotifyConf = jdks.load(ConfigFile)
	else:
		if not os.path.isfile(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json")):
			if not os.path.isdir(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify")):
				os.makedirs(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify"))
			jdks.JSON_DUPLICATE_KEYS({
				"Telegram": {
					"<BOT_NAME>": {
						"BOT-TOKEN": "<BOT_TOKEN>",
						"CHANNEL-USERNAME": "<CHANNEL_USERNAME>"
					}
				}
			}).dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		NotifyConf = jdks.load(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"))


	if NotifyConf:
		if NotifyConf.get("Telegram") == "JSON_DUPLICATE_KEYS_ERROR" or type(NotifyConf.get("Telegram")) != dict:
			NotifyConf.delete("Telegram")
			NotifyConf.set("Telegram", {"<BOT_NAME>": {"BOT-TOKEN": "<BOT_TOKEN>", "CHANNEL-USERNAME": "<CHANNEL_USERNAME>"}})
			NotifyConf.dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		BOT_TOKEN = NotifyConf.get("Telegram||"+bot_name+"||BOT-TOKEN")
		CHANNEL_USERNAME = NotifyConf.get("Telegram||"+bot_name+"||CHANNEL-USERNAME")
		if (type(message) == str and len(message) > 0) and (type(BOT_TOKEN) == str and BOT_TOKEN not in ["", "JSON_DUPLICATE_KEYS_ERROR"]) and (type(CHANNEL_USERNAME) == str and CHANNEL_USERNAME not in ["", "JSON_DUPLICATE_KEYS_ERROR"]):
			try:
				requests.post("https://api.telegram.org/bot{BOT_TOKEN}/sendMessage".format(BOT_TOKEN=BOT_TOKEN),
					data = {
					"chat_id": CHANNEL_USERNAME,
					"text": message,
					"parse_mode": MessageFormat
				})
			except Exception as e:
				print(e)



# Sending message notification to Slack
def toSlack(bot_name, message, ConfigFile=None):
	if type(bot_name) != str: bot_name = ""

	if type(ConfigFile) == str and len(ConfigFile) > 0:
		NotifyConf = jdks.load(ConfigFile)
	else:
		if not os.path.isfile(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json")):
			if not os.path.isdir(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify")):
				os.makedirs(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify"))
			jdks.JSON_DUPLICATE_KEYS({
				"Slack": {
					"<BOT_NAME>": {
						"WEBHOOK-URL": "https://hooks.slack.com/services/<WORKSPACE_ID>/<CHANNEL_ID>/<TOKEN>"
					}
				}
			}).dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		NotifyConf = jdks.load(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"))


	if NotifyConf:
		if NotifyConf.get("Slack") == "JSON_DUPLICATE_KEYS_ERROR" or type(NotifyConf.get("Slack")) != dict:
			NotifyConf.delete("Slack")
			NotifyConf.set("Slack", {"<BOT_NAME>": {"WEBHOOK-URL": "https://hooks.slack.com/services/<WORKSPACE_ID>/<CHANNEL_ID>/<TOKEN>"}})
			NotifyConf.dump(os.path.join(os.path.expanduser("~"), ".TPConfig", "TP-sendNotify", "sendNotify.json"), indent=4)

		WEBHOOK_URL = NotifyConf.get("Slack||"+bot_name+"||WEBHOOK-URL")
		if (type(message) == str and len(message) > 0) and (type(WEBHOOK_URL) == str and WEBHOOK_URL not in ["", "JSON_DUPLICATE_KEYS_ERROR"]):
			json_data = {"text": message}

			try:
				requests.post(WEBHOOK_URL, json=json_data)
			except Exception as e:
				print(e)