import random
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw


class SortingAlgorithm(ABC):
    def __init__(self):
        self.steps = []

    def step(self, data):
        self.steps.append(list(data))

    @abstractmethod
    def sort(self, data):
        pass


class InsertionSort(SortingAlgorithm):
    def sort(self, data):
        self.step(data)
        for i in range(1, len(data)):
            j = i
            while j > 0 and data[j - 1] > data[j]:
                data[j], data[j - 1] = data[j - 1], data[j]
                self.step(data)
                j -= 1


if __name__ == '__main__':
    colors = list(range(0, 256 ** 3 * 4, 256 ** 3 // 64))
    random.shuffle(colors)
    sort = InsertionSort()
    sort.sort(colors)

    image = Image.new('RGB', (len(sort.steps), len(colors)))
    draw_ctx = ImageDraw.Draw(image)

    for x, step in enumerate(sort.steps):
        for y, color in enumerate(step):
            draw_ctx.point((x, y), color)

    image.show()
    image.save('image.bmp')
