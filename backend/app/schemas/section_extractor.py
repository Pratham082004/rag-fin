from dataclasses import dataclass
import re


@dataclass
class Section:

    title: str

    start: int

    end: int

    content: str