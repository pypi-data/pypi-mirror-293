from typing import Optional, Dict, Tuple, List

from thestage.services.clients.thestage_api.dtos.enums.rented_status import RentedStatusEnumDto
from thestage.i18n.translation import __
from thestage.services.storage.mapper.storage_mapper import StorageMapper
from thestage.services.storage.storage_service import StorageService
from thestage.controllers.utils_controller import \
    validate_config_and_get_service_factory

import typer


app = typer.Typer(no_args_is_help=True, help=__("Help manage rented storages"))


@app.command(name="list")
def item_list(
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
        statuses: List[RentedStatusEnumDto] = typer.Option(
            ["RENTED"],
            '--status',
            '-s',
            help=__("Filter by status, use 'all' to list all rented storages"),
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
        Lists rented storages
    """
    service_factory = validate_config_and_get_service_factory(no_dialog=no_dialog)
    config = service_factory.get_config_provider().get_full_config()

    headers = ['#', 'SLUG', 'TITLE', 'PROVIDER ID', 'STATUS', 'IS ACTIVE', 'CREATED AT', 'UPDATED AT']

    storage_service: StorageService = service_factory.get_storage_service()

    typer.echo(__(
        "List rented storages with the following statuses: %statuses%, to view all rented storages, use --status=ALL",
        placeholders={
            'statuses': ', '.join([item.value for item in statuses])
        }))

    if RentedStatusEnumDto.find_special_status(statuses=statuses):
        statuses = []

    storage_service.print(
        func_get_data=storage_service.get_list,
        func_special_params={
            'statuses': statuses,
        },
        mapper=StorageMapper(),
        config=config,
        headers=headers,
        row=row,
        page=page,
        no_dialog=no_dialog,
    )

    typer.echo(__("Rented storages listing complete"))
    raise typer.Exit(0)
