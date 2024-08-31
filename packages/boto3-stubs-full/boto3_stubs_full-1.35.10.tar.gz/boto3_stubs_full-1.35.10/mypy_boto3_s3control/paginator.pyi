"""
Type annotations for s3control service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_s3control.client import S3ControlClient
    from mypy_boto3_s3control.paginator import (
        ListAccessPointsForObjectLambdaPaginator,
    )

    session = Session()
    client: S3ControlClient = session.client("s3control")

    list_access_points_for_object_lambda_paginator: ListAccessPointsForObjectLambdaPaginator = client.get_paginator("list_access_points_for_object_lambda")
    ```
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef,
    ListAccessPointsForObjectLambdaResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListAccessPointsForObjectLambdaPaginator",)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListAccessPointsForObjectLambdaPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/paginators/#listaccesspointsforobjectlambdapaginator)
    """
    def paginate(
        self,
        **kwargs: Unpack[
            ListAccessPointsForObjectLambdaRequestListAccessPointsForObjectLambdaPaginateTypeDef
        ],
    ) -> _PageIterator[ListAccessPointsForObjectLambdaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3control.html#S3Control.Paginator.ListAccessPointsForObjectLambda.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_s3control/paginators/#listaccesspointsforobjectlambdapaginator)
        """
