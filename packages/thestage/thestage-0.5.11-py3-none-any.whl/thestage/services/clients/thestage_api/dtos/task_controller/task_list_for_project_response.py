from typing import List, Optional

from pydantic import Field, ConfigDict, BaseModel

from thestage.services.clients.thestage_api.dtos.base_response import TheStageBaseResponse
from thestage.services.clients.thestage_api.dtos.pagination_data import PaginationData
from thestage.services.task.dto.task_dto import TaskDto


class TaskListForProjectPaging(BaseModel):
    entities: List[TaskDto] = Field(default_factory=list, alias='entities')
    pagination_data: Optional[PaginationData] = Field(None, alias='paginationData')


class TaskListForProjectResponse(TheStageBaseResponse):
    model_config = ConfigDict(use_enum_values=True)

    tasks: TaskListForProjectPaging = Field(None, alias='tasks')
