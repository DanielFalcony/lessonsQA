from hw_2_checkers import (checkout, take_data)
from conftest import data


class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        # test Add files to archive
        res1 = checkout(f"cd {data['folder_in']}; 7z a {data['folder_out']}/arx2", "Everything is Ok")
        res2 = checkout(f"ls {data['folder_out']}", "arx2.7z")
        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test check hash sum with CRC32 and 7z h
        res = []
        for item in make_files:
            res.append(checkout(f"cd {data['folder_in']}; 7z h {item}", "Everything is Ok"))
            hash_date_crc32 = str(take_data(f"cd {data['folder_in']}; crc32 {item}")).upper()
            res.append(checkout(f"cd {data['folder_in']}; 7z h {item}", hash_date_crc32))
        assert all(res), "test2 FAIL"

    def test_step3(self, clear_folders, make_files):
        # test List contents of archive
        res = []
        res.append(checkout(f"cd {data['folder_in']}; 7z a {data['folder_out']}/arx2", "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f"cd {data['folder_out']}; 7z l arx2.7z", item))
        assert all(res), "test3 FAIL"

    def test_step4(self, clear_folders, make_files):
        # test Extract files from archive (without using directory names)
        res = []
        res.append(checkout(f"cd {data['folder_in']}; 7z a {data['folder_out']}/arx2", "Everything is Ok"))
        res.append(checkout(f"cd {data['folder_out']}; 7z e arx2.7z -o{data['folder_ext']} -y", "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f"ls {data['folder_ext']}", item))
        assert all(res), "test2 FAIL"

    def test_step5(self, clear_folders, make_files, make_subfolder):
        # test eXtract files with full paths
        res = []
        res.append(checkout(f"cd {data['folder_in']}; 7z a {data['folder_out']}/arx", "Everything is Ok"))
        res.append(checkout(f"cd {data['folder_out']}; 7z x arx.7z -o{data['folder_ext2']} -y", "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f"ls {data['folder_ext2']}", item))
        res.append(checkout(f"ls {data['folder_ext2']}", make_subfolder[0]))
        res.append(checkout(f"ls {data['folder_ext2']}", make_subfolder[0]))
        assert all(res), "test5 FAIL"

    def test_step6(self):
        # Test integrity of archive
        assert checkout(f"cd {data['folder_out']}; 7z t arx.7z", "Everything is Ok"), "test3 FAIL"

    def test_step7(self):
        # test Update files to archive
        assert checkout(f"cd {data['folder_in']}; 7z u arx.7z", "Everything is Ok"), "test4 FAIL"

    def test_step8(self):
        # test Delete files from archive
        assert checkout(f"cd {data['folder_out']}; 7z d arx.7z", "Everything is Ok"), "test5 FAIL"

    def test_step9(self, clear_folders):
        # delite all files in folders and check it
        res = [data['folder_in'], data['folder_out'], data['folder_ext'], data['folder_ext2']]
        checkout_clean = []
        for item in res:
            iter_step = checkout(f"cd {item}; ls -l", "total 0"), f"Here some files, {item} FAIL"
            checkout_clean.append(iter_step[0])
        assert all(checkout_clean), "test9 FAIL"
