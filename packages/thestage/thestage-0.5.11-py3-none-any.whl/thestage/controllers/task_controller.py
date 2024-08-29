from typing import Optional

from thestage.i18n.translation import __
from thestage.services.clients.thestage_api.dtos.enums.task_status import TaskStatus
from thestage.services.clients.thestage_api.dtos.task_controller.task_view_response import TaskViewResponse
from thestage.services.logging.logging_service import LoggingService
from thestage.helpers.logger.app_logger import app_logger
from thestage.controllers.utils_controller import validate_config_and_get_service_factory, get_current_directory

import typer

from thestage.services.task.task_service import TaskService

app = typer.Typer(no_args_is_help=True, help=__("Help with tasks"))


@app.callback()
def callback():
    pass

@app.command(name="logs", help=__("View task logs"))
def task_logs(
        task_id: Optional[int] = typer.Option(
            None,
            '--task-id',
            '-id',
            help=__("Task ID"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Start process with default values, without future dialog"),
            is_eager=False,
        ),
):
    """
        View task logs
    """
    app_logger.info(f'View task logs')

    if not task_id:
        typer.echo(__('Task ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    logging_service: LoggingService = service_factory.get_logging_service()

    logging_service.stream_task_logs(
        config=config,
        task_id=task_id
    )

    app_logger.info(f'Task logs - end')
    raise typer.Exit(0)
