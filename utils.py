from emoji import emojize

def get_emoji(emoji_name, fail_silently=False):
    alias = emoji_name if emoji_name[0] == emoji_name[-1] == ":" else f":{emoji_name}:"
    the_emoji = emojize(alias, use_aliases=True)
    if the_emoji == alias and not fail_silently:
        raise ValueError(f"Emoji {alias} not found!")
    return the_emoji

def get_channel(client, value, attribute="name"):
    channel = next((c for c in client.get_all_channels() if getattr(c, attribute).lower() == value.lower()), None)
    if not channel:
        raise ValueError("No such channel")
    return channel
