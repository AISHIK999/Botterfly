from telethon import events

from plugins.commands import help, trigger
from plugins.utils import get_command_registry, safe_handler
from userbot import botterfly

COMMAND_NAME = "help"
tr = trigger[-1]


@botterfly.on(events.NewMessage(**help))
@safe_handler
async def send_help(event):
    """
    Shows command help. With no argument, lists every command.
    With a command name as argument, shows just that command's help.

    USAGE:
    $help
    $help <command>
    """
    registry = get_command_registry()

    parts = event.message.message.split(maxsplit=1)
    requested = parts[1].strip().lstrip(tr) if len(parts) > 1 else None

    if requested:
        doc = registry.get(requested)
        if not doc:
            await event.edit(f"`No such command: {tr}{requested}`")
            return
        await event.edit(f"`{tr}{requested}`:\n{doc}")
        return

    sections = [f"`{tr}{name}`:\n{doc}" for name, doc in sorted(registry.items())]
    help_text = "Available commands:\n\n" + "\n\n".join(sections)

    await event.edit("User manual has been forwarded to 'Saved Messages'")
    await event.client.send_message("me", help_text)
