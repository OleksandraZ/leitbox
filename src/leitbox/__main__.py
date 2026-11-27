from leitbox import config
from leitbox.cli.menu import run
from leitbox.domain.scheduler import Scheduler
from leitbox.domain.user import User
from leitbox.services.deck_service import DeckService
from leitbox.services.project_service import ProjectService
from leitbox.services.study_service import StudyService
from leitbox.storage.json_storage import JsonReviewRepository, JsonUserRepository


def main() -> None:
    try:
        repo = JsonUserRepository(config.DATA_FILE)
        if repo.get(config.DEFAULT_USER_ID) is None:
            repo.save(User("me", user_id=config.DEFAULT_USER_ID))
        project_service = ProjectService(repo, config.DEFAULT_USER_ID)
        deck_service = DeckService(repo, config.DEFAULT_USER_ID)
        reviews = JsonReviewRepository(config.DATA_FILE)
        study_service = StudyService(repo, reviews, Scheduler(config.INTERVALS), config.DEFAULT_USER_ID)

        try:
            run(project_service, deck_service, study_service)
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
    except ValueError as error:
        print(f"Can't start: {error}")


if __name__ == "__main__":
    main()
