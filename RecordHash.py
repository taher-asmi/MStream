import random
import math
from typing import List

class RecordHash:
    def __init__(self,num_rows:int, num_buckets:int, dim1: int, dim2: int):
        self.num_rows = num_rows
        self.num_buckets = num_buckets
        self.dimension1 = dim1
        self.dimension2 = dim2
        self.num_recordhash = [[[random.normalvariate(0,1) for _ in range(dim1)] for _ in range(int(math.ceil(math.log2(num_buckets))))] for _ in range(num_rows)]
        self.cat_recordhash = [[random.randint(1, num_buckets-1) if k < dim2-1 else random.randint(0, num_buckets-1) for k in range(dim2)] for _ in range(num_rows)]
        self.count = [[1.0 for _ in range(num_buckets)] for _ in range(num_rows)]

    def numerichash(self, cur_numeric: List[float], i: int) -> int:
        sum_ = 0.0
        bitcounter = 0
        log_bucket = math.ceil(math.log2(self.num_buckets))
        b = 0
        for iter in range(int(log_bucket)):
            sum_ = 0.0
            for k in range(self.dimension1):
                sum_ += self.num_recordhash[i][iter][k] * cur_numeric[k]
            b = b | ((1 if sum_ >= 0 else 0) << bitcounter)
            bitcounter += 1
        return int(b)
  
    def categhash(self, cur_categ: List[int], i: int) -> int:
        counter = 0
        resid = 0
        for k in range(self.dimension2):
            resid = (resid + self.cat_recordhash[i][counter] * cur_categ[counter]) % self.num_buckets
            counter += 1
        return int(resid + (resid < 0) * self.num_buckets)

    def insert(self, cur_numeric: List[float], cur_categ: List[int], weight: float):
        bucket1, bucket2, bucket = None, None, None
        for i in range(self.num_rows):
            bucket1 = self.numerichash(cur_numeric, i)
            bucket2 = self.categhash(cur_categ, i)
            bucket = (bucket1 + bucket2) % self.num_buckets
            self.count[i][bucket] += weight

    def get_count(self, cur_numeric: List[float], cur_categ: List[int]) -> float:
        min_count = float('inf')
        bucket1, bucket2, bucket = None, None, None
        for i in range(self.num_rows):
            bucket1 = self.numerichash(cur_numeric, i)
            bucket2 = self.categhash(cur_categ, i)
            bucket = (bucket1 + bucket2) % self.num_buckets
            min_count = min(min_count, self.count[i][bucket])
        return min_count

    def clear(self):
        self.count = [[1.0 for _ in range(self.num_buckets)] for _ in range(self.num_rows)]

    def lower(self, factor: float):
        self.count = [[count * factor for count in row] for row in self.count]

