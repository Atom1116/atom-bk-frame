import unittest
import os
from atom_bk_frame.util.file_util import create_dir
import unittest.mock


class FileUtilTest(unittest.TestCase):
    """atom_bk_frame.util.file_util ファイルテスト

    Args:
        unittest (_type_): _description_
    """

    # @unittest.mock.patch('os.path.isdir', return_value=False)
    def test_create_dir(self):
        test_dir = os.getcwd() + "/test_dir"

        print(test_dir)
        # ディレクトリの作成
        create_dir(test_dir)

        self.assertTrue(os.path.isdir(test_dir))

    def tearDown(self) -> None:
        os.rmdir(os.getcwd() + "/test_dir")


if __name__ == "__main__":
    unittest.main()
