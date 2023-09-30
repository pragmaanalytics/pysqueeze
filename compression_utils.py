import gzip
import os
import zipfile
from enum import Enum
from functools import wraps
from time import time


def zip_it(input_path, output_path):
    base_file = os.path.basename(input_path)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        zf.write(input_path, base_file)


def gzip_it(input_path, output_path):
    with (open(input_path, 'rb') as inpf, open(output_path, 'wb') as outf):
        raw_content = inpf.read()
        compressed_data = gzip.compress(raw_content)
        outf.write(compressed_data)


def unzip_it(input_path, output_path):
    # base_file = os.path.basename(output_path)

    with zipfile.ZipFile(input_path, "r") as zf:
        zf.extractall(os.path.dirname(output_path))


def ungzip_it(input_path, output_path):
    with (open(input_path, 'rb') as inpf, open(output_path, 'wb') as outf):
        raw_content = inpf.read()
        decompressed_data = gzip.decompress(raw_content)
        outf.write(decompressed_data)


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' %
              (f.__name__, args, kw, te-ts))
        return result
    return wrap


class CompressionOptions(str, Enum):
    ZIP = 'zip'
    GZIP = 'gzip'


def derive_output_file_path(
        input_dir=os.path.join('input'),
        output_dir=os.path.join('output', 'zip'),
        root_dir=os.path.join('input', 'test_dir', 'test_dir_2')):
    '''
    input_dir: input/
    output_dir: output/zip/
    root_dir: input/test_dir/test_dir_2
    file_name: test_file_2.json

    expected_output_file: output/zip/test_dir/test_dir_2/test_file_2.json.zip
    '''
    common_input_path = os.path.commonprefix([input_dir, root_dir])
    inside_path = os.path.relpath(root_dir, common_input_path)
    output_file_path = os.path.join(output_dir, inside_path)
    return output_file_path


@timing
def compress_dir_files(source_dir, destination_dir,
                       method: type(CompressionOptions) = CompressionOptions.ZIP):

    for root_dir, _, files in os.walk(source_dir):
        for file in files:
            if not file.endswith('.json'):
                continue
            ext = '.' + method
            output_path = derive_output_file_path(source_dir, destination_dir, root_dir)
            os.makedirs(output_path, exist_ok=True)
            input_file = os.path.join(root_dir, file)
            output_file = os.path.join(output_path, file + ext)
            compression_func = zip_it if method == CompressionOptions.ZIP else gzip_it
            compression_func(input_file, output_file)


def decompress_dir_files(source_dir, destination_dir,
                         method: type(CompressionOptions) = None):

    for root_dir, _, files in os.walk(source_dir):
        for file in files:
            base_file_pieces = os.path.basename(file).split('.')
            file_ext = base_file_pieces[-1] if len(base_file_pieces) > 1 else ''
            compression_options = [x.value for x in CompressionOptions]
            if not file_ext or file_ext not in compression_options:
                continue
            if method in compression_options and file_ext != method:
                continue

            output_path = derive_output_file_path(source_dir, destination_dir, root_dir)
            os.makedirs(output_path, exist_ok=True)
            input_file = os.path.join(root_dir, file)
            output_file = os.path.join(output_path, '.'.join(base_file_pieces[:-1]))
            decompression_func = unzip_it if file_ext == CompressionOptions.ZIP else ungzip_it
            decompression_func(input_file, output_file)
