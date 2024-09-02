import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

from blackboard.api_extended import BlackboardExtended
from blackboard.blackboard import BBCourseContent

from .base import FStream
from .job import DownloadJob


class ExternalLink(FStream):
    """Creates a platform-aware internet shortcut."""

    def __init__(self, content: BBCourseContent, _, job: DownloadJob):
        self.url = content.contentHandler.url

    def write(self, path: Path, executor: ThreadPoolExecutor):
        if self.url is None:
            return

        path = path / path.stem

        if platform.system() in ["Windows", "Darwin"]:
            body = f"[InternetShortcut]\nURL={self.url}"
            path = path.with_suffix(".url")
        else:
            body = f"[Desktop Entry]\nIcon=text-html\nType=Link\nURL[$e]={self.url}"

        super().write(path, body, executor)

    @property
    def create_dir(self) -> bool:
        return True
