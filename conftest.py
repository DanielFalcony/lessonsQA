import random
import string
from datetime import datetime

import yaml
import pytest
from hw_2_checkers import checkout


with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(f"mkdir {data['folder_in']} {data['folder_out']} {data['folder_ext']} {data['folder_ext2']}", "")


@pytest.fixture()
def clear_folders():
    return checkout(f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/* {data['folder_ext2']}/*", "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data['files_count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f"cd {data['folder_in']}; dd if=/dev/urandom of={filename} bs=1M count=1 iflag=fullblock", ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    sub_folder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f"cd {data['folder_in']}; mkdir {sub_folder_name}", ""):
        return None, None
    if not checkout(
            f"cd {data['folder_in']}/{sub_folder_name}; dd if=/dev/urandom of={test_file_name} bs=1M count=1 iflag=fullblock",
            ""):
        return sub_folder_name, None
    else:
        return sub_folder_name, test_file_name


@pytest.fixture(autouse=True)
def show_time():
    print(f"Start time: {datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')}")
    yield print(f"Stop time: {datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')}")
