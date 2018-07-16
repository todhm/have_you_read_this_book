import unittest
from common import calculate_distance


class SparkAppTest(unittest.TestCase):
    def setUp(self):
        self.query = "hello"

    def test_text_sim(self):
        sentence_lst =["yellow world","bye bye world","hello world","askdjf;alskdadfadsf"]
        sorted_lst = calculate_distance(self.query,sentence_lst)
        assert(sorted_lst[0]=="hello world")
        assert(sorted_lst[1] == "yellow world")
        assert(sorted_lst[-1] == "askdjf;alskdadfadsf")



if __name__ == '__main__':
    unittest.main()
