import glob
import importlib
import logging
import os
from typing import Union

import boto3
import youtube_dl
from youtube_dl.utils import DownloadError


settings = importlib.import_module("app.settings.{}".format(os.getenv("ENV", "dev")))
logger = logging.getLogger(__name__)


def download_video(url: str) -> Union[None, str]:
    """download video

    :param url:             video url
    :return:                video title, none otherwise
    """
    video_title = None
    info_dict = dict()
    ydl_opts = {"outtmpl": f"{settings.UPLOAD_PATH}%(id)s.%(ext)s", "noplaylist": True}

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
    except DownloadError as e:
        logger.error(f"DownloadError: {e}")
    except Exception as e:
        logger.error(f"Exception: {e}")
    else:
        id_ = info_dict.get("id")
        ext = info_dict.get("ext")

        if id_ and ext and os.path.exists(f"{settings.UPLOAD_PATH}{id_}.{ext}"):
            video_title = f"{id_}.{ext}"

    return video_title


def upload_to_spaces(file_name: str) -> None:
    """upload video file to spaces

    :param file_name:           file name used for key
    :return:                    Nothing
    """
    if not all(
        [
            settings.SPACES_ACCESS_KEY_ID,
            settings.SPACES_SECRET_ACCESS_KEY,
            settings.SPACES_REGION_NAME,
            settings.SPACES_BUCKET_NAME,
        ]
    ):
        logger.warning("Please check settings for SPACES_* vars.")
        return

    # Initialize a session using DigitalOcean Spaces.
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=settings.SPACES_REGION_NAME,
        endpoint_url=f"https://{settings.SPACES_REGION_NAME}.digitaloceanspaces.com",
        aws_access_key_id=settings.SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SPACES_SECRET_ACCESS_KEY,
    )

    client.upload_file(
        Bucket=settings.SPACES_BUCKET_NAME,
        Key=file_name,
        Filename=f"{settings.UPLOAD_PATH}{file_name}",
        ExtraArgs={"ACL": "public-read"},
    )


def tmp_folder_clean_up() -> None:
    """remove downloaded videos from @UPLOAD_PATH
    :return:            nothing
    """
    path = f"{settings.UPLOAD_PATH}*"
    files = glob.glob(path)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            err_msg = f"Error: {f} : {e.strerror}"
            logger.error(err_msg)
