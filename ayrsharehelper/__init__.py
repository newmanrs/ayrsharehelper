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
        # Ayrshare is fond of returnign status_code 400 for error, but then an actual
        # error message with a 2xx code...
        msg = f"status_code: {res.status_code}\nurl: {res.url}\n, res.text={res.text}"
        raise requests.exceptions.HTTPError(msg) from e

    return res.json()


def history(status=None, platform=None, ayr_id=None, display="full", lastRecords=500):

    # Statuses ["success", "error", "processing", "pending", "deleted", "awaiting"]
    params = {'lastDays' : 0, 'lastRecords': lastRecords}
    if status is not None:
        params["status"] = status

    if ayr_id is not None:
        if platform is not None:
            raise ValueError("one of platform or ayr_id must be specified as None")

    url = "https://app.ayrshare.com/api/history"
    if ayr_id:
        url += f"/{ayr_id}"  # Responses are significantly different format
        res = rg(url, params=params, headers=headers)
        return [res]
    else:
        out = []
        res = rg(url, params=params, headers=headers)
        for item in res:
            # Filter
            if platform is None or platform in item["platforms"]:
                out.append(item)
        return out
