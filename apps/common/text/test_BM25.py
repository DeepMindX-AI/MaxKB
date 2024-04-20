import unittest
from common.text.BM25 import BM25

class TestBM25(unittest.TestCase):
    def setUp(self):
        self.document_list = ["行政机关强行解除行政协议造成损失，如何索取赔偿？",
                              "借钱给朋友到期不还得什么时候可以起诉？怎么起诉？",
                              "我在微信上被骗了，请问被骗多少钱才可以立案？",
                              "公民对于选举委员会对选民的资格申诉的处理决定不服，能不能去法院起诉吗？",
                              "有人走私两万元，怎么处置他？",
                              "法律上餐具、饮具集中消毒服务单位的责任是不是对消毒餐具、饮具进行检验？"]
        self.query = "走私了两万元，在法律上应该怎么量刑？"
        self.bm25 = BM25(self.document_list)

    def test_initialization(self):
        self.assertEqual(self.bm25.k1, 1.5)
        self.assertEqual(self.bm25.b, 0.75)
        self.assertEqual(self.bm25.corpus_size, 6)
        self.assertTrue(isinstance(self.bm25.corpus[0], list))
        print(self.bm25.get_score_docs(self.query))