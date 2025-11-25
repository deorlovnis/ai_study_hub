from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Draft:
    id: int
    raw_text: str
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Pipeline:
    id: int
    name: str
    channel: str
    language_avatar: str
    user_persona: str
    post_config: str

@dataclass
class GeneratedPost:
    id: int
    draft_id: int
    pipeline_id: int
    final_text: str
    created_at: datetime = field(default_factory=datetime.utcnow)
