"""Feed/timeline CLI commands."""

from __future__ import annotations

from typing import Annotated

import typer

from clix.cli.helpers import (
    get_client,
    is_compact_mode,
    is_json_mode,
    is_yaml_mode,
    output_compact,
    output_json,
    output_yaml,
    validate_output_flags,
)
from clix.display.formatter import format_tweet_list

feed_app = typer.Typer(no_args_is_help=False, invoke_without_command=True)


@feed_app.callback(invoke_without_command=True)
def feed(
    ctx: typer.Context,
    timeline_type: Annotated[
        str, typer.Option("--type", "-t", help="Timeline type: for-you, following")
    ] = "for-you",
    count: Annotated[int, typer.Option("--count", "-n", help="Number of tweets")] = 20,
    pages: Annotated[int, typer.Option("--pages", "-p", help="Number of pages to fetch")] = 1,
    filter_mode: Annotated[
        str | None, typer.Option("--filter", help="Filter: all, top, score")
    ] = None,
    top_n: Annotated[int, typer.Option("--top", help="Top N for filter mode")] = 10,
    threshold: Annotated[float, typer.Option("--threshold", help="Score threshold")] = 0.0,
    compact: Annotated[
        bool, typer.Option("--compact", "-c", help="Compact JSON output for AI agents")
    ] = False,
    full_text: Annotated[
        bool, typer.Option("--full-text", help="Show full tweet text without truncation")
    ] = False,
    json_output: Annotated[bool, typer.Option("--json", help="JSON output")] = False,
    yaml_output: Annotated[bool, typer.Option("--yaml", help="YAML output")] = False,
    account: Annotated[str | None, typer.Option(help="Account name")] = None,
):
    """Fetch your home timeline."""
    if ctx.invoked_subcommand is not None:
        return

    validate_output_flags(json_output, yaml_output)

    # Merge local flags with global ctx.obj flags
    ctx.ensure_object(dict)
    if compact:
        ctx.obj["compact"] = True
    if full_text:
        ctx.obj["full_text"] = True

    from clix.core.api import get_home_timeline
    from clix.utils.filter import filter_tweets

    all_tweets = []
    cursor = None

    with get_client(account) as client:
        for _ in range(pages):
            response = get_home_timeline(client, timeline_type, count, cursor)
            all_tweets.extend(response.tweets)
            cursor = response.cursor_bottom
            if not response.has_more:
                break

    if filter_mode:
        all_tweets = filter_tweets(all_tweets, mode=filter_mode, top_n=top_n, threshold=threshold)

    is_compact = is_compact_mode(ctx)
    if is_compact and json_output:
        raise typer.BadParameter("--compact and --json are mutually exclusive")

    if is_compact:
        output_compact(all_tweets)
    elif is_json_mode(json_output):
        output_json([t.to_json_dict() for t in all_tweets])
    elif is_yaml_mode(yaml_output):
        output_yaml([t.to_json_dict() for t in all_tweets])
    else:
        use_full_text = ctx.obj.get("full_text", False) if ctx.obj else False
        format_tweet_list(all_tweets, full_text=use_full_text)
