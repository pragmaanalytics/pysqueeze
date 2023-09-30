import json
import os
import shutil
import unittest
from zipfile import ZipFile

import compression_utils as cu


class TestZip(unittest.TestCase):
    INPUT_DIR = os.path.join('test_data', 'input')
    OUTPUT_DIR = os.path.join('test_data', 'compressed_output')
    DECOMPRESSED_DIR = os.path.join('test_data', 'output', 'decompressed')

    @classmethod
    def setUpClass(cls) -> None:
        shutil.rmtree(cls.OUTPUT_DIR, ignore_errors=True)

        for option in cu.CompressionOptions:
            cu.compress_dir_files(cls.INPUT_DIR, os.path.join(cls.OUTPUT_DIR, option), method=option)

        cu.decompress_dir_files(os.path.join(cls.OUTPUT_DIR, 'gzip'), os.path.join(cls.DECOMPRESSED_DIR, 'ungzipped'))
        cu.decompress_dir_files(os.path.join(cls.OUTPUT_DIR, 'zip'), os.path.join(cls.DECOMPRESSED_DIR, 'unzipped'))

    def test_zip(self):
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'zip', 'test_file_1.json.zip'))
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'zip', 'test_dir', 'test_file_2.json.zip'))
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'zip', 'test_dir', 'test_dir_2', 'test_file_3.json.zip'))

        target_zip = os.path.join(self.OUTPUT_DIR, 'zip', 'test_file_1.json.zip')
        with ZipFile(target_zip, 'r') as zf:
            assert zf.filelist[0].filename == 'test_file_1.json'
            assert len(zf.filelist) == 1

    def test_gzip(self):
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'gzip', 'test_file_1.json.gzip'))
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'gzip', 'test_dir', 'test_file_2.json.gzip'))
        assert os.path.exists(os.path.join(self.OUTPUT_DIR, 'gzip', 'test_dir', 'test_dir_2', 'test_file_3.json.gzip'))

    def test_unzip(self):
        decompressed_dir = os.path.join(self.DECOMPRESSED_DIR, 'unzipped')
        with open(os.path.join(decompressed_dir, 'test_file_1.json')) as f:
            data = json.loads(f.read())
        assert data['test'] == 'data 1'

        with open(os.path.join(decompressed_dir, 'test_dir', 'test_dir_2', 'test_file_3.json')) as f:
            data = json.loads(f.read())
        assert data['test'] == 'data 3'

    def test_ungzip(self):
        decompressed_dir = os.path.join(self.DECOMPRESSED_DIR, 'ungzipped')
        with open(os.path.join(decompressed_dir, 'test_file_1.json')) as f:
            data = json.loads(f.read())
        assert data['test'] == 'data 1'

        with open(os.path.join(decompressed_dir, 'test_dir', 'test_dir_2', 'test_file_3.json')) as f:
            data = json.loads(f.read())
        assert data['test'] == 'data 3'
