import json
import click
import ayrsharehelper as ah


#@click.group(invoke_without_command=True)
# @click.argument("task_id", nargs=1)
@click.group
@click.pass_context
def cli(ctx):
    """
    Ayrshare debugging cli.  Invoke help on one of the 
    commands below.
    """
    pass


@cli.command
@click.pass_context
@click.option(
    "--status-filter",
    "-s",
    type=click.Choice(
        ["all", "success", "error", "processing", "pending", "deleted", "awaiting"],
    ),
    default="all",
    help="Apply a filter by status category to the history API call"
)
@click.option(
    "--platform-filter",
    "-p",
    type=click.Choice(["all", "linkedin", "twitter", "linkedin", "youtube"]),
    default="all",
    help="Filter results to a specific platform only"
)
@click.option(
    "--ayr_socialpost_id",
    "-i",
    type=str,
    default=None,
    help="Query a specific social post by id.")
@click.option("--no-indent", is_flag=True)
@click.option(
    "--display",
    "-d",
     type=click.Choice(["all", "id", "id-status"]),
     default="all",
     help="Change command output from entire json to other choices"
)
def history(ctx, status_filter, platform_filter, ayr_socialpost_id, no_indent, display):

    if status_filter == "all":
        status_filter = None

    if platform_filter == "all":
        platform_filter = None

    if no_indent:
        indent = None
    else:
        indent = 2

    for item in ah.history(status_filter, platform_filter, ayr_socialpost_id):
        if display == "all":
            click.echo(json.dumps(item, indent=indent, sort_keys=True))
        elif display == "id":
            click.echo(item["id"])
        elif display == "id-status":
            click.echo(f"{item['id']} {item['status']}")
        else:
            raise NotImplementedError(
                f"missing implementation for display value {display}"
            )
