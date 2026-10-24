from API.utils.vault_client import VaultClient

client = VaultClient()

JIRA_TOKEN = {
    'Authorization': 'Bearer ' + client.get_creds("main")["jira_token"],
    "Content-Type": "application/json"
}

# mailhog cookie
MAILHOG_COOKIE = client.get_creds("main")["mailhog_cookie"]

mailhog_headers = {
    'accept': 'application/json',
    'Authorization': MAILHOG_COOKIE
}
