import os
import threading
import time
from typing import Tuple

from IPython.display import HTML, clear_output, display
from ipywidgets import widgets
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from sidecar import Sidecar

from finter.framework_model.submission.config import get_model_info
from finter.framework_model.submission.helper_notebook import NotebookExtractor
from finter.framework_model.submission.helper_path import FileManager
from finter.framework_model.submission.helper_poetry import prepare_docker_submit_files
from finter.framework_model.submission.helper_position import load_model_instance
from finter.framework_model.submission.helper_submission import submit_model
from finter.framework_model.submission.helper_ui import MAC_STYLE
from finter.framework_model.submission.notebook import name_exist
from finter.framework_model.validation import ValidationHelper
from finter.settings import logger
from finter.utils.timer import timer


class JupyterLabSubmission(NotebookExtractor):
    def __init__(
        self,
        model_name: str = None,
        model_universe: str = None,
        docker: bool = None,
        direct: bool = False,
        overwrite: bool = False,  # 새로운 파라미터 추가
    ):
        super().__init__()

        # 만약 인자가 전달되지 않았다면 기본값 설정
        self.default_modelname = model_name if model_name is not None else ""
        self.default_model_universe = (
            model_universe if model_universe is not None else "kr_stock"
        )
        self.default_docker = docker if docker is not None else True
        self.direct = direct
        self.overwrite = overwrite  # 새로운 속성 추가

        self.setup_ui()
        self.register_event_handlers()
        self.update_info_display()

        if direct:
            self.direct_submit(model_name, model_universe, docker)

    def direct_submit(self, model_name: str, model_universe: str, docker: bool):
        if (model_name is None) or (model_universe is None) or (docker is None):
            raise ValueError(
                "Model name, universe and docker must be provided for direct submit."
            )

        self.model_name_input.value = model_name
        self.model_universe_dropdown.value = model_universe
        self.docker_checkbox.value = docker

        # Simulate clicking the submit button
        self.on_submit(None)

    def setup_ui(self):
        self.setup_sidecar()
        self.create_widgets()
        self.setup_layout()

    def setup_sidecar(self):
        self.sidecar = Sidecar(title="Submission Dashboard")

    def create_widgets(self):
        self.model_name_input, self.model_universe_dropdown = (
            self.create_input_widgets()
        )
        self.docker_checkbox = widgets.Checkbox(
            value=self.default_docker,
            description="Use Docker",
            disabled=False,
            indent=False,
        )

        self.title = self.create_title_widget()
        self.code_display = self.create_code_display_widget()

        self.status_output = widgets.Output()
        (
            self.submit_button,
            self.cancel_button,
            self.position_button,
            self.simulation_button,
            self.progress,
        ) = self.create_action_widgets()
        self.refresh_button = widgets.Button(
            description="Refresh",
            button_style="info",
            layout=widgets.Layout(width="auto", margin="0 5px"),
        )

    def setup_layout(self):
        layout = widgets.VBox(
            [
                self.title,
                widgets.HBox(
                    [self.model_name_input, self.model_universe_dropdown],
                    layout=widgets.Layout(margin="0"),
                ),
                widgets.HBox(
                    [self.docker_checkbox],
                    layout=widgets.Layout(margin="0"),
                ),
                self.create_action_layout(),
                self.status_output,
                self.code_display,
            ],
            layout=widgets.Layout(padding="20px"),
        )
        self.sidecar.clear_output()
        with self.sidecar:
            display(layout)

    def register_event_handlers(self):
        self.model_name_input.observe(self.on_modelname_change, names="value")
        self.model_universe_dropdown.observe(self.on_modelname_change, names="value")
        self.submit_button.on_click(self.on_submit)
        self.cancel_button.on_click(self.on_cancel)
        self.refresh_button.on_click(self.on_refresh)

    def create_title_widget(self) -> widgets.HTML:
        return widgets.HTML(
            value="<h1 style='text-align:center; color:#4A90E2; padding:10px;'>Submission Dashboard</h1>"
        )

    def create_code_display_widget(self) -> widgets.HTML:
        code_display = widgets.HTML()
        self.update_code_display(code_display, "")
        return code_display

    def create_input_widgets(self) -> Tuple[widgets.Text, widgets.Dropdown]:
        modelname_input = widgets.Text(
            value=self.default_modelname,
            description="Model Name:",
            placeholder="Enter model name (eg. directory/name)",
            layout=widgets.Layout(width="50%", margin="0 10px 0 0"),
        )
        model_universe_dropdown = widgets.Dropdown(
            options=["kr_stock", "us_stock", "us_etf", "vn_stock"],
            value=self.default_model_universe,
            description="Universe:",
            layout=widgets.Layout(width="50%", margin="0 0 0 10px"),
        )
        return modelname_input, model_universe_dropdown

    def create_action_widgets(
        self,
    ) -> Tuple[
        widgets.Button,
        widgets.Button,
        widgets.Button,
        widgets.Button,
        widgets.IntProgress,
    ]:
        button_layout = widgets.Layout(width="auto", margin="0 5px")
        submit_button = widgets.Button(
            description="Submit",
            button_style="primary",
            layout=button_layout,
        )
        cancel_button = widgets.Button(
            description="Cancel",
            button_style="danger",
            layout=button_layout,
        )
        position_button = widgets.Button(
            description="Position",
            # button_style="info",
            layout=button_layout,
        )
        position_button.on_click(self.on_position_click)

        simulation_button = widgets.Button(
            description="Simulation",
            # button_style="warning",
            layout=button_layout,
        )
        simulation_button.on_click(self.on_simulation_click)

        progress = widgets.IntProgress(
            value=0,
            min=0,
            max=100,
            description="Loading:",
            bar_style="info",
            orientation="horizontal",
            layout=widgets.Layout(width="100%", margin="10px 0"),
        )

        for button in [
            submit_button,
            cancel_button,
            position_button,
            simulation_button,
        ]:
            button.add_class("widget-button")

        return (
            submit_button,
            cancel_button,
            position_button,
            simulation_button,
            progress,
        )

    def create_action_layout(self) -> widgets.VBox:
        button_box = widgets.HBox(
            [
                self.submit_button,
                self.cancel_button,
                self.position_button,
                self.simulation_button,
                self.refresh_button,
            ],
            layout=widgets.Layout(
                justify_content="flex-start", align_items="center", margin="0"
            ),
        )
        return widgets.VBox(
            [button_box, self.progress], layout=widgets.Layout(margin="0")
        )

    def on_modelname_change(self, change):
        self.update_info_display()

    def colored_print(self, text: str, color: str):
        with self.status_output:
            display(HTML(f"<p style='color: {color};'>{text}</p>"))

    def update_info_display(self):
        modelname = self.model_name_input.value

        self.status_output.clear_output()
        if (
            modelname.startswith("/")
            or " " in modelname
            or "." in modelname
            or modelname.strip() == ""
        ):
            self.colored_print(
                "Error: Model name cannot start with '/' or contain spaces or '.'.",
                "red",
            )
        else:
            output_path = os.path.join(os.getcwd(), modelname, self.model_file_name)
            self.colored_print(f"Model will be saved to: {output_path}", "green")

        self.update_code_display(
            self.code_display,
            (
                output_path + f" ({self.model_type.lower()})"
                if "output_path" in locals()
                else ""
            ),
        )

    def update_code_display(self, code_display: widgets.HTML, file_path: str):
        formatter = HtmlFormatter(style="monokai")
        highlighted_code = highlight(self.model_cell.source, PythonLexer(), formatter)

        style = (
            MAC_STYLE + "<style>" + formatter.get_style_defs(".highlight") + "</style>"
        )
        html_content = f"""
        {style}
        <div class="mac-window" style="margin-top: 20px;">
            <div class="mac-titlebar">
                <div class="mac-buttons">
                    <div class="mac-button mac-close"></div>
                    <div class="mac-button mac-minimize"></div>
                    <div class="mac-button mac-zoom"></div>
                </div>
                <div class="mac-title" style="text-align: center; color: #fff; padding: 5px;">
                    {' '+file_path}
                </div>
            </div>
            <div class="mac-content" style="padding: 10px;">
                {highlighted_code}
            </div>
        </div>
        """
        code_display.value = html_content

    def on_submit(self, b):
        self.status_output.clear_output()
        with self.status_output:
            print("Submission preparation...")
        self.set_button_states(submit_disabled=True, cancel_disabled=True)
        self.progress.value = 0

        try:
            self.start_progress()
            self.save_model_and_load_instance()
            self.submit_model()
        except Exception as e:
            self.handle_submission_error(e)
        finally:
            self.set_button_states(submit_disabled=False, cancel_disabled=False)

    def check_name_exist(self) -> bool:
        return name_exist(
            self.model_type,
            self.model_universe_dropdown.value,
            self.model_name_input.value,
        )

    def save_model_and_load_instance(self):
        self.output_path = os.path.join(
            os.getcwd(), self.model_name_input.value, self.model_file_name
        )

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        self.write_notebook(self.output_path)
        with self.status_output:
            print(f"Notebook saved to {self.output_path}")

        path_manager = FileManager()
        path_manager.clear_paths()
        self.model_instance = load_model_instance(self.output_path, self.model_type)
        path_manager.copy_files_to(self.model_name_input.value)

    def submit_model(self):
        self.model_info = get_model_info(
            self.model_universe_dropdown.value,
            self.model_type,
        )
        with self.status_output:
            print(
                f"Name: {self.model_name_input.value}, Universe: {self.model_universe_dropdown.value}, Type: {self.model_type.lower()}"
            )

        if self.check_name_exist():
            if self.overwrite:
                self.colored_print("Warning: Overwriting existing model.", "orange")
                self.proceed_with_submission()
            else:
                self.show_overwrite_dialog()
        else:
            self.proceed_with_submission()

    def show_overwrite_dialog(self):
        # self.status_output.clear_output()
        with self.status_output:
            print("Model name already exists. Do you want to overwrite?")
            overwrite_button = widgets.Button(
                description="Overwrite", button_style="warning"
            )
            cancel_button = widgets.Button(description="Cancel", button_style="danger")

            overwrite_button.on_click(lambda _: self.proceed_with_submission())
            cancel_button.on_click(lambda _: self.cancel_submission())

            display(widgets.HBox([overwrite_button, cancel_button]))
            self.progress.value = 100
            self.progress.bar_style = "danger"

    def proceed_with_submission(self):
        self.start_progress()

        with self.status_output:
            print("Submission started...")

            if self.docker_checkbox.value:
                prepare_docker_submit_files(self.model_name_input.value)

            # Perform validation
            try:
                validator = ValidationHelper(
                    model_path=self.model_name_input.value, model_info=self.model_info
                )
                validator.validate()
            except Exception as e:
                self.handle_submission_error("", raise_error=True)

            # Todo insample, benchmark
            submit_result = submit_model(
                model_info=self.model_info,
                output_directory=self.model_name_input.value,
                docker_submit=self.docker_checkbox.value,
                staging=False,
            )
            if submit_result is None:
                self.handle_submission_error("Error submitting the model.")
            else:
                self.progress.value = 100
                print("Submission completed!")
                print(f"Model ID: {submit_result.result['identity_name']}")
                print("Validation is in progress on the server.")
                display(
                    HTML(
                        f'<a href="{submit_result.s3_url}" target="_blank">Validation URL</a>'
                    )
                )

    def cancel_submission(self):
        self.status_output.clear_output()
        self.colored_print("Submission cancelled.", "orange")

    def handle_submission_error(self, error: Exception, raise_error: bool = False):
        self.progress.bar_style = "danger"
        self.progress.value = 100
        self.colored_print(f"\nSubmission failed: {str(error)}", "red")
        if raise_error:
            raise

    def on_cancel(self, b):
        self.sidecar.close()
        # with self.status_output:
        # clear_output(wait=True)
        # self.colored_print("Submission cancelled.", "orange")

    def set_button_states(self, submit_disabled: bool, cancel_disabled: bool):
        self.submit_button.disabled = submit_disabled
        self.cancel_button.disabled = cancel_disabled

    def start_progress(self):
        self.progress.value = 0
        self.progress.bar_style = "info"

        def progress_animation():
            direction = 1
            while True:
                self.progress.value += direction

                if self.progress.value > 95:
                    self.progress.value = 100
                    direction = 0
                    break

                if self.progress.value >= 90:
                    direction = -1
                elif self.progress.value <= 80:
                    direction = 1

                time.sleep(0.1)

        thread = threading.Thread(target=progress_animation)
        thread.start()

    def on_refresh(self, b):
        self.status_output.clear_output()
        self.colored_print("Refreshing... Clearing cache and reinitializing.", "blue")
        # Clear cache logic here if needed
        self.__init__(
            self.model_name_input.value,
            self.model_universe_dropdown.value,
            self.docker_checkbox.value,
        )  # Reinitialize

    def on_position_click(self, b):
        self.status_output.clear_output()
        with self.status_output:
            print(
                """
   _____          _ _   _             _             
  |  __ \        (_) | (_)           (_)            
  | |__) |__  ___ _| |_ _  ___  _ __  _ _ __   __ _ 
  |  ___/ _ \/ __| | __| |/ _ \| '_ \| | '_ \ / _` |
  | |  | (_) \__ \ | |_| | (_) | | | | | | | | (_| |
  |_|   \___/|___/_|\__|_|\___/|_| |_|_|_| |_|\__, |
                                               __/ |
                                              |___/ 
Oh, you want Position? It's still under construction!
=================================================="""
            )
        self.position = "Not Implemented"

    def on_simulation_click(self, b):
        self.status_output.clear_output()
        with self.status_output:
            print(
                """
   _____ _                 _       _   _             
  / ____(_)               | |     | | (_)            
 | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  
  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \ 
  ____) | | | | | | | |_| | | (_| | |_| | (_) | | | |
 |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|
                                                     
Simulation, you say? Hold your horses, we're working on it!
==========================================================="""
            )
        self.simulation = "Not Implemented"
