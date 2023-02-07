import base64
import binascii
import quopri
import inspect
from email import message_from_bytes
from email.header import decode_header, Header
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from imaplib import IMAP4_SSL
from smtplib import SMTP

from utils.constants import GmailBase, Imap


class Gmailer:
    def __init__(self, login: str, password: str):
        self.__login = login
        self.__password = password

    def send_message(self, message: str,
                     to_emails: list | str = "",
                     subject: str = GmailBase.DEFAULT_SUBJECT,
                     ) -> None:
        """
        sends email with message and subject to recipients in to_emails.
        :param message: str - contains text for a message body
        :param to_emails: str or list - contains recipients emails
        :param subject: str (default GmailBase.DEFAULT_SUBJECT) - contains email subject
        :return: None
        """
        try:
            with SMTP(GmailBase.SMTP, GmailBase.PORT) as mailer:
                msg = self.__set_msg(to_emails, subject, message)
                mailer.starttls()
                mailer.login(self.__login, self.__password)
                mailer.send_message(msg)
                print(GmailBase.SUCCESS_MESSAGE_FORMAT)
        except Exception as ex:
            self.__print_error_message(ex)

    def receive_last_messages(self,
                              search_type: Imap.SEARCH_TYPES = Imap.SEARCH_TYPES.ALL,
                              count: int = 1) -> list[Message] | None:
        """
        Returns list of recent messages from gmail.
        :param search_type: Imap.SEARCH_TYPE - contains search type (see Imap.SEARCH_TYPES)
        :param count: int (default = 1) - contains the number of recent email to be received
        :return: list of recent messages or None on error
        """
        with IMAP4_SSL(GmailBase.IMAP) as mailer:
            try:
                mailer.login(self.__login, self.__password)
                mailer.list()
                mailer.select(GmailBase.INBOX)
                letters_uid = self.__get_uid_letters(mailer, search_type, count)
                messages = self.__get_emails(mailer, letters_uid)
                return messages

            except Exception as ex:
                self.__print_error_message(ex)

    def __set_valid_to_emails(self, to_emails: str | list | None) -> str:
        """
        converts to_emails to the valid string.
        :param to_emails: str or list - contains recipients emails
        :return: str - returns string with recipients emails
        """
        if not to_emails:
            to_emails = self.__login
        else:
            if isinstance(to_emails, list):
                to_emails = ', '.join(to_emails)
        return to_emails

    def __set_msg(self, to_emails: list | str | None,
                  subject: str,
                  message: str) -> MIMEMultipart:
        """
        creates a MIMEMultipart object with to_emails, subject and message.
        :param to_emails: list or str or None - recipients emails
        :param subject: contains email subject
        :param message: str - contains text for a message body
        :return: a valid MIMEMultipart message object
        """
        msg = MIMEMultipart()
        msg['To'] = self.__set_valid_to_emails(to_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(message))
        return msg

    def __get_emails(self, mailer: IMAP4_SSL, emails_uid: list) -> list[Message]:
        """
        gets emails by emails_uid.
        :param mailer: IMAP4_SSL - IMAP4 connection object
        :param emails_uid: list - list with emails uid
        :return: list with emails
        """
        mails = []
        for email_uid in emails_uid:
            try:
                _, data = mailer.uid(Imap.FETCH, email_uid, Imap.RFC)
                mail = message_from_bytes(data[0][1])
                mails.append(mail)
            except Exception as ex:
                self.__print_error_message(ex)
        return mails

    def print_text_messages(self, messages: list[Message] | None) -> None:
        """
        Prints message content (from, subject, body).
        If message doesn't have a text/plain -
        print message doesn't have a text/plain.
        :param messages: list[Message] - list with messages
        :return: None
        """
        if not messages:
            self.__print_error_message('Messages is empty')
            return None
        for message in messages:
            message_from = self.__decode_from_header(message['FROM'])
            message_subject = self.__decode_from_header(message['SUBJECT'])
            print(f'[FROM] {message_from}')
            print(f'[SUBJECT] {message_subject}')
            print('[BODY START]\n')
            payload = self.__get_text_plain_payload(message)
            if payload:
                payload = payload.pop()
                body = self.__get_decoded_body(payload.get_payload())
                print(body)
            else:
                print('MESSAGE DOESNT HAVE A TEXT/PLAIN')
            print('\n[BODY END]\n')

    @staticmethod
    def __get_uid_letters(mailer: IMAP4_SSL,
                          search_type: Imap.SEARCH_TYPES,
                          count: int) -> list:
        """
        Gets all emails uid and return specified number of emails uid.
        :param mailer: IMAP4 connection object
        :param search_type: Imap.SEARCH_TYPE - contains search type (see Imap.SEARCH_TYPES)
        :param count: int - contains the number of recent email to be received
        :return: list with emails uid
        """
        _, data = mailer.uid(Imap.SEARCH, search_type)
        letters_uid: list = data.pop().split()
        letters_uid.reverse()
        return letters_uid[:count]

    @staticmethod
    def __print_error_message(error_message: Exception | str) -> None:
        """
        Prints error message and function name where error occurred.
        :param error_message: Exception or str - text with error message
        :return: None
        """
        function_name = inspect.stack()[1].function
        print(GmailBase.ERROR_MESSAGE_FORMAT.format(name=function_name, text=repr(error_message)))

    @staticmethod
    def __decode_from_header(header: Header | str) -> str:
        """
        Decodes message header.
        :param header: Header or str - object with message header
        :return: decoded message header
        """
        decoded_header = decode_header(header)[0][0]
        if 'decode' in dir(decoded_header):
            return decoded_header.decode('utf-8')
        return str(decoded_header)

    @staticmethod
    def __get_decoded_body(encoded_body: bytes) -> str:
        """
        decodes message body.
        :param encoded_body: bytes - encoded message body
        :return: decoded message body
        """
        try:
            body = base64.b64decode(encoded_body).decode('utf-8')
            return body
        except (UnicodeDecodeError, binascii.Error):
            body = quopri.decodestring(encoded_body).decode('utf-8')
            return body

    @staticmethod
    def __get_text_plain_payload(message: Message) -> list[Message] | list:
        """
        returns list of payloads which contain content type - text/plain
        :param message: Message - object with message
        :return: list of payloads or empty list
        """
        return [payload for payload in message.walk() if
                payload.get_content_type() == Imap.MAIL_TYPES.TEXT_PLAIN]
