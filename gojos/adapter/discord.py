from discord_webhook import DiscordWebhook, DiscordEmbed
from pathlib import Path

from gojos.util import env


def send_basic_text(message_text):
    hook = DiscordWebhook(url=_channel_url(), content=message_text)
    hook.execute()
    pass


def send_attachment(msg_title: str, description: str, file_path: Path, file_name: str, as_attachment: bool = False):
    hook = DiscordWebhook(url=_channel_url())
    with open(file_path, "rb") as f:
        hook.add_file(file=f.read(), filename=file_name)

    if as_attachment:
        return _as_attachment(hook, msg_title, description, file_name)
    _as_embedded(hook)


def _as_attachment(hook, msg_title: str, description: str, file_name: str):
    embed = DiscordEmbed(title=msg_title, description=description, color='03b2f8')
    embed.set_thumbnail(url=f"attachment://{file_name}")

    hook.add_embed(embed)
    hook.execute()


def _as_embedded(hook):
    hook.execute()


def _channel_url():
    return env.Env().discord_channel_url()
