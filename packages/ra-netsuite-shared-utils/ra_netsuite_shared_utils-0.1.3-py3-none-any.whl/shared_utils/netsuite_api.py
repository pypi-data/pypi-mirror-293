import requests
import json
from netsuite_helper import get_auth_token, get_journal_request_url
from file_utils import record_posted_memo, has_memo_been_posted
from utils import DecimalEncoder

def post_journal_entry(memo, journal_items, journal_date, posting_period, env, consumer_key, consumer_secret, token_id, token_secret, realm):
    if has_memo_been_posted(memo):
        print(f"Skipping already posted journal entry: {memo}")
        return

    url = get_journal_request_url(env)

    items = [item.to_dict() for item in journal_items]

    payload = json.dumps({
      "subsidiary": 1,
      "currency": 1,
      "exchangerate": 1,
      "postingperiod": posting_period,
      "approvalstatus": 1,
      "memo": memo,
      "trandate": journal_date,
      "line": {
        "items": items
      }
    }, cls=DecimalEncoder)

    auth = get_auth_token(consumer_key, consumer_secret, token_id, token_secret, realm)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, auth=auth, headers=headers, data=payload)

    try:
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to post journal entry: {memo}, Error: {str(e)}")
        return "Error: " + str(e)

    print(f"Successfully posted journal entry: {memo}, Status Code: {response.status_code}")
    record_posted_memo(memo)

