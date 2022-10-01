import random
import os
import praw
from telethon import events
from userbot import templar
from plugins.commands import red

# Send a random meme from the listed subreddits

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     username=os.environ['REDDIT_USERNAME'],
                     password=os.environ['REDDIT_PASSWORD'],
                     user_agent="this is useless")

# Add subs as you wish
subs = ["memes", "dankmemes", "me_irl", "meirl", "2meirl4meirl", "AdviceAnimals", "MemeEconomy", "memeeconomy", "wholesomememes", "dankchristianmemes", "terriblefacebookmemes"]


@templar.on(events.NewMessage(**red))
async def red(event):
    submission = ""
    await event.edit("`Wait a moment my Lord, while I find a meme for you...`")
    memes_submissions = reddit.subreddit(random.choice(subs)).hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)
    image_url = submission.url
    try:
        await event.client.send_file(event.chat_id, image_url, caption=submission.title)
    except Exception:
        await event.edit("`Our troops met an unhandled exception during meme acquisition`")
