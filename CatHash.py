import numpy as np
import random

class CatHash:
    def __init__(self, num_rows:int, num_buckets:int):
        self.num_rows = num_rows
        self.num_buckets = num_buckets
        self.hash_a = [random.randint(1, num_buckets) for _ in range(num_rows)]
        self.hash_b = [random.randint(0, num_buckets-1) for _ in range(num_rows)]
        self.count = np.ones((num_rows, num_buckets))
        self.clear()

    def transform(self, a, i: int):#i: int
        resid = (a * self.hash_a[i] + self.hash_b[i]) % self.num_buckets
        return int(resid)

    def insert(self, cur_int):#cur_int: int
        for i in range(self.num_rows):
            bucket = self.transform(cur_int, i)
            self.count[i][bucket] += 1

    def get_count(self, cur_int):#cur_int: int
        min_count = float('inf')
        for i in range(self.num_rows):
            bucket = self.transform(cur_int, i)
            min_count = min(min_count, self.count[i][bucket])
        return min_count

    def clear(self):
        self.count = np.ones((self.num_rows, self.num_buckets))

    def lower(self, factor):
        self.count = self.count * factor
