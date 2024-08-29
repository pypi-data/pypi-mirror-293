from typing import Optional, List

from thestage.entities.container import DockerContainerEntity
from thestage.services.clients.thestage_api.dtos.enums.container_status import ContainerBussinessStatusEnumDto, \
    ContainerFrontendStatusEnumDto
from thestage.services.clients.thestage_api.dtos.enums.container_pending_action import ContainerPendingActionEnumDto
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.i18n.translation import __
from thestage.services.container.container_service import ContainerService
from thestage.services.container.mapper.container_mapper import ContainerMapper
from thestage.helpers.logger.app_logger import app_logger
from thestage.controllers.utils_controller import validate_config_and_get_service_factory, get_current_directory

import typer

from thestage.services.logging.logging_service import LoggingService

app = typer.Typer(no_args_is_help=True, help=__("Help manage containers"))


@app.command(name='ls', help=__("List containers"))
def list_items(
        row: int = typer.Option(
            5,
            '--row',
            '-r',
            help=__("Number of rows per page"),
            is_eager=False,
        ),
        page: int = typer.Option(
            1,
            '--page',
            '-p',
            help=__("Page number"),
            is_eager=False,
        ),
        statuses: List[ContainerFrontendStatusEnumDto] = typer.Option(
            ["running", "starting"],
            '--status',
            '-s',
            help=__("Filter by status, use 'all' to list all containers"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Lists containers
    """
    app_logger.info(f'Start container lists from {get_current_directory()}')

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    typer.echo(__(
        "List containers with the following statuses: %statuses%. To view all containers, use --status=all)",
        placeholders={
            'statuses': ', '.join([item.value for item in statuses])
        }))

    real_statuses: List[str] = container_service.map_container_statuses(config=config, frontend=statuses)

    container_service.print(
        func_get_data=container_service.get_list,
        func_special_params={
            'statuses': real_statuses,
        },
        mapper=ContainerMapper(),
        config=config,
        headers=list(map(lambda x: x.alias, DockerContainerEntity.model_fields.values())),
        row=row,
        page=page,
        no_dialog=no_dialog,
        max_col_width=[10, 20, 30, 30, 30, 20, 20, 20],
        show_index="never",
    )

    typer.echo(__("Containers listing complete"))
    raise typer.Exit(0)


@app.command(name="info", help=__("Help get container details"))
def item_details(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Lists container details
    """
    app_logger.info(f'Start container details')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if not container:
        typer.echo(__("Container not found: %container_item%", {'container_item': str(container_slug) if container_slug else ''}))
        raise typer.Exit(1)

    typer.echo(__('CONTAINER DETAILS:'))
    typer.echo(__("STATUS: %status%", {'status': str(container.frontend_status.status_translation if container and container.frontend_status else 'UNKNOWN')}))
    typer.echo(__("UNIQUE ID: %slug%", {'slug': str(container.slug)}))
    typer.echo(__("TITLE: %title%", {'title': str(container.title)}))

    if container.instance_rented:
        typer.echo(
            __("RENTED INSTANCE UNIQUE ID: %instance_slug%", {'instance_slug': str(container.instance_rented.slug)})
        )
        typer.echo(
            __("RENTED INSTANCE STATUS: %instance_status%",
               {'instance_status': str(container.instance_rented.frontend_status.status_translation if container.instance_rented.frontend_status else 'UNKNOWN')})
        )

    if container.selfhosted_instance:
        typer.echo(
            __("SELF-HOSTED INSTANCE UNIQUE ID: %instance_slug%", {'instance_slug': str(container.selfhosted_instance.slug)})
        )
        typer.echo(
            __("SELF-HOSTED INSTANCE STATUS: %instance_status%",
               {'instance_status': str(container.selfhosted_instance.frontend_status.status_translation if container.selfhosted_instance.frontend_status else 'UNKNOWN')})
        )

    if container.mappings and (container.mappings.port_mappings or container.mappings.directory_mappings):
        if container.mappings.port_mappings:
            typer.echo(__("CONTAINER PORT MAPPING:"))
            for src, dest in container.mappings.port_mappings.items():
                typer.echo(f"    {src} : {dest}")

        if container.mappings.directory_mappings:
            typer.echo(__("CONTAINER DIRECTORY MAPPING:"))
            for src, dest in container.mappings.directory_mappings.items():
                typer.echo(f"    {src} : {dest}")

    typer.echo(__("Container details complete"))
    raise typer.Exit(0)


@app.command(name="connect", help=__("Help connect to container"))
def container_connect(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required if using self-hosted instance)"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Connects to container
    """
    app_logger.info(f'Connect to container')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_container_status_for_work(
            container=container
        )
        container_service.connect_container(
            config=config,
            container=container,
            no_dialog=no_dialog,
            username_param=username,
        )
    else:
        typer.echo(__("Container not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'Stop connect to container')
    raise typer.Exit(0)


@app.command(name="upload", help=__("Help copy file to container"))
def put_file(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        source_path: str = typer.Option(
            None,
            '--target-path',
            '-sp',
            help=__("Source file path"),
            is_eager=True,
        ),
        destination_path: Optional[str] = typer.Option(
            None,
            '--destination-path',
            '-dp',
            help=__("Destination directory path"),
            is_eager=False,
        ),
        is_recursive: bool = typer.Option(
            False,
            "--is-recursive",
            "-r",
            help=__("Enable recursive copying of directories"),
            is_eager=False,
        ),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required if using self-hosted instance)"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Uploads file to container
    """
    app_logger.info(f'Push file to container')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_container_status_for_work(
            container=container
        )

        container_service.put_file_to_container(
            container=container,
            src_path=source_path,
            destination_path=destination_path,
            is_folder=is_recursive,
            no_dialog=no_dialog,
            username_param=username,
        )
    else:
        typer.echo(__("Not found container - %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End send files to container')
    raise typer.Exit(0)


@app.command(name="download", help=__("Help copy file from container"))
def download_file(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        source_path: str = typer.Option(
            None,
            '--target-path',
            '-sp',
            help=__("Source file path"),
            is_eager=True,
        ),
        destination_path: Optional[str] = typer.Option(
            None,
            '--destination-path',
            '-dp',
            help=__("Destination directory path"),
            is_eager=False,
        ),
        is_recursive: bool = typer.Option(
            False,
            "--is-recursive",
            "-r",
            help=__("Enable recursive copying of directories"),
            is_eager=False,
        ),
        username: Optional[str] = typer.Option(
            None,
            '--username',
            '-u',
            help=__("Username for the server instance (required if using self-hosted instance)"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Downloads file from container
    """
    app_logger.info(f'Download file from container')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_container_status_for_work(
            container=container
        )

        container_service.get_file_from_container(
            container=container,
            src_path=source_path,
            destination_path=destination_path,
            is_folder=is_recursive,
            no_dialog=no_dialog,
            username_param=username,
        )
    else:
        typer.echo(__("Container not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End download files from container')
    raise typer.Exit(0)


@app.command(name="start", help=__("Help start container"))
def item_start(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Starts container
    """
    app_logger.info(f'Start container')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_container_status_for_start(
            container=container
        )
        result = container_service.change_container_status(
            config=config,
            container=container,
            action=ContainerPendingActionEnumDto.START
        )

        if result:
            typer.echo(__('Container is starting'))
        else:
            typer.echo(__('Error occurred on the server, please try again later'))
    else:
        typer.echo(__("NContainer not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End start container')
    raise typer.Exit(0)


@app.command(name="stop", help=__("Help stop container"))
def item_stop(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique ID"),
            is_eager=False,
        ),
        no_dialog: Optional[bool] = typer.Option(
            None,
            "--no-dialog",
            "-nd",
            help=__("Run with default values and skip any interactive prompts"),
            is_eager=False,
        ),
):
    """
        Stops container
    """
    app_logger.info(f'Stop container')

    if not container_slug:
        typer.echo(__('Container ID or container unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        container_service.check_container_status_for_stop(
            container=container
        )
        result = container_service.change_container_status(
            config=config,
            container=container,
            action=ContainerPendingActionEnumDto.STOP
        )

        if result:
            typer.echo(__('Container is stopping'))
        else:
            typer.echo(__('Error occurred on the server, please try again later'))
    else:
        typer.echo(__("Container not found: %container_item%", {'container_item': container_slug}))

    app_logger.info(f'End stop container')
    raise typer.Exit(0)


@app.command(name="logs", help=__("View container logs"))
def item_stop(
        container_slug: Optional[str] = typer.Option(
            None,
            '--container-uniqueid',
            '-uid',
            help=__("Container unique id"),
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
        View docker container logs
    """
    app_logger.info(f'View container logs')

    if not container_slug:
        typer.echo(__('Container Unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    container_service: ContainerService = service_factory.get_container_service()
    logging_service: LoggingService = service_factory.get_logging_service()

    container: Optional[DockerContainerDto] = container_service.get_item(
        config=config,
        container_slug=container_slug,
    )

    if container:
        logging_service.stream_container_logs(
            config=config,
            container=container
        )
    else:
        typer.echo(__("Not found container - %container_slug%", {'container_slug': container_slug}))

    app_logger.info(f'Container logs - end')
    raise typer.Exit(0)
