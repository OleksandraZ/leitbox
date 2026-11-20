from datetime import date
from pathlib import Path

from leitbox import config
from leitbox.importers.csv_importer import read_cards
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService


def run(projects: ProjectService, decks: DeckService) -> None:
    while True:                                   
        print("Please choose:\n0) Quit  1) Create a project  2) List projects  3) Import a deck" )
        choice = input("> ").strip()

        if choice == "1":
            name = input("Name: ")
            try:
                project = projects.create_project(name)   
            except ValueError as error: 
                print(f"Not possible: {error}")
            else:
                print(f"Project {project.name} was created.")
        elif choice == "2":
            all_projects = projects.list_projects()
            today = date.today()
            if not all_projects:
                print("No projects yet.")
            for project in all_projects:
                print(f"- {project.name}")
                for deck in project.decks:
                    print(f"  {deck.name}: {deck.due_count(today)} due ({len(deck.cards)} cards)") 
        elif choice == "3":
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

        elif choice == "0":
            break                                
        else:
            print("Please choose 1, 2, 3 or 0.")
