import json
import click
import ayrsharehelper as ah


@click.group(invoke_without_command=True)
# @click.argument("task_id", nargs=1)
@click.pass_context
def cli(ctx):
    """
    Ayrshare debugging cli
    """
    # task = clickuphelper.Task(task_id, verbose=False)
    # ctx.obj = task

    # if ctx.invoked_subcommand is None:
    #    click.echo(json.dumps(task.task, indent=2))
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
)
@click.option(
    "--platform-filter",
    "-p",
    type=click.Choice(["all", "linkedin", "twitter", "linkedin", "youtube"]),
    default="all",
)
@click.option("--ayr_socialpost_id", "-i", type=str, default=None)
@click.option("--no-indent", is_flag=True)
@click.option(
    "-d", "--display", type=click.Choice(["all", "id", "id-status"]), default="all"
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
