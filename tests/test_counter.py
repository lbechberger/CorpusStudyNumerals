import unittest

from counter import Counter

class CounterTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(CounterTest, self).__init__(*args, **kwargs)
        self.counter = Counter(0,10)

    def test_empty(self):
        self.counter.reset()
        self.assertEqual(self.counter[3],0)

    def test_single(self):
        self.counter.reset()
        self.counter(3)
        self.assertEqual(self.counter[3],1)

    def test_multiple(self):
        self.counter.reset()
        self.counter(5)
        self.counter(5)
        self.assertEqual(self.counter[5],2)

    def test_count_list(self):
        self.counter.reset()
        self.counter([1,3,5,1])
        self.assertEqual(self.counter[1],2)
        self.assertEqual(self.counter[3],1)
        self.assertEqual(self.counter[5],1)

    def test_count_tuple(self):
        self.counter.reset()
        self.counter((1,3,5,1))
        self.assertEqual(self.counter[1],2)
        self.assertEqual(self.counter[3],1)
        self.assertEqual(self.counter[5],1)

    def test_count_args(self):
        self.counter.reset()
        self.counter(1,3,5,1)
        self.assertEqual(self.counter[1],2)
        self.assertEqual(self.counter[3],1)
        self.assertEqual(self.counter[5],1)

    def test_multiget(self):
        self.counter.reset()
        self.counter(1)
        self.counter(3)
        self.counter(5)
        self.counter(1)
        self.assertEqual(self.counter[1,2,3,4,5],[2,0,1,0,1])

    def test_boundaries(self):
        self.counter.reset()
        self.counter([-1,0,10,11])
        self.assertEqual(self.counter[-1],0)
        self.assertEqual(self.counter[0],1)
        self.assertEqual(self.counter[10],1)
        self.assertEqual(self.counter[11],0)

    def test_reset(self):
        self.counter.reset()
        self.counter(1)
        self.assertEqual(self.counter[1],1)
        self.counter.reset()
        self.assertEqual(self.counter[1],0)
