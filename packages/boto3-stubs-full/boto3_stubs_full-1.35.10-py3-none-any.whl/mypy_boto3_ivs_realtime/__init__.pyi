"""
Main interface for ivs-realtime service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivs_realtime import (
        Client,
        IvsrealtimeClient,
        ListPublicKeysPaginator,
    )

    session = Session()
    client: IvsrealtimeClient = session.client("ivs-realtime")

    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    ```
"""

from .client import IvsrealtimeClient
from .paginator import ListPublicKeysPaginator

Client = IvsrealtimeClient

__all__ = ("Client", "IvsrealtimeClient", "ListPublicKeysPaginator")
