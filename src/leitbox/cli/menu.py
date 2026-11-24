from datetime import date, datetime
from pathlib import Path

from leitbox import config
from leitbox.importers.csv_importer import read_cards
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService
from leitbox.services.study_service import StudyService


def run(projects: ProjectService, decks: DeckService, study: StudyService) -> None:
    while True:
        print("Please choose:\n0) Quit  1) Create a project  2) List projects  3) Import a deck  4) Study a deck" )
        choice = input("> ").strip()
        if choice == "1":   
            create_project(projects)
        elif choice == "2": 
            list_projects(projects)
        elif choice == "3": 
            import_deck(decks)
        elif choice == "4": 
            study_deck(study)
        elif choice == "0": 
            break
        else:               
            print("Please choose 1, 2, 3, 4 or 0.")


def ask_reply() -> str:
    reply = input("Did you know it? (y)es / (n)o / (q)uit: ").strip().lower()
    while reply not in ("y", "n", "q"):
        reply = input("Please type y, n or q: ").strip().lower()
    return reply

def create_project(projects: ProjectService) -> None:
    name = input("Name: ")
    try:
        project = projects.create_project(name)   
    except ValueError as error: 
        print(f"Not possible: {error}")
    else:
        print(f"Project {project.name} was created.")

def list_projects(projects: ProjectService) -> None: 
    all_projects = projects.list_projects()
    today = date.today()
    if not all_projects:
        print("No projects yet.")
    for project in all_projects:
        print(f"- {project.name}")
        for deck in project.decks:
            print(f"  {deck.name}: {deck.due_count(today)} due ({len(deck.cards)} cards)") 

def import_deck(decks: DeckService) -> None: 
    project_name = input("Project name: ")
    deck_name = input("Deck name: ")
    file_path = input("File path: ")
    try:
        rows = read_cards(Path(file_path.strip()).expanduser(), config.MAX_IMPORT_BYTES, config.MAX_IMPORT_CARDS)
        deck = decks.import_deck(project_name, deck_name, rows, date.today())
    except ValueError as error:
        print(f"Not possible: {error}")
    else:
        print (f"Imported {len(deck.cards)} cards into deck {deck.name}.")
    
def study_deck(study: StudyService) -> None: 
    project_name = input("Project name: ")
    deck_name = input("Deck name: ")
    today = datetime.now().astimezone().date()
    try:
        cards = study.due_cards(project_name, deck_name, today)
    except ValueError as error:
        print(f"Not possible: {error}")
        return
                                     
    
    if not cards:                                  
        next_date = study.next_due(project_name, deck_name)
        if next_date is None: 
            print("Nothing to study: all cards are retired.")
        else: 
            print(f"Nothing due. Next card on {next_date}.")
        return
    
    knew = 0
    didnt = 0
    for card in cards:
        mark = " (overdue)" if card.is_overdue(today) else ""      
        print(f"\nQuestion{mark}: {card.question}")
        input("Press Enter to see the answer...")                   
        print(f"Answer: {card.answer}")
        reply = ask_reply()
        if reply == "q":
            break                                 
        study.answer(card.id, reply == "y", datetime.now().astimezone())
        if reply == "y":
            knew += 1 
        elif reply == "n":
            didnt += 1
    print(f"Done: {knew} known, {didnt} not known.")
    
