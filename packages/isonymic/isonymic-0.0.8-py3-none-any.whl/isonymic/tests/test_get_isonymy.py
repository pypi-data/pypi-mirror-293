import unittest
import pandas
from isonymic.indicators.isonymy import get_isonymy


class TestGetIsonymy(unittest.TestCase):
    def test_get_isonymy(self):
        isonymy_result = get_isonymy.get_isonymy(pandas.Series([1, 1, 1, 1]))
        self.assertEqual(isonymy_result, 1)


unittest.main()
