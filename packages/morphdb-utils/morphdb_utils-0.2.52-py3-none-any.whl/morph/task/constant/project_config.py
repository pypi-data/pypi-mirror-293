import os


class ProjectConfig:
    # Directories
    INIT_DIR = os.path.expanduser("~/.morph")
    RUNS_DIR = os.path.expanduser("~/.morph/runs")
    CANVAS_DIR = "canvases"
    PUBLIC_DIR = "_public"
    PRIVATE_DIR = "_private"
    # Files
    MORPH_CRED_PATH = os.path.expanduser("~/.morph/credentials")
    # TODO: delete MORPH_YAML in future
    MORPH_YAML = "morph.yaml"
    MORPH_PROJECT_DB = "morph_project.sqlite3"
    MORPH_PROFILE_PATH = os.path.expanduser("~/.morph/profiles.yaml")
    # Others
    EXECUTABLE_EXTENSIONS = [".sql", ".py"]
