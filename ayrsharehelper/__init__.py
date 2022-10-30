import requests
import json
import os


def config_headers():
    if os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is None:
        ayr_brand_account = os.environ.get("AYRSHARE_BRAND_ACCOUNT")
        key_var = "AYRSHARE_API_KEY"
        if ayr_brand_account is not None:
            key_var += "_" + ayr_brand_account

        ayrkey = os.environ[key_var]
        headers = {"Authorization": f"Bearer {ayrkey}"}
    else:
        ayrkey = None  # AWS_LAMBDA_FUNCTION_NAME must set these
        headers = None  # AWS_LAMBDA_FUNCTION_NAME must set these

    return headers


headers = config_headers()


def rg(*args, **kwargs):
    """
    requests_get with some minimum error handling
    """
    res = requests.get(*args, **kwargs)
    try:
        res.raise_for_status()  # We probably ought to customize more than this
    except requests.exceptions.HTTPError as e:
        # Ayrshare is fond of returning status_code 400 for error, but then an actual
        # error message with a 2xx code...
        msg = f"status_code: {res.status_code}\nurl: {res.url}\n, res.text={res.text}"
        raise requests.exceptions.HTTPError(msg) from e

    return res.json()


def history(status=None, platform=None, ayr_id=None, display="full", lastRecords=500):

    # Statuses ["success", "error", "processing", "pending", "deleted", "awaiting"]
    params = {"lastDays": 0, "lastRecords": lastRecords}
    if status is not None:
        params["status"] = status

    if ayr_id is not None:
        ayr_id = ayr_id.strip().rstrip(",")  # Strip whitespace, strip trailing commas
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


def delete_post(post_id):
    """
    Delete ayrshare post by id.
    """
    payload = {"id": post_id}
    # headers = {'Content-Type': 'application/json',

    r = requests.delete(
        "https://app.ayrshare.com/api/post", json=payload, headers=headers
    )

    return r.json()


def analytics_platforms():

    payload = {
        "platforms": [
            "facebook",
            # "instagram",
            "twitter",
            "linkedin",
            # "pinterest",
            "youtube",
            # "tiktok",
        ]
    }

    r = requests.post(
        "https://app.ayrshare.com/api/analytics/social", json=payload, headers=headers
    )

    return r.json()


def analytics_post(post_id):
    payload = {
        "id": post_id,
        "platforms": [
            "facebook",
            "instagram",
            "twitter",
            "youtube",
            "tiktok",
            "linkedin",
            "pinterest",
        ],
    }

    r = requests.post(
        "https://app.ayrshare.com/api/analytics/post", json=payload, headers=headers
    )

    return r.json()
