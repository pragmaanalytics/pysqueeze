import os
import shutil

import compression_utils as cu

if __name__ == '__main__':
    output_dir = 'output'
    shutil.rmtree(output_dir, ignore_errors=True)

    for option in cu.CompressionOptions:
        cu.compress_dir_files('data', os.path.join(output_dir, option), method=option)

    cu.decompress_dir_files(os.path.join(output_dir, 'gzip'), os.path.join(output_dir, 'ungzipped'))
    cu.decompress_dir_files(os.path.join(output_dir, 'zip'), os.path.join(output_dir, 'unzipped'))
