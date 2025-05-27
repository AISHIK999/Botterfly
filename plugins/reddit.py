from os import remove
import asyncio
import asyncpraw
import aiohttp
import aiofiles
import random
import os
from urllib.parse import urlparse
from telethon import events
from plugins.commands import reddit
from userbot import botterfly


CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
USER_AGENT = os.environ["REDDIT_USER_AGENT"]

SUBREDDITS = [
    "EarthPorn",
    "spaceporn",
    "animegifs",
    "perfectloops",
    "Cinemagraphs",
    "WeatherGifs",
    "NatureIsFuckingLit",
    "oddlysatisfying",
    "interestingasfuck",
    "BeAmazed",
    "nextfuckinglevel",
    "Damnthatsinteresting",
    "mildlyinteresting",
    "pics",
    "gifs",
    "videos",
    "dankmemes",
    "memes",
    "aww",
    "cats",
]


def is_supported_media(url):
    if not url:
        return False

    supported_domains = [
        "imgur.com",
        "i.imgur.com",
        "i.redd.it",
        "v.redd.it",
        "gfycat.com",
        "redgifs.com",
        "giphy.com",
        "streamable.com",
    ]

    parsed_url = urlparse(url.lower())
    domain = parsed_url.netloc.lower()

    if any(site in domain for site in supported_domains):
        return True

    path = parsed_url.path.lower()
    media_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
        ".bmp",
        ".mp4",
        ".webm",
        ".mov",
    ]
    if any(path.endswith(ext) for ext in media_extensions):
        return True

    return False


def process_imgur_url(url):
    if "imgur.com" in url and not url.endswith(
        (".jpg", ".jpeg", ".png", ".gif", ".webp")
    ):
        if "/a/" in url or "/gallery/" in url:
            return None
        img_id = url.split("/")[-1].split(".")[0]
        return f"https://i.imgur.com/{img_id}.jpg"
    return url


def get_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    if "." in path:
        extension = path.split(".")[-1].lower()
    else:
        extension = "jpg"
    return f"reddit_media_{random.randint(1000, 9999)}.{extension}"


async def download_file(url, filename):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    async with aiofiles.open(filename, "wb") as f:
                        async for chunk in response.content.iter_chunked(8192):
                            await f.write(chunk)
                    return True
    except Exception:
        pass
    return False


async def get_reddit_media():
    try:
        reddit = asyncpraw.Reddit(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT
        )

        for attempt in range(3):
            chosen_subreddit = random.choice(SUBREDDITS)
            subreddit = await reddit.subreddit(chosen_subreddit)

            posts = []
            for time_filter in ["week", "month", "all"]:
                async for post in subreddit.top(time_filter=time_filter, limit=500):
                    if not post.stickied and post.url:
                        posts.append(post)
                if posts:
                    break

            if posts:
                random.shuffle(posts)
                for post in posts[:10]:
                    media_url = post.url

                    if hasattr(post, "is_video") and post.is_video:
                        if hasattr(post, "media") and post.media:
                            reddit_video = post.media.get("reddit_video")
                            if reddit_video:
                                media_url = reddit_video.get("fallback_url")

                    if "imgur.com" in media_url:
                        processed = process_imgur_url(media_url)
                        if processed:
                            media_url = processed

                    if media_url and is_supported_media(media_url):
                        await reddit.close()
                        return media_url, post.title

        await reddit.close()

    except Exception as e:
        return f"ERROR: {str(e)}", None

    return None, None


async def reddit_media_with_retry(event, status_msg, attempt=1, max_attempts=10):
    if attempt > max_attempts:
        await status_msg.edit(
            f"`Failed after {max_attempts} attempts. Try again later.`"
        )
        return

    if attempt > 1:
        await status_msg.edit(f"`Attempt {attempt}/{max_attempts} - Fetching...`")

    media_url, post_title = await get_reddit_media()

    if not media_url:
        await asyncio.sleep(1)
        return await reddit_media_with_retry(
            event, status_msg, attempt + 1, max_attempts
        )

    if media_url.startswith("ERROR:"):
        await status_msg.edit(f"`{media_url}`")
        return

    await status_msg.edit(f"`Downloading... (attempt {attempt})`")

    filename = get_filename(media_url)
    success = await download_file(media_url, filename)

    if not success:
        await asyncio.sleep(1)
        return await reddit_media_with_retry(
            event, status_msg, attempt + 1, max_attempts
        )

    await status_msg.edit("`Sending...`")

    try:
        await event.client.send_file(event.chat_id, filename, caption=post_title[:200])
        await status_msg.delete()

        is_owner = event.sender_id == (await event.client.get_me()).id
        if not is_owner:
            await event.delete()

        remove(filename)
        return

    except Exception:
        if os.path.exists(filename):
            remove(filename)

        await asyncio.sleep(1)
        return await reddit_media_with_retry(
            event, status_msg, attempt + 1, max_attempts
        )


@botterfly.on(events.NewMessage(**reddit))
async def reddit_media(event):
    is_owner = event.sender_id == (await event.client.get_me()).id

    if is_owner:
        status_msg = await event.edit("`Fetching random Reddit media...`")
    else:
        status_msg = await event.reply("`Fetching random Reddit media...`")

    await reddit_media_with_retry(event, status_msg)
