import unittest


import scripts.src.Tools as t


class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.tools = t.Tools()

    def test_connected_cities(self):
        a = (1, 2)
        b = (0.5, 1.5)
        self.assertEqual(1, self.tools.isConnected(a, b, 0.8))

    def test_disconnected_cities(self):
        a=(1,2)
        b=(2,3)
        self.assertEqual(0, self.tools.isConnected(a,b, 0.8))


if __name__ == '__main__':
    unittest.main()
