# TweetClaw OpenClaw Companion Workflows

clix is the primary tool when a user wants a local X/Twitter CLI or MCP server
that uses browser cookies, terminal output, JSON output, and direct account
state. Keep using clix for account-local commands, quick terminal checks,
scriptable JSON, and self-hosted MCP sessions.

[TweetClaw](https://github.com/Xquik-dev/tweetclaw) is an optional OpenClaw
companion when an agent workflow needs a managed plugin path for X/Twitter
automation. It is useful for search tweets, search tweet replies, scrape tweets
from search results, follower export, user lookup, media upload, media
download, direct messages, monitor tweets, webhooks, giveaway draws, and
approval-gated post tweets or post tweet replies.

## Install

Install TweetClaw in the OpenClaw environment, then keep clix available for
local CLI and MCP workflows:

```bash
openclaw plugins install @xquik/tweetclaw
uvx clix0 mcp
```

Configure any OpenClaw API keys in local OpenClaw plugin config or environment
variables. Do not paste keys, browser cookies, webhook secrets, or signing
material into prompts, issues, docs, or shared logs.

## When to Use Each Tool

Use clix when the workflow needs:

- Local browser-cookie auth.
- The same X account state as the user's browser.
- Terminal output, JSON, YAML, or compact output for scripts.
- A self-hosted MCP server backed by the user's own session.

Use TweetClaw beside clix when the workflow needs:

- OpenClaw plugin install and routing.
- Search tweets or search tweet replies from an agent workflow.
- Monitor tweets and send webhook results to another system.
- Export followers, inspect users, or collect reviewed tweet URLs.
- Approval-gated post tweets, post tweet replies, media upload, or DMs.

## Handoff Pattern

Keep handoffs explicit and reviewable. A good handoff from TweetClaw to clix is a
small record with tweet IDs or URLs, author handles, the query, the time window,
and the next action.

```json
{
  "source": "tweetclaw",
  "query": "openclaw launch",
  "time_window": "2026-06-06T00:00:00Z/2026-06-06T12:00:00Z",
  "results": [
    {
      "tweet_url": "https://x.com/example/status/1234567890",
      "author_handle": "example",
      "next_action": "summarize with clix tweet"
    }
  ]
}
```

The agent can then run clix on reviewed tweet URLs or IDs:

```bash
clix tweet 1234567890 --json
clix tweets 1234567890 2345678901 --compact
```

## Agent Guardrails

- Read with either tool without additional approval.
- Ask for explicit user approval before posting, replying, sending DMs, deleting
  tweets, following, unfollowing, blocking, muting, or scheduling posts.
- Store credentials only in local config, environment variables, or the user's
  approved secret store.
- Pass only reviewed tweet IDs, tweet URLs, handles, summaries, and task notes
  between tools.
- Prefer clix for account-local inspection and TweetClaw for OpenClaw-managed
  search, monitoring, and webhook workflows.
