"""
Helper functions.
"""

import subprocess


def needs_change(destination, dependencies):
    """
    Checks if the destination file is older than its dependencies.
    """
    last_dependency_change = 0
    for dependency in dependencies:
        if dependency is None:
            return False
        last_dependency_change = max(last_dependency_change, dependency.lstat().st_mtime)

    if not destination.exists():
        return True

    return destination.lstat().st_mtime < last_dependency_change


def generate_cover(video, cover, second=2):
    """
    Take a snapshot of the video to create a cover file.
    """
    command = [
        "ffmpeg",
        "-loglevel",
        "quiet",
        "-i",
        str(video.absolute()),
        "-vcodec",
        "mjpeg",
        "-vframes",
        "1",
        "-an",
        "-f",
        "rawvideo",
        "-ss",
        str(second),
        "-y",
        str(cover.absolute()),
    ]
    subprocess.check_call(command)


def generate_thumbnail(cover, thumbnail, geometry="200x200"):
    """
    Generate a reduced image of the cover.
    """
    command = [
        "convert",
        str(cover.absolute()),
        "-resize",
        geometry,
        str(thumbnail.absolute()),
    ]
    subprocess.check_call(command)
