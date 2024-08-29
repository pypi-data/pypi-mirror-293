"""
Type annotations for autoscaling-plans service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient
    from types_aiobotocore_autoscaling_plans.paginator import (
        DescribeScalingPlanResourcesPaginator,
        DescribeScalingPlansPaginator,
    )

    session = get_session()
    with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient

        describe_scaling_plan_resources_paginator: DescribeScalingPlanResourcesPaginator = client.get_paginator("describe_scaling_plan_resources")
        describe_scaling_plans_paginator: DescribeScalingPlansPaginator = client.get_paginator("describe_scaling_plans")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ApplicationSourceUnionTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("DescribeScalingPlanResourcesPaginator", "DescribeScalingPlansPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeScalingPlanResourcesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
    """

    def paginate(
        self,
        *,
        ScalingPlanName: str,
        ScalingPlanVersion: int,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeScalingPlanResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanresourcespaginator)
        """


class DescribeScalingPlansPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
    """

    def paginate(
        self,
        *,
        ScalingPlanNames: Sequence[str] = ...,
        ScalingPlanVersion: int = ...,
        ApplicationSources: Sequence[ApplicationSourceUnionTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[DescribeScalingPlansResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/paginators/#describescalingplanspaginator)
        """
