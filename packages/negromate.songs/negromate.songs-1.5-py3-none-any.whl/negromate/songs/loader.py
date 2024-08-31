"""
Load songs from the root folder.
"""

import json

import asstosrt
import webvtt

from . import logger
from .karaoke_templates import generate_karaoke_ass
from .utils import generate_cover, generate_thumbnail, needs_change


class Song:
    """
    Python representation of a song.
    """

    def __init__(self, path, root):
        self.name = path.name
        self.metadata = None
        self.original = None
        self.author = None
        self.date = None
        self.path = path
        self.root = root
        self.video = None
        self.video_type = None
        self.vtt = None
        self.srt = None
        self.karaoke_ass = None
        self.ass = None
        self.cover = None
        self.thumbnail = None
        self.files = []
        self.search_media()

    def search_media(self):
        """
        Initialize song attributes.
        """
        for entry in self.path.iterdir():
            if entry.name == "metadata.json":
                with entry.open("r") as metadatafile:
                    self.metadata = json.load(metadatafile)
                self.name = self.metadata.get("name", self.path.name)
                self.original = self.metadata.get("original", None)
                self.author = self.metadata.get("author", None)
                self.date = self.metadata.get("date", None)
            elif entry.name.endswith("mp4"):
                self.video = entry
                self.video_type = "video/mp4"
                self.files.append(entry)
            elif entry.name.endswith("webm"):
                self.video = entry
                self.video_type = "video/webm"
                self.files.append(entry)
            elif entry.name.endswith("ogv"):
                self.video = entry
                self.video_type = "video/ogg"
                self.files.append(entry)
            elif entry.name.endswith("vtt"):
                self.vtt = entry
            elif entry.name == f"{self.path.name}.srt":
                self.srt = entry
                self.files.append(entry)
            elif entry.name == f"{self.path.name}.karaoke.ass":
                self.karaoke_ass = entry
                self.files.append(entry)
            elif entry.name == f"{self.path.name}.ass":
                self.ass = entry
                self.files.append(entry)
            elif entry.name == "thumb.jpg":
                self.thumbnail = entry
            elif entry.name == "cover.jpg":
                self.cover = entry
            elif entry.name == "index.html":
                continue
            else:
                self.files.append(entry)

    def generate_missing(self, regenerate=False, karaoke_template_file=None):
        """
        Generate missing files, if they can be derived from another one.
        """
        srt_ = self.path / f"{self.path.name}.srt"
        if regenerate or needs_change(srt_, (self.ass,)):
            logger.info("generating %s", str(srt_))
            self.srt = srt_
            with self.ass.open("r") as assfile, self.srt.open("w") as srtfile:
                srtfile.write(asstosrt.convert(assfile))
            self.files.append(self.srt)

        vtt = self.path / f"{self.path.name}.vtt"
        if regenerate or needs_change(vtt, (self.srt,)):
            logger.info("generating %s", str(vtt))
            self.vtt = vtt
            webvtt.from_srt(str(self.srt.absolute())).save(str(self.vtt.absolute()))

        cover = self.path / "cover.jpg"
        if regenerate or needs_change(cover, (self.video,)):
            logger.info("generating %s", str(cover))
            self.cover = cover
            generate_cover(self.video, self.cover)

        thumbnail = self.path / "thumb.jpg"
        if regenerate or needs_change(thumbnail, (self.cover,)):
            logger.info("generating %s", str(thumbnail))
            self.thumbnail = thumbnail
            generate_thumbnail(self.cover, self.thumbnail)

        karaoke_ass = self.path / f"{self.path.name}.karaoke.ass"
        karaoke_requirements = (
            self.metadata.get("karaoke", False),
            regenerate or needs_change(karaoke_ass, (self.ass, karaoke_template_file)),
        )
        if all(karaoke_requirements):
            logger.info("generating %s", str(karaoke_ass))
            self.karaoke_ass = karaoke_ass
            generate_karaoke_ass(str(karaoke_template_file), str(self.ass), str(karaoke_ass))

    @property
    def has_subtitles(self):
        """
        True if the song has any type of subtitles.
        """
        return self.ass or self.srt or self.vtt

    @property
    def publish(self):
        """
        True if the song can be published.
        """
        return self.video and self.has_subtitles

    @property
    def pending(self):
        """
        True if the song has a video and ass subtitles.
        """
        finished = self.ass and self.video
        return not finished


def load_songs(root_folder, generate=True, regenerate=False, karaoke_template_file=None):
    """
    Load songs from root_folder.

    If generate is True missing files will be generated.

    If regenerate is True, the files will be generated again, even if they source has not changed.

    karaoke_template_file can be a path to a ass file with the code to generate subtitle animations.
    """
    songs = []
    pending_songs = []
    for entry in root_folder.iterdir():
        if entry.name in ["static", "playlist", "home", "todo"]:
            continue
        if entry.is_dir() and (entry / "metadata.json").exists():
            logger.info("building %s", str(entry.name))
            try:
                song = Song(entry, root_folder)
                if generate:
                    song.generate_missing(regenerate, karaoke_template_file)
            except Exception as e:
                logger.error("Error: %s", e)
                continue
            if song.publish:
                songs.append(song)
            if song.pending:
                pending_songs.append(song)

    songs.sort(key=lambda a: a.name)

    return songs, pending_songs
