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
    '--platform-filter',
    '-p',
    type=click.Choice(
        ["all", 'linkedin', 'twitter', 'linkedin']
        ),
    default = "all"
    )
def history(ctx, status_filter, platform_filter):

    if status_filter == "all":
        status_filter = None
    if platform_filter == "all":
        platform_filter == None

    for item in ah.history(status_filter, platform_filter):
        click.echo(json.dumps(item,indent=2))
