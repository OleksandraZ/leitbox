import csv
from pathlib import Path


class CsvImportError(ValueError):
    """Any error with the .csv import"""
    

def read_cards(path: Path, max_bytes: int, max_cards: int) -> list[tuple[str, str]]:
    if not path.exists():               
        raise CsvImportError(f"File not found: {path}")
    if path.suffix.lower() != ".csv":   
        raise CsvImportError(f"{path.name} is not a .csv file")
    if path.stat().st_size > max_bytes:
        raise CsvImportError(f"{path.name} is bigger than {max_bytes} bytes.")

    cards = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None or not {"question", "answer"}.issubset(reader.fieldnames):
                raise CsvImportError("The header must contain: question, answer")

            for row_number, row in enumerate(reader, start=2):
                question = row["question"]
                answer = row["answer"]
                if question is None or answer is None:          
                    raise CsvImportError(f"Row {row_number}: a column is missing")
                question = question.strip()
                answer = answer.strip()
                if not question or not answer:
                    raise CsvImportError(f"Row {row_number}: question and answer must not be empty")
                cards.append((question, answer)) 
    except UnicodeDecodeError:
        raise CsvImportError(f"{path.name} is not a UTF-8 text file") from None

                    
    if not cards:
        raise CsvImportError("The file has no cards")
    if len(cards) > max_cards:
        raise CsvImportError(f"Too many cards: {len(cards)} (max {max_cards})")
    return cards
        
