from typing import List, Optional

from pydantic import Field, ConfigDict, BaseModel

from thestage.services.clients.thestage_api.dtos.base_response import TheStageBaseResponse
from thestage.services.clients.thestage_api.dtos.container_response import DockerContainerDto
from thestage.services.clients.thestage_api.dtos.pagination_data import PaginationData


class DockerContainerListPaging(BaseModel):
    entities: List[DockerContainerDto] = Field(default_factory=list, alias='entities')
    pagination_data: Optional[PaginationData] = Field(None, alias='paginationData')


class DockerContainerListResponse(TheStageBaseResponse):
    model_config = ConfigDict(use_enum_values=True)

    paginatedList: DockerContainerListPaging = Field(None, alias='paginatedList')
