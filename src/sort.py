from typing import Generator


class SVSort:
    def __init__(self, array: list[int]) -> None:
        self.array = array
        self.size = len(array)

    def swap(self, i: int, j: int) -> None:
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def bubble_sort(self) -> Generator:
        for _ in range(self.size):
            for j in range(self.size - 1):
                if self.array[j] > self.array[j + 1]:
                    self.swap(j, j + 1)

            yield self.array
