import unittest
import os
import atom_bk_frame.util.settings_util as settings_util
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class SettingsUtilTest(unittest.TestCase):
    """atom_bk_frame.util.settings_util ファイルテスト

    Args:
        unittest (_type_): _description_
    """

    def setUp(self) -> None:
        os.environ.setdefault('SETTINGS_PATH', "settings")

    def test_get_settings(self,):
        settings = settings_util.get_settings()

        self.assertEqual(settings.APP_PATH, 'test.test_app')

    def test_get_member_by_settings(self,):
        app_path = settings_util.get_member_by_settings("APP_PATH")

        self.assertEqual(app_path, 'test.test_app')

    def test_get_module_path_by_settings(self,):
        module_path = settings_util.get_module_path_by_settings("APP_PATH")
        self.assertEqual(module_path, "test.test_app.test.test_app")


if __name__ == "__main__":
    unittest.main()
