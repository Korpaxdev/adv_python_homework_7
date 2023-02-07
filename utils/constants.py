from dataclasses import dataclass


@dataclass(frozen=True)
class EnvNames:
    GMAIL_LOGIN = 'GMAIL_LOGIN'
    GMAIL_PASSWORD = 'GMAIL_PASSWORD'


@dataclass(frozen=True)
class BaseMessages:
    BALANCED = 'Сбалансированоо'
    IMBALANCED = 'Неслабалансировано'
    BRACKETS = 'Задача № 1 и 2. На проверку сбалансированности'
    GMAILER = 'Задача № 3. Отправка писем на Gmail'


@dataclass(frozen=True)
class GmailBase:
    SMTP = 'smtp.gmail.com'
    IMAP = 'imap.gmail.com'
    PORT = 587
    DEFAULT_SUBJECT = 'Without subject'
    SUCCESS_MESSAGE_FORMAT = '[SUCCESS] Message sent'
    ERROR_MESSAGE_FORMAT = '[ERROR] An error occurred in {name} - {text}'
    INBOX = 'INBOX'


@dataclass(frozen=True)
class ImapSearchTypes:
    ALL = 'ALL'
    UNSEEN = 'UNSEEN'


@dataclass(frozen=True)
class MailTypes:
    TEXT_PLAIN = 'text/plain'


@dataclass(frozen=True)
class Imap:
    SEARCH = 'SEARCH'
    FETCH = 'FETCH'
    SEARCH_TYPES = ImapSearchTypes
    MAIL_TYPES = MailTypes
    RFC = '(RFC822)'
