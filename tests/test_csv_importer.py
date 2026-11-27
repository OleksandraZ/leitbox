from pathlib import Path

import pytest

from leitbox.importers.csv_importer import CsvImportError, read_cards


def write_csv(folder: Path, text: str, name: str = "cards.csv") -> Path:
    path = folder / name
    path.write_text(text, encoding="utf-8")
    return path


def test_rows_trimmed_in_order(tmp_path):
    text = """question,answer,note
sein,  to be  ,irregular
gehen,"to go, to walk",
können,"can, to be able to",modal
"""
    path = write_csv(tmp_path, text)
    result = read_cards(path, 1_000_000, 2000)

    assert result == [("sein", "to be"), ("gehen", "to go, to walk"), ("können", "can, to be able to")]

def test_file_with_bom_works(tmp_path):
    path = tmp_path / "cards.csv"
    path.write_text("question,answer\nsein,to be\n", encoding="utf-8-sig")

    assert read_cards(path, 1_000_000, 2000) == [("sein", "to be")]

def test_missing_file_is_refused(tmp_path):
    path = tmp_path / "missing.csv"

    with pytest.raises(CsvImportError, match="not found"):
        read_cards(path, 1_000_000, 2000)

def test_not_csv_file_is_refused(tmp_path):
    path = tmp_path / "cards.txt"
    path.write_text("question,answer\nsein,to be\n")

    with pytest.raises(CsvImportError, match="not a .csv"):
        read_cards(path, 1_000_000, 2000)

def test_file_bigger_than_max_bytes_is_refused(tmp_path):
    path = write_csv(tmp_path, "question,answer\nsein,to be\n")

    with pytest.raises(CsvImportError, match="bigger"):
        read_cards(path, 10, 2000)

def test_file_not_UTF_8_is_refused(tmp_path):
    path = tmp_path / "cards.csv"

    path.write_bytes(b"\xff\xfe\xfa")

    with pytest.raises(CsvImportError, match="UTF-8"):
        read_cards(path, 1_000_000, 2000)

def test_empty_file_is_refused(tmp_path):
    path = write_csv(tmp_path, "")

    with pytest.raises(CsvImportError, match="header"):
        read_cards(path, 1_000_000, 2000)

def test_file_with_wrong_header_is_refused(tmp_path):
    path = write_csv(tmp_path, "front,back\nsein,to be\n")

    with pytest.raises(CsvImportError, match="header"):
        read_cards(path, 1_000_000, 2000)

def test_file_with_wrong_row_is_refused(tmp_path):
    path = write_csv(tmp_path, "question,answer\nsein,to be\nhaben\n")

    with pytest.raises(CsvImportError, match="Row 3"):
        read_cards(path, 1_000_000, 2000)

def test_file_with_wrong_row2_is_refused(tmp_path):
    path = write_csv(tmp_path, "question,answer\nsein, \n")

    with pytest.raises(CsvImportError, match="Row 2"):
        read_cards(path, 1_000_000, 2000)

def test_file_with_no_cards_is_refused(tmp_path):
    path = write_csv(tmp_path, "question,answer\n")

    with pytest.raises(CsvImportError, match="no cards"):
        read_cards(path, 1_000_000, 2000)

def test_max_cards(tmp_path):
    text = """question,answer,note
sein,  to be  ,irregular
gehen,"to go, to walk",
können,"can, to be able to",modal
"""
    path = write_csv(tmp_path, text)
    with pytest.raises(CsvImportError, match="Too many cards"):
            read_cards(path, 1_000_000, 2)

def test_csv_import_error_is_a_value_error():
    assert issubclass(CsvImportError, ValueError)
