from leitbox import config
from leitbox.cli.menu import run
from leitbox.domain.user import User
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService
from leitbox.storage.json_storage import JsonUserRepository


def main() -> None:
    repo = JsonUserRepository(config.DATA_FILE)
    if repo.get(config.DEFAULT_USER_ID) is None:          
        repo.save(User("me", user_id=config.DEFAULT_USER_ID))
    project_service = ProjectService(repo, config.DEFAULT_USER_ID)
    deck_service = DeckService(repo, config.DEFAULT_USER_ID)
    run(project_service, deck_service)


if __name__ == "__main__": 
    main()