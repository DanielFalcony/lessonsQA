import random
import string
import subprocess
import yaml
import pytest


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def checkout_negative(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def take_data(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    return result.stdout


@pytest.fixture()
def make_folders():
    return checkout(f"mkdir {data['folder_in']} {data['folder_out']} {data['folder_ext']} {data['folder_ext2']}", "")


@pytest.fixture()
def clear_folders():
    return checkout(f"rm -rf {data['folder_in']}/* {data['folder_out']}/* {data['folder_ext']}/* {data['folder_ext2']}/*", "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(5):
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
