import numpy as np
import math

class NumHash:

    def __init__(self, num_rows:int, num_buckets:int):
        self.num_rows = num_rows
        self.num_buckets = num_buckets
        self.count = np.ones((num_rows,num_buckets))

    
    def transform(self, x):
        val = math.floor(x * self.num_buckets)
        return(val % self.num_buckets)
    

    def insert(self, x):
        hashing = self.transform(x)
        self.count[0][hashing] += 1

    def get_count(self, x):
        hashing = self.transform(x)
        return (self.count[0][hashing])
    
    def lower(self, factor):
        self.count = factor * self.count
    
    def clear(self):
        self.count = np.ones((self.num_rows, self.num_buckets))
