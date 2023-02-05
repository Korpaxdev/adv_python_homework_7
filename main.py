from classes.brackets import Brackets
from collections import namedtuple


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
    test_brackets = get_test_data()
    for test_bracket in test_brackets:
        bracket = Brackets(test_bracket.bracket)
        assert bracket.is_balanced() == test_bracket.result
        print('Сбалансировано' if bracket.is_balanced() else 'Несбалансированно')


if __name__ == '__main__':
    main()
