[![TeleTok](logo.jpg?raw=true)](https://t.me/TeleTockerBot)

# [TeleTok](https://t.me/TeleTockerBot): Telegram bot for TikTok

## Description

This bot will send you a video from a TikTok. Pretty simple.

Just share a link to the chat (no need to mention the bot)

## Thanks to

Built on top of [aiogram](https://github.com/aiogram/aiogram)

# Installation

## Env

(*REQUIRED*)

- `API_TOKEN` - Bot token from BotFather

(*OPTIONAL*)

- `ALLOWED_IDS` - _JSON int list_. Gives access only to specific user/chat id (default: `[]` (empty list) = all
  users/chats)
- `REPLY_TO_MESSAGE` - _JSON Boolean_. Whether the bot should reply to source message or not (default: `true`)
- `WITH_CAPTIONS` - _JSON Boolean_. Whether the bot should include captions from TikTok in its message (default: `true`)
- `SIGNTOK_URL` - _JSON String_. A URL to a [SignTok](https://github.com/pablouser1/SignTok) service, which adds support
  for photos (default: ``)
- `DISABLE_NOTIFICATION` - _JSON Boolean_. Disabled send notification (default: `false`)

## Local

```bash
$ python3 -m venv venv
$ (venv) pip install .
$ (venv) echo "API_TOKEN=foo:bar" >> .env
$ (venv) export $(cat .env)
$ (venv) python app
```

## Docker

```bash
$ docker build -t teletok .
$ docker run -e "API_TOKEN=foo:bar" teletok
```

## Docker Compose

Create .env file

```bash
$ echo "API_TOKEN=foo:bar" >> .env
```

Build and start containers

```bash
$ docker compose up -d --build
```

# License

MIT
