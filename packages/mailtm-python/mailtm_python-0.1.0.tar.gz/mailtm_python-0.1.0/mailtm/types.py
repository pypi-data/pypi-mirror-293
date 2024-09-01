from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Domain:
    a_context: Optional[str] = field(default=None)
    a_id: Optional[str] = field(default=None)
    a_type: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    domain: Optional[str] = field(default=None)
    isActive: Optional[bool] = field(default=None)
    isPrivate: Optional[bool] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    updatedAt: Optional[str] = field(default=None)


@dataclass
class MessageRecipient:
    name: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)


@dataclass
class Attachment:
    id: Optional[str] = field(default=None)
    filename: Optional[str] = field(default=None)
    contentType: Optional[str] = field(default=None)
    disposition: Optional[str] = field(default=None)
    transferEncoding: Optional[str] = field(default=None)
    related: Optional[bool] = field(default=None)
    size: Optional[int] = field(default=None)
    downloadUrl: Optional[str] = field(default=None)


@dataclass
class Message:
    a_context: Optional[str] = field(default=None)
    a_id: Optional[str] = field(default=None)
    a_type: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    accountId: Optional[str] = field(default=None)
    msgid: Optional[str] = field(default=None)
    from_: Optional[MessageRecipient] = field(default=None, metadata={'field_name': 'from'})
    to: Optional[List[MessageRecipient]] = field(default_factory=list)
    subject: Optional[str] = field(default=None)
    intro: Optional[str] = field(default=None)
    seen: Optional[bool] = field(default=None)
    isDeleted: Optional[bool] = field(default=None)
    hasAttachments: Optional[bool] = field(default=None)
    size: Optional[int] = field(default=None)
    downloadUrl: Optional[str] = field(default=None)
    sourceUrl: Optional[str] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    updatedAt: Optional[str] = field(default=None)

    def __post_init__(self):
        # Convert 'from_' field to a MessageRecipient instance if it is a dict
        if isinstance(self.from_, dict):
            self.from_ = MessageRecipient(**self.from_)
        
        # Convert 'to' list of dicts to list of MessageRecipient instances
        if isinstance(self.to, list):
            self.to = [MessageRecipient(**recipient) if isinstance(recipient, dict) else recipient for recipient in self.to]


@dataclass
class MessageDetail(Message):
    cc: Optional[List[MessageRecipient]] = field(default_factory=list)
    bcc: Optional[List[MessageRecipient]] = field(default_factory=list)
    verifications: Optional[List[str]] = field(default_factory=list)
    retention: Optional[bool] = field(default=None)
    retentionDate: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    html: Optional[List[str]] = field(default_factory=list)
    attachments: Optional[List[Attachment]] = field(default_factory=list)
    flagged: Optional[bool] = field(default=None)  # Add the flagged field

    def __post_init__(self):
        super().__post_init__()  # Ensure base class post init is called
        
        # Convert 'cc' and 'bcc' fields to lists of MessageRecipient instances
        if isinstance(self.cc, list):
            self.cc = [MessageRecipient(**recipient) if isinstance(recipient, dict) else recipient for recipient in self.cc]
        if isinstance(self.bcc, list):
            self.bcc = [MessageRecipient(**recipient) if isinstance(recipient, dict) else recipient for recipient in self.bcc]
        
        # Convert 'attachments' field to a list of Attachment instances
        if isinstance(self.attachments, list):
            self.attachments = [Attachment(**attachment) if isinstance(attachment, dict) else attachment for attachment in self.attachments]


@dataclass
class TokenResponse:
    a_context: Optional[str] = field(default=None)
    a_id: Optional[str] = field(default=None)
    a_type: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)


@dataclass
class MessageSource:
    a_context: Optional[str] = field(default=None)
    a_id: Optional[str] = field(default=None)
    a_type: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    downloadUrl: Optional[str] = field(default=None)
    data: Optional[str] = field(default=None)


@dataclass
class Account:
    a_context: Optional[str] = field(default=None)
    a_id: Optional[str] = field(default=None)
    a_type: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)
    address: Optional[str] = field(default=None)
    quota: Optional[int] = field(default=None)
    used: Optional[int] = field(default=None)
    isDisabled: Optional[bool] = field(default=None)
    isDeleted: Optional[bool] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    updatedAt: Optional[str] = field(default=None)
