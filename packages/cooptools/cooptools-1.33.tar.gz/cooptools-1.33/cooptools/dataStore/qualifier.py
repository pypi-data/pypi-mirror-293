from dataclasses import dataclass
from cooptools.protocols import UniqueIdentifier

@dataclass(frozen=True, slots=True)
class PatternMatchQuery:
    regex: str = None
    id: UniqueIdentifier = None

    def __post_init__(self):
        if self.regex is None and self.id is None:
            raise ValueError(f"At least one of regex or id must be filled")

        if self.id is not None:
            object.__setattr__(self, f'{self.regex=}'.split('=')[0].replace('self.', ''), str(self.id))

    def check_if_matches(self, value: str):
        return re.match(self.regex, value)
