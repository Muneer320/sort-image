from typing import Generator


class SVSort:
    def __init__(self, array: list[int]) -> None:
        self.array = array
        self.size = len(array)

        self.algorithms: list[object] = []
        self.algorithms.append(self.bubble_sort)

    def swap(self, i: int, j: int) -> None:
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def bubble_sort(self) -> Generator[list[int], None, None]:
        for _ in range(self.size):
            for j in range(self.size - 1):
                if self.array[j] > self.array[j + 1]:
                    self.swap(j, j + 1)

            yield self.array

    def sort(self, index: int) -> object:
        algorithm = self.algorithms[index]
        return algorithm
