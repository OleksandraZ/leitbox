from leitbox.services.project_service import ProjectService


def run(service: ProjectService) -> None:
    while True:                                   
        print("\n1) Create a project  2) List projects  0) Quit")
        choice = input("> ").strip()

        if choice == "1":
            name = input("Name: ")
            try:
                project = service.create_project(name)   
            except ValueError as error: 
                print(f"Not possible: {error}")
            else:
                print(f"Project {project.name} was created.")
        elif choice == "2":
            projects = service.list_projects()
            if not projects:
                print("No projects yet.")
            for project in projects:
                print(f"- {project.name}")
        elif choice == "0":
            break                                
        else:
            print("Please choose 1, 2 or 0.")
