from pydantic import BaseModel
from plexflow.utils.strings.filesize import parse_size
from pathlib import Path
from typing import Optional

class TorrentFile(BaseModel):
    name: Optional[str]
    size: Optional[str]
    
    @property
    def size_bytes(self):
        return next(iter(parse_size(self.size)), None) if self.size else None

    @property
    def size_human(self):
        return self.size
    
    @property
    def extension(self):
        return Path(self.name).suffix.lstrip('.') if self.name else None

    def __str__(self) -> str:
        return f"{self.name} [({self.size_human})][{self.extension}][{self.size_bytes} bytes]"
    
    def __repr__(self) -> str:
        return self.__str__()

class TorrentSubtitle(BaseModel):
    language: Optional[str]
    name: Optional[str]
    
    def __str__(self) -> str:
        return f"{self.language} - {self.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
