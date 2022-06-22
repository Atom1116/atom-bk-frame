import unittest
from atom_bk_frame.util.class_loader_util import get_module_by_full_route, get_module_by_route, get_module_by_file_path


class TestCallModule:
    def __init__(self) -> None:
        self.a = "test_a"
        self.b = "test_b"

    def call_a(self):
        return self.a


class ClassLLoaderUtilTest(unittest.TestCase):
    """atom_bk_frame.util.class_loader_util ファイルテスト

    Args:
        unittest (_type_): _description_
    """

    def test_get_module_by_full_route(self,):

        module = get_module_by_full_route(
            'class_loader_util_test.TestCallModule',
        )

        test_call_module = module()

        self.assertEqual(test_call_module.call_a(), "test_a")

    def test_get_module_by_route(self,):

        module = get_module_by_route(
            'TestCallModule',
            'class_loader_util_test'
        )

        test_call_module = module()

        self.assertEqual(test_call_module.call_a(), "test_a")

    @unittest.skip('not use method')
    def test_get_module_by_file_path(self,):

        module = get_module_by_file_path(
            'TestCallModule',
            './class_loader_util_test'
        )

        test_call_module = module()

        self.assertEqual(test_call_module.call_a(), "test_a")


if __name__ == "__main__":
    unittest.main()
