from collections import namedtuple
from dotenv import load_dotenv
from os.path import join, dirname
from os import environ

from classes.brackets import Brackets
from classes.gmailer import Gmailer
from utils.constants import EnvNames, BaseMessages


def get_test_data():
    TestBracket = namedtuple('TestBracket', 'bracket, result')
    brackets = [('(((([{}]))))', True),
                ('[([])((([[[]]])))]{()}', True),
                ('{{[()]}}', True),
                ('}{}', False),
                ('{{[(])]}}', False),
                ('[[{())}]', False),
                ('))))', False),
                ('))((', False)]
    return [TestBracket(bracket[0], bracket[1]) for bracket in brackets]


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    gmail_login = environ.get(EnvNames.GMAIL_LOGIN)
    gmail_password = environ.get(EnvNames.GMAIL_PASSWORD)

    # Lesson 1 and Lesson 2
    print(BaseMessages.BRACKETS, end='\n\n')
    test_brackets = get_test_data()
    for test_bracket in test_brackets:
        bracket = Brackets(test_bracket.bracket)
        assert bracket.is_balanced() == test_bracket.result
        print(BaseMessages.BALANCED if bracket.is_balanced() else BaseMessages.IMBALANCED)

    # # Lesson 3
    print(f'\n{BaseMessages.GMAILER}', end='\n\n')
    gmailer = Gmailer(gmail_login, gmail_password)
    gmailer.send_message(message='Hello world', subject='This is a test message')
    messages = gmailer.receive_last_messages()
    gmailer.print_text_messages(messages)


if __name__ == '__main__':
    main()
