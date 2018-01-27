import random
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw, ImagePalette


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


class SelectionSort(SortingAlgorithm):
    def sort(self, data):
        self.step(data)
        for i in range(len(data)):
            minIndex = i

            for j in range(i + 1, len(data)):
                if data[minIndex] > data[j]:
                    minIndex = j

            data[i], data[minIndex] = data[minIndex], data[i]
            self.step(data)


class BubbleSort(SortingAlgorithm):
    def sort(self, data):
        self.step(data)
        n = len(data)
        while True:
            swapped = False
            for i in range(1, n):
                if data[i - 1] > data[i]:
                    self.step(data)
                    data[i - 1], data[i] = data[i], data[i - 1]
                    swapped = True
            n -= 1
            if not swapped:
                break


class MergeSort(SortingAlgorithm):
    def sort(self, data, start=None, end=None):
        self.step(data)
        if start is None:
            start = 0
        if end is None:
            end = len(data)

        if end - start < 2:
            return

        middle = (start + end) // 2

        self.sort(data, start, middle)
        self.sort(data, middle, end)

        temp = []

        l = start
        r = middle
        while l < middle and r < end:
            if data[l] < data[r]:
                temp.append(data[l])
                l += 1
            else:
                temp.append(data[r])
                r += 1

        for i in range(l, middle):
            temp.append(data[i])
        for i in range(r, end):
            temp.append(data[i])

        for i in range(start, end):
            data[i] = temp[i - start]
            self.step(data)


class QuickSort(SortingAlgorithm):
    def sort(self, data, start=None, end=None):
        self.step(data)
        if start is None:
            start = 0
        if end is None:
            end = len(data) - 1

        if end <= start:
            return

        pivot = data[(end - start) // 2 + start]

        l = start
        r = end

        while True:
            while True:
                if data[l] < pivot:
                    l += 1
                else:
                    break
            while True:
                if data[r] > pivot:
                    r -= 1
                else:
                    break

            if l >= r:
                break

            data[r], data[l] = data[l], data[r]
            self.step(data)
            l += 1
            r -= 1

        self.sort(data, start, r)
        self.sort(data, r + 1, end)


class HeapSort(SortingAlgorithm):
    def sort(self, data):
        self.step(data)

        n = len(data)

        for i in range(n, 0, -1):
            self.heapify(data, n, i)

        for i in range(n - 1, 0, -1):
            data[i], data[0] = data[0], data[i]
            self.step(data)

            self.heapify(data, i, 0)

    def heapify(self, data, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and data[i] < data[l]:
            largest = l

        if r < n and data[largest] < data[r]:
            largest = r

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            self.step(data)
            self.heapify(data, n, largest)


if __name__ == '__main__':
    # color_grid = (range(0, 360, 6) for _ in range(0, 360, 6))
    color_grid = (range(0, 256, 4) for _ in range(0, 256, 4))
    steps = []
    for row in color_grid:
        line = list(row)
        random.shuffle(line)
        sort = MergeSort()
        sort.sort(line)
        steps.append(sort.steps)

    hue_grid = []

    for i in range(len(max(steps, key=len))):
        hue_grid.append([
            line[i if i < len(line) else len(line) - 1] for line in steps
        ])

    frames = []

    scale = 8

    length, width = len(hue_grid[0]), len(hue_grid[0])
    gif = Image.new('P', (length * scale, width * scale))

    # for hue in range(0, 256, 4):
    #     gif.putpalette()

    for frame in hue_grid:
        image = Image.new('HSV', (length, width))
        draw_ctx = ImageDraw.Draw(image)

        for x, row in enumerate(frame):
            for y, hue in enumerate(row):
                # draw_ctx.point((x, y), (int((hue / 360) * 256), 255, 255))
                draw_ctx.point((x, y), (hue, 255, 255))

        frames.append(image.convert('P').resize((length * scale, width * scale), resample=Image.NEAREST))

    gif.save('image.gif', save_all=True, append_images=frames, duration=100, loop=100)

    # image = Image.new('HSV', (len(sort.steps), len(color_grid)))
    # draw_ctx = ImageDraw.Draw(image)
    #
    # for x, step in enumerate(sort.steps):
    #     print(x, step)
    #     for y, color in enumerate(step):
    #         draw_ctx.point((x, y), (int((color / 360) * 256), 255, 255))
    #
    # image.convert('RGB').save('image.bmp')
    # image.show()
