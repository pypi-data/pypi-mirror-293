from typing import Optional, List

from thestage.helpers.logger.app_logger import app_logger
from thestage.services.clients.thestage_api.dtos.enums.selfhosted_status import SelfHostedFrontendStatusEnumDto
from thestage.services.clients.thestage_api.dtos.enums.rented_status import RentedFrontendStatusEnumDto
from thestage.services.instance.mapper.instance_mapper import InstanceMapper
from thestage.services.instance.mapper.selfhosted_mapper import SelfHostedMapper
from thestage.services.instance.instance_service import InstanceService
from thestage.i18n.translation import __
from thestage.controllers.utils_controller import \
    validate_config_and_get_service_factory

import typer


app = typer.Typer(no_args_is_help=True, help=__("Help manage server instances"))

rented = typer.Typer(no_args_is_help=True, help=__("Help manage rented server instances"))
self_hosted = typer.Typer(no_args_is_help=True, help=__("Help manage self-hosted instances"))

app.add_typer(rented, name="rented")
app.add_typer(self_hosted, name="self-hosted")


@rented.command(name="ls", help=__("List rented server instances"))
def rented_list(
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
        statuses: List[RentedFrontendStatusEnumDto] = typer.Option(
            ["online", "creating", "terminating", "rebooting"],
            '--status',
            '-s',
            help=__("Filter by status, use 'all' to list all rented server instances"),
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
        Lists rented server instances
    """
    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    headers = [
        #'#',
        #'ID',
        'STATUS',
        'TITLE',
        'UNIQUE ID',
        'CPU TYPE',
        'CPU CORES',
        'GPU TYPE',
        'IP ADDRESS',
        'CREATED AT',
        'UPDATED AT',
    ]

    instance_service: InstanceService = service_factory.get_instance_service()

    typer.echo(__(
        "List rented server instances with the following statuses: %statuses%, to view all rented server instances, use --status=all",
        placeholders={
            'statuses': ', '.join([item.value for item in statuses])
        }))

    real_statuses: List[str] = instance_service.map_rented_statuses(config=config, frontend=statuses)

    instance_service.print(
        func_get_data=instance_service.get_rented_list,
        func_special_params={
            'statuses': real_statuses,
        },
        mapper=InstanceMapper(),
        config=config,
        headers=headers,
        row=row,
        page=page,
        no_dialog=no_dialog,
        show_index="never",
    )

    typer.echo(__("Rented server instances listing complete"))
    raise typer.Exit(0)


@rented.command(name="connect", help=__("Help connect to rented server instance"))
def instance_connect(
        instance_slug: Optional[str] = typer.Option(
            None,
            '--instance-uniqueid',
            '-uid',
            help=__("Rented server instance unique ID"),
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
        Connects to rented server instance
    """
    app_logger.info(f'Connect to rented server instance')

    if not instance_slug:
        typer.echo(__('Rented server instance unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()
    instance = instance_service.get_rented_item(config=config, instance_slug=instance_slug)

    if instance:
        instance_service.check_instance_status_to_connect(
            instance=instance,
        )
        instance_service.connect_to_instance(
            ip_address=instance.ip_address,
            username=instance.host_username,
        )
    else:
        typer.echo(__("Server instance not found: %instance_item%", {'instance_item': instance_slug}))

    app_logger.info(f'Stop connecting to rented server instance')
    raise typer.Exit(0)


@self_hosted.command(name="ls", help=__("List self-hosted instances"))
def self_hosted_list(
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
        statuses: List[SelfHostedFrontendStatusEnumDto] = typer.Option(
            ["awaiting_setup", "online", "terminated"],
            '--status',
            '-s',
            help=__("Filter by status, use 'all' to list all self-hosted server instances"),
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
        Lists self-hosted instances
    """
    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    headers = [
        # '#',
        # 'ID',
        'STATUS',
        'TITLE',
        'UNIQUE ID',
        'CPU TYPE',
        'CPU CORES',
        'GPU TYPE',
        'IP ADDRESS',
        'CREATED AT',
        'UPDATED AT'
    ]

    instance_service: InstanceService = service_factory.get_instance_service()

    typer.echo(__(
        "List self-hosted instances with the following statuses: %statuses%, to view all self-hosted instances, use --status=all",
        placeholders={
            'statuses': ', '.join([item.value for item in statuses])
        }))

    real_statuses: List[str] = instance_service.map_selfhosted_statuses(config=config, frontend=statuses)

    instance_service.print(
        func_get_data=instance_service.get_self_hosted_list,
        func_special_params={
            'statuses': real_statuses,
        },
        mapper=SelfHostedMapper(),
        config=config,
        headers=headers,
        row=row,
        page=page,
        no_dialog=no_dialog,
        show_index="never",
    )

    typer.echo(__("Self-hosted instances listing complete"))
    raise typer.Exit(0)


@self_hosted.command(name="connect", help=__("Help connect to self-hosted instance"))
def self_hosted_connect(
        instance_slug: Optional[str] = typer.Option(
            None,
            '--instance-uniqueid',
            '-uid',
            help=__("Self-hosted instance unique ID"),
            is_eager=False,
        ),
        username: Optional[str] = typer.Option(
            'root',
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
        Connects to self-hosted instance
    """
    app_logger.info(f'Connect to self-hosted instance')

    if not instance_slug:
        typer.echo(__('Self-hosted instance unique ID is required'))
        raise typer.Exit(1)

    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    instance_service: InstanceService = service_factory.get_instance_service()
    # rebuild to rented
    instance = instance_service.get_self_hosted_item(config=config, instance_slug=instance_slug)

    if instance:
        instance_service.check_selfhosted_status_to_connect(
            instance=instance,
        )

        if not username or not instance.host_username:
            typer.echo(__('User not found to connect to self-hosted instance'))
            raise typer.Exit(1)

        instance_service.connect_to_instance(
            ip_address=instance.ip_address,
            username=username or instance.host_username or 'root',
        )
    else:
        typer.echo(__("Server instance not found: %instance_item%", {'instance_item': instance_slug}))

    app_logger.info(f'Stop connecting to self-hosted instance')
    raise typer.Exit(0)
