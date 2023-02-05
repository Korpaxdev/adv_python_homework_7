class Stack:
    def __init__(self, items: any):
        if not isinstance(items, list):
            items = list(items)
        self.__items = items
        self.__last_iter_index = None

    def is_empty(self) -> bool:
        return bool(self.__items)

    def push(self, item: any) -> None:
        self.__items.append(item)

    def pop(self) -> any:
        return self.__items.pop()

    def peek(self) -> any:
        return self.__items[-1]

    def size(self) -> int:
        return len(self.__items)

    def __iter__(self):
        self.__last_iter_index = len(self.__items)
        return self

    def __next__(self):
        if self.__last_iter_index <= 0:
            raise StopIteration
        self.__last_iter_index -= 1
        return self.__items[self.__last_iter_index]
