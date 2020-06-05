import glob
import logging
import os
from typing import Union

import boto3
import youtube_dl
from youtube_dl.utils import DownloadError


logger = logging.getLogger(__name__)


def download_video(url: str) -> Union[None, str]:
    """download video

    :param url:             video url
    :return:                video title, none otherwise
    """
    video_title = None
    info_dict = dict()
    ydl_opts = {"outtmpl": "/tmp/videos/%(id)s.%(ext)s", "noplaylist": True}

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
        if id_ and ext and os.path.exists(f"{id_}.{ext}"):
            video_title = f"{id_}.{ext}"

    return video_title


def upload_to_spaces(file_name: str) -> None:
    """upload video file to spaces

    :param file_name:           file name used for key
    :return:                    Nothing
    """
    aws_access_key_id = os.getenv("SPACES_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("SPACES_SECRET_ACCESS_KEY")
    region_name = os.getenv("SPACES_REGION_NAME")
    bucket_name = os.getenv("SPACES_BUCKET_NAME")

    # Initialize a session using DigitalOcean Spaces.
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name=region_name,
        endpoint_url=f"https://{region_name}.digitaloceanspaces.com",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    client.upload_file(Bucket=bucket_name, Key=file_name, Filename=f"/code/{file_name}")


def tmp_folder_clean_up() -> None:
    """remove downloaded videos frpm /tmp/videos
    """
    files = glob.glob("/tmp/videos/*")
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            err_msg = f"Error: {f} : {e.strerror}"
            logger.error(err_msg)
