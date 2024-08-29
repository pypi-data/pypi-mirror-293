"""
Type annotations for iotfleetwise service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iotfleetwise.client import IoTFleetWiseClient
    from types_aiobotocore_iotfleetwise.paginator import (
        GetVehicleStatusPaginator,
        ListCampaignsPaginator,
        ListDecoderManifestNetworkInterfacesPaginator,
        ListDecoderManifestSignalsPaginator,
        ListDecoderManifestsPaginator,
        ListFleetsPaginator,
        ListFleetsForVehiclePaginator,
        ListModelManifestNodesPaginator,
        ListModelManifestsPaginator,
        ListSignalCatalogNodesPaginator,
        ListSignalCatalogsPaginator,
        ListVehiclesPaginator,
        ListVehiclesInFleetPaginator,
    )

    session = get_session()
    with session.create_client("iotfleetwise") as client:
        client: IoTFleetWiseClient

        get_vehicle_status_paginator: GetVehicleStatusPaginator = client.get_paginator("get_vehicle_status")
        list_campaigns_paginator: ListCampaignsPaginator = client.get_paginator("list_campaigns")
        list_decoder_manifest_network_interfaces_paginator: ListDecoderManifestNetworkInterfacesPaginator = client.get_paginator("list_decoder_manifest_network_interfaces")
        list_decoder_manifest_signals_paginator: ListDecoderManifestSignalsPaginator = client.get_paginator("list_decoder_manifest_signals")
        list_decoder_manifests_paginator: ListDecoderManifestsPaginator = client.get_paginator("list_decoder_manifests")
        list_fleets_paginator: ListFleetsPaginator = client.get_paginator("list_fleets")
        list_fleets_for_vehicle_paginator: ListFleetsForVehiclePaginator = client.get_paginator("list_fleets_for_vehicle")
        list_model_manifest_nodes_paginator: ListModelManifestNodesPaginator = client.get_paginator("list_model_manifest_nodes")
        list_model_manifests_paginator: ListModelManifestsPaginator = client.get_paginator("list_model_manifests")
        list_signal_catalog_nodes_paginator: ListSignalCatalogNodesPaginator = client.get_paginator("list_signal_catalog_nodes")
        list_signal_catalogs_paginator: ListSignalCatalogsPaginator = client.get_paginator("list_signal_catalogs")
        list_vehicles_paginator: ListVehiclesPaginator = client.get_paginator("list_vehicles")
        list_vehicles_in_fleet_paginator: ListVehiclesInFleetPaginator = client.get_paginator("list_vehicles_in_fleet")
    ```
"""

from typing import AsyncIterator, Generic, Iterator, Sequence, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .literals import SignalNodeTypeType
from .type_defs import (
    GetVehicleStatusResponseTypeDef,
    ListCampaignsResponseTypeDef,
    ListDecoderManifestNetworkInterfacesResponseTypeDef,
    ListDecoderManifestSignalsResponseTypeDef,
    ListDecoderManifestsResponseTypeDef,
    ListFleetsForVehicleResponseTypeDef,
    ListFleetsResponseTypeDef,
    ListModelManifestNodesResponseTypeDef,
    ListModelManifestsResponseTypeDef,
    ListSignalCatalogNodesResponseTypeDef,
    ListSignalCatalogsResponseTypeDef,
    ListVehiclesInFleetResponseTypeDef,
    ListVehiclesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "GetVehicleStatusPaginator",
    "ListCampaignsPaginator",
    "ListDecoderManifestNetworkInterfacesPaginator",
    "ListDecoderManifestSignalsPaginator",
    "ListDecoderManifestsPaginator",
    "ListFleetsPaginator",
    "ListFleetsForVehiclePaginator",
    "ListModelManifestNodesPaginator",
    "ListModelManifestsPaginator",
    "ListSignalCatalogNodesPaginator",
    "ListSignalCatalogsPaginator",
    "ListVehiclesPaginator",
    "ListVehiclesInFleetPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class GetVehicleStatusPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.GetVehicleStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
    """

    def paginate(
        self, *, vehicleName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[GetVehicleStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.GetVehicleStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#getvehiclestatuspaginator)
        """

class ListCampaignsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListCampaigns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
    """

    def paginate(
        self, *, status: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListCampaignsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListCampaigns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listcampaignspaginator)
        """

class ListDecoderManifestNetworkInterfacesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDecoderManifestNetworkInterfacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifestNetworkInterfaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestnetworkinterfacespaginator)
        """

class ListDecoderManifestSignalsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifestSignals)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDecoderManifestSignalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifestSignals.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestsignalspaginator)
        """

class ListDecoderManifestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
    """

    def paginate(
        self, *, modelManifestArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListDecoderManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListDecoderManifests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listdecodermanifestspaginator)
        """

class ListFleetsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListFleets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListFleetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListFleets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetspaginator)
        """

class ListFleetsForVehiclePaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListFleetsForVehicle)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
    """

    def paginate(
        self, *, vehicleName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListFleetsForVehicleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListFleetsForVehicle.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listfleetsforvehiclepaginator)
        """

class ListModelManifestNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListModelManifestNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
    """

    def paginate(
        self, *, name: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListModelManifestNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListModelManifestNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestnodespaginator)
        """

class ListModelManifestsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListModelManifests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
    """

    def paginate(
        self, *, signalCatalogArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListModelManifestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListModelManifests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listmodelmanifestspaginator)
        """

class ListSignalCatalogNodesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListSignalCatalogNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
    """

    def paginate(
        self,
        *,
        name: str,
        signalNodeType: SignalNodeTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListSignalCatalogNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListSignalCatalogNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalognodespaginator)
        """

class ListSignalCatalogsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListSignalCatalogs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListSignalCatalogsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListSignalCatalogs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listsignalcatalogspaginator)
        """

class ListVehiclesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListVehicles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
    """

    def paginate(
        self,
        *,
        modelManifestArn: str = ...,
        attributeNames: Sequence[str] = ...,
        attributeValues: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> AsyncIterator[ListVehiclesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListVehicles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclespaginator)
        """

class ListVehiclesInFleetPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListVehiclesInFleet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
    """

    def paginate(
        self, *, fleetId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> AsyncIterator[ListVehiclesInFleetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotfleetwise.html#IoTFleetWise.Paginator.ListVehiclesInFleet.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotfleetwise/paginators/#listvehiclesinfleetpaginator)
        """
