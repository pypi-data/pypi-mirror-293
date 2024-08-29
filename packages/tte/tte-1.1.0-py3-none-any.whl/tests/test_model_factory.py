import unittest
from tte_models.ModelFactory import get_model


class TestGetModel(unittest.TestCase):

    def test_get_model(self):
        self.assertEquals(get_model("Some_Model", 10), None)


unittest.main()
