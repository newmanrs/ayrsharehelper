# ayrsharehelper

Click CLI + python module for interacting with and debugging [ayrshare](https://www.ayrshare.com/) social media uploads to different platforms.  


## ash history

CLI for the [ayrshare history api](https://docs.ayrshare.com/rest-api/endpoints/history).

```
ash history --help
Usage: ash history [OPTIONS]

Options:
  -s, --status-filter [default|success|error|processing|scheduled|pending|deleted|awaiting]
                                  Apply a filter by status category to the
                                  history API call
  -p, --platform-filter [all|linkedin|twitter|linkedin|youtube]
                                  Filter results to a specific platform only
  -i, --ayr_socialpost_id TEXT    Query a specific social post by id.
  --no-indent
  -d, --display [all|id|id-status]
                                  Change command output from entire json to
                                  other choices
  --help                          Show this message and exit.
```

## ash analytics

CLI for the [ayrshare analytics api](https://docs.ayrshare.com/rest-api/endpoints/analytics).

```
ash analytics --help
Usage: ash analytics [OPTIONS]

  Statistics for a given post id

Options:
  -i, --post_id TEXT  Query a specific social post by id.
  --help              Show this message and exit.
```

## Usage examples

Filter history for uploads with status `-s success` , on platform `-p facebook`, and display `-d id` only.  This can then be fed into the analytics endpoint for each of these ids.
ash history -s success -d id -p facebook | xargs -n 1 ash analytics -i   
