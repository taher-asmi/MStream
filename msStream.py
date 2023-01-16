import numpy as np
from RecordHash import RecordHash
from NumHash import NumHash
from CatHash import CatHash

def counts_to_anom(tot: float, cur: float, cur_t: int):
    cur_mean = tot / cur_t
    sqerr = max(0, cur - cur_mean) ** 2
    return sqerr / cur_mean + sqerr / (cur_mean * max(1, cur_t - 1))

class MsStream:
    def __init__(self, num_rows, num_buckets, factor) -> None:
        self.num_rows = num_rows
        self.num_buckets = num_buckets
        self.factor = factor
        self.dimension1 = 0
        self.dimension2 = 0
        self.comp = 0

        self.cur_count = None
        self.total_count = None

        self.numeric_score = None
        self.numeric_total = None

        self.categ_score = None
        self.categ_total = None

        self.min_numeric = None
        self.max_numeric = None

        self.cur_t = 1
        self.time = 0

    
    def learn_one(self, X, cat_name, num_name,t):

        if not self.comp :
            self.dimension1 = len(num_name)
            self.dimension2 = len(cat_name) 

            self.cur_count = RecordHash(self.num_rows, self.num_buckets, self.dimension1, self.dimension2)
            self.total_count = RecordHash(self.num_rows, self.num_buckets, self.dimension1, self.dimension2)

            self.numeric_score = [NumHash(self.num_rows, self.num_buckets) for i in range(self.dimension1)]
            self.numeric_total = [NumHash(self.num_rows, self.num_buckets) for i in range(self.dimension1)] 

            self.categ_score = [CatHash(self.num_rows, self.num_buckets) for i in range(self.dimension2)]
            self.categ_total = [CatHash(self.num_rows, self.num_buckets) for i in range(self.dimension2)]
            self.time = t

        
        if (self.time!=t):
            self.lower()
            self.cur_t+=1

        numeric, categ = X[num_name], X[cat_name]

        cur_numeric = np.array(numeric)
        cur_categ = np.array(categ)

        cur_numeric = np.log10(1 + cur_numeric)

        if not self.comp:
            self.min_numeric = cur_numeric
            self.max_numeric = cur_numeric

        self.min_numeric = np.minimum(self.min_numeric, cur_numeric)
        self.max_numeric = np.maximum(self.max_numeric, cur_numeric)
        eps = 1e-15
        cur_numeric = (cur_numeric - self.min_numeric) / (eps+ self.max_numeric - self.min_numeric)

        for j in range(self.dimension1):
            self.numeric_score[j].insert(cur_numeric[j])
            self.numeric_total[j].insert(cur_numeric[j])

        for j in range(self.dimension2):
            self.categ_score[j].insert(cur_categ[j])
            self.categ_total[j].insert(cur_categ[j])

        self.cur_count.insert(cur_numeric, cur_categ, 1)
        self.total_count.insert(cur_numeric, cur_categ, 1)

        self.comp+= 1


    def score_one(self, X, cat_name, num_name,t):
         

        numeric, categ = X[num_name], X[cat_name]

        cur_numeric = np.array(numeric)
        cur_categ = np.array(categ)

        cur_numeric = np.log10(1 + cur_numeric)

        eps = 1e-6
        cur_numeric = (cur_numeric - self.min_numeric) / (eps+ self.max_numeric - self.min_numeric)

        sum1 = np.array([counts_to_anom(self.numeric_total[j].get_count(cur_numeric[j]),
                               self.numeric_score[j].get_count(cur_numeric[j]), self.cur_t) 
                for j in range(self.dimension1)])
        
        sum2 = np.array([counts_to_anom(self.categ_total[j].get_count(cur_categ[j]),
                               self.categ_score[j].get_count(cur_categ[j]), self.cur_t)
                for j in range(self.dimension2)])

        sum = sum1.sum()+sum2.sum()

        sum3 = counts_to_anom(self.total_count.get_count(cur_numeric, cur_categ),
                               self.cur_count.get_count(cur_numeric, cur_categ), self.cur_t)

        sum += sum3

        anom_score = (np.log(1+sum))        

        return anom_score

    def lower(self):
        self.cur_count.lower(self.factor)
        for j in range(self.dimension1):
            self.numeric_score[j].lower(self.factor)
        for j in range(self.dimension2):
            self.categ_score[j].lower(self.factor)



    def counts_to_anom(tot: float, cur: float, cur_t: int):
        cur_mean = tot / cur_t
        sqerr = max(0, cur - cur_mean) ** 2
        return sqerr / cur_mean + sqerr / (cur_mean * max(1, cur_t - 1))




