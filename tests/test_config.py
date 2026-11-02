from leitbox import config

def test_five_intervals():
    assert len(config.INTERVALS) == 5

def test_data_dir_is_absolute_and_named_data():
    assert config.DATA_DIR.is_absolute()
    assert config.DATA_DIR.name == "data"
    