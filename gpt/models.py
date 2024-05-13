import enum
from dataclasses import dataclass


class Role(enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class MessageDTO:
    role: Role
    content: str

    def as_dict(self):
        return {"role": self.role.value, "content": self.content}

    @staticmethod
    def from_user(request):
        return MessageDTO(Role.USER, request)
