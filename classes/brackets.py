from classes.stack import Stack


class Brackets:
    def __init__(self, brackets: any):
        self.__brackets = Stack(brackets)
        self.__size = self.__brackets.size()
        self.__close_bracket_pairs = {
            ')': '(',
            ']': '[',
            '}': '{'
        }
        self.__balanced = self.__check_balanced()

    def __check_size(self) -> bool:
        return self.__size % 2 == 0

    def __check_balanced(self) -> bool:
        """
        Проверяет сбалансирован ли стек скобок или нет.
        - Если длина стека не четная, то список не сбалансирован.
        - Итерация по стеку:
            1. Если скобка закрывающая (т.е. есть среди ключей __close_brackets_pairs), то добавляется ее пара в список needed_bracket.
            2. Если скобка открывающая и есть в needed_bracket, то из списка удаляется эта скобка.
            3. Если скобка открывающая и ее нет в списке needed_bracket, то значит это лишняя скобка - список не сбалансирован.
            4. Если список needed_brackets не пустой, значит список не сбалансирован
        """
        if not self.__check_size():
            return False
        needed_bracket = []
        for bracket in self.__brackets:
            if bracket in self.__close_bracket_pairs:
                needed_bracket.append(self.__close_bracket_pairs[bracket])
            elif bracket in needed_bracket:
                needed_bracket.remove(bracket)
            else:
                return False
        return not needed_bracket

    def is_balanced(self) -> bool:
        return self.__balanced
