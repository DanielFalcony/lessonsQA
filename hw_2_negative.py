from hw_2_checkers import checkout_negative, folder_out, folder_ext


def test_negative_step1():
    # test neg 1
    assert checkout_negative(f"cd {folder_out}; 7z e arx3.7z -o{folder_ext} -y", "ERROR"), "test1 FAIL"


def test_negative_step2():
    # test neg 1
    assert checkout_negative(f"cd {folder_out}; 7z x arx3.7z -o{folder_ext} -y", "ERROR"), "test1 FAIL"


def test_negative_step3():
    # test neg 2
    assert checkout_negative(f"cd {folder_out}; 7z t arx3.7z", "ERROR"), "test2 FAIL"
