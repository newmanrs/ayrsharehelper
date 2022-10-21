import requests
import json
import os

if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is None:
    ayrkey = os.environ["AYRSHARE_API_KEY_AME"]
    headers = {"Authorization": f"Bearer {ayrkey}"}
else:
    raise NotImplementedError("AWS Lambda secrets not implemented yet")


def rg(*args, **kwargs):
    """
    requests_get with some minimum error handling
    """
    res = requests.get(*args, **kwargs)
    try:
        res.raise_for_status()  # We probably ought to customize more than this
    except requests.exceptions.HTTPError as e:
        msg = f"status_code: {res.status_code}\nurl: {res.url}\n, res.text={res.text}"
        raise requests.exceptions.HTTPError(msg) from e

    return res.json()


def hello_world():
    return "hello_world"


def history(status=None, platform=None):

    # Statuses ["success", "error", "processing", "pending", "deleted", "awaiting"]

    params = {}
    if status is not None:
        params["status"] = status

    res = rg("https://app.ayrshare.com/api/history", params=params, headers=headers)

    out=[]
    for item in res:
        #print(platform)
        if platform is None or platform in item['platforms']:
            out.append(item)

    return out
