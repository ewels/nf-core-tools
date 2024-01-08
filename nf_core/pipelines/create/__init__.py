"""A Textual app to create a pipeline."""
from textual.app import App
from textual.widgets import Button

from nf_core.pipelines.create.basicdetails import BasicDetails
from nf_core.pipelines.create.completed import Completed
from nf_core.pipelines.create.custompipeline import CustomPipeline
from nf_core.pipelines.create.error import ExistError
from nf_core.pipelines.create.finaldetails import FinalDetails
from nf_core.pipelines.create.githubexit import GithubExit
from nf_core.pipelines.create.githubrepo import GithubRepo
from nf_core.pipelines.create.githubrepoquestion import GithubRepoQuestion
from nf_core.pipelines.create.nfcorepipeline import NfcorePipeline
from nf_core.pipelines.create.pipelinetype import ChoosePipelineType
from nf_core.pipelines.create.utils import CreateConfig
from nf_core.pipelines.create.welcome import WelcomeScreen


class PipelineCreateApp(App[CreateConfig]):
    """A Textual app to manage stopwatches."""

    CSS_PATH = "create.tcss"
    TITLE = "nf-core create"
    SUB_TITLE = "Create a new pipeline with the nf-core pipeline template"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
    ]
    SCREENS = {
        "welcome": WelcomeScreen(),
        "basic_details": BasicDetails(),
        "choose_type": ChoosePipelineType(),
        "type_custom": CustomPipeline(),
        "type_nfcore": NfcorePipeline(),
        "final_details": FinalDetails(),
        "github_repo_question": GithubRepoQuestion(),
        "github_repo": GithubRepo(),
        "github_exit": GithubExit(),
        "completed_screen": Completed(),
        "error_screen": ExistError(),
    }

    # Initialise config as empty
    TEMPLATE_CONFIG = CreateConfig()

    # Initialise pipeline type
    PIPELINE_TYPE = None

    def on_mount(self) -> None:
        self.push_screen("welcome")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle all button pressed events."""
        if event.button.id == "start":
            self.switch_screen("choose_type")
        elif event.button.id == "type_nfcore":
            self.PIPELINE_TYPE = "nfcore"
            self.switch_screen("basic_details")
        elif event.button.id == "type_custom":
            self.PIPELINE_TYPE = "custom"
            self.switch_screen("basic_details")
        elif event.button.id == "continue":
            self.switch_screen("final_details")
        elif event.button.id == "github_repo":
            self.switch_screen("github_repo")
        elif event.button.id == "exit":
            self.switch_screen("github_exit")
        if event.button.id == "close_app":
            self.exit(return_code=0)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark: bool = not self.dark