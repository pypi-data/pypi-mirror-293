"""
Type annotations for location service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_location.client import LocationServiceClient

    session = get_session()
    async with session.create_client("location") as client:
        client: LocationServiceClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    DistanceUnitType,
    OptimizationModeType,
    PositionFilteringType,
    PricingPlanType,
    SpeedUnitType,
    TravelModeType,
)
from .paginator import (
    ForecastGeofenceEventsPaginator,
    GetDevicePositionHistoryPaginator,
    ListDevicePositionsPaginator,
    ListGeofenceCollectionsPaginator,
    ListGeofencesPaginator,
    ListKeysPaginator,
    ListMapsPaginator,
    ListPlaceIndexesPaginator,
    ListRouteCalculatorsPaginator,
    ListTrackerConsumersPaginator,
    ListTrackersPaginator,
)
from .type_defs import (
    ApiKeyFilterTypeDef,
    ApiKeyRestrictionsUnionTypeDef,
    BatchDeleteDevicePositionHistoryResponseTypeDef,
    BatchDeleteGeofenceResponseTypeDef,
    BatchEvaluateGeofencesResponseTypeDef,
    BatchGetDevicePositionResponseTypeDef,
    BatchPutGeofenceRequestEntryTypeDef,
    BatchPutGeofenceResponseTypeDef,
    BatchUpdateDevicePositionResponseTypeDef,
    CalculateRouteCarModeOptionsTypeDef,
    CalculateRouteMatrixResponseTypeDef,
    CalculateRouteResponseTypeDef,
    CalculateRouteTruckModeOptionsTypeDef,
    CreateGeofenceCollectionResponseTypeDef,
    CreateKeyResponseTypeDef,
    CreateMapResponseTypeDef,
    CreatePlaceIndexResponseTypeDef,
    CreateRouteCalculatorResponseTypeDef,
    CreateTrackerResponseTypeDef,
    DataSourceConfigurationTypeDef,
    DescribeGeofenceCollectionResponseTypeDef,
    DescribeKeyResponseTypeDef,
    DescribeMapResponseTypeDef,
    DescribePlaceIndexResponseTypeDef,
    DescribeRouteCalculatorResponseTypeDef,
    DescribeTrackerResponseTypeDef,
    DevicePositionUpdateTypeDef,
    DeviceStateTypeDef,
    ForecastGeofenceEventsDeviceStateTypeDef,
    ForecastGeofenceEventsResponseTypeDef,
    GeofenceGeometryUnionTypeDef,
    GetDevicePositionHistoryResponseTypeDef,
    GetDevicePositionResponseTypeDef,
    GetGeofenceResponseTypeDef,
    GetMapGlyphsResponseTypeDef,
    GetMapSpritesResponseTypeDef,
    GetMapStyleDescriptorResponseTypeDef,
    GetMapTileResponseTypeDef,
    GetPlaceResponseTypeDef,
    ListDevicePositionsResponseTypeDef,
    ListGeofenceCollectionsResponseTypeDef,
    ListGeofencesResponseTypeDef,
    ListKeysResponseTypeDef,
    ListMapsResponseTypeDef,
    ListPlaceIndexesResponseTypeDef,
    ListRouteCalculatorsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrackerConsumersResponseTypeDef,
    ListTrackersResponseTypeDef,
    MapConfigurationUnionTypeDef,
    MapConfigurationUpdateTypeDef,
    PutGeofenceResponseTypeDef,
    SearchPlaceIndexForPositionResponseTypeDef,
    SearchPlaceIndexForSuggestionsResponseTypeDef,
    SearchPlaceIndexForTextResponseTypeDef,
    TimestampTypeDef,
    TrackingFilterGeometryTypeDef,
    UpdateGeofenceCollectionResponseTypeDef,
    UpdateKeyResponseTypeDef,
    UpdateMapResponseTypeDef,
    UpdatePlaceIndexResponseTypeDef,
    UpdateRouteCalculatorResponseTypeDef,
    UpdateTrackerResponseTypeDef,
    VerifyDevicePositionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("LocationServiceClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class LocationServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LocationServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#exceptions)
        """

    async def associate_tracker_consumer(
        self, *, TrackerName: str, ConsumerArn: str
    ) -> Dict[str, Any]:
        """
        Creates an association between a geofence collection and a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.associate_tracker_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#associate_tracker_consumer)
        """

    async def batch_delete_device_position_history(
        self, *, TrackerName: str, DeviceIds: Sequence[str]
    ) -> BatchDeleteDevicePositionHistoryResponseTypeDef:
        """
        Deletes the position history of one or more devices from a tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_device_position_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_delete_device_position_history)
        """

    async def batch_delete_geofence(
        self, *, CollectionName: str, GeofenceIds: Sequence[str]
    ) -> BatchDeleteGeofenceResponseTypeDef:
        """
        Deletes a batch of geofences from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_delete_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_delete_geofence)
        """

    async def batch_evaluate_geofences(
        self, *, CollectionName: str, DevicePositionUpdates: Sequence[DevicePositionUpdateTypeDef]
    ) -> BatchEvaluateGeofencesResponseTypeDef:
        """
        Evaluates device positions against the geofence geometries from a given
        geofence
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_evaluate_geofences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_evaluate_geofences)
        """

    async def batch_get_device_position(
        self, *, TrackerName: str, DeviceIds: Sequence[str]
    ) -> BatchGetDevicePositionResponseTypeDef:
        """
        Lists the latest device positions for requested devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_get_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_get_device_position)
        """

    async def batch_put_geofence(
        self, *, CollectionName: str, Entries: Sequence[BatchPutGeofenceRequestEntryTypeDef]
    ) -> BatchPutGeofenceResponseTypeDef:
        """
        A batch request for storing geofence geometries into a given geofence
        collection, or updates the geometry of an existing geofence if a geofence ID is
        included in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_put_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_put_geofence)
        """

    async def batch_update_device_position(
        self, *, TrackerName: str, Updates: Sequence[DevicePositionUpdateTypeDef]
    ) -> BatchUpdateDevicePositionResponseTypeDef:
        """
        Uploads position update data for one or more devices to a tracker resource (up
        to 10 devices per
        batch).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.batch_update_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#batch_update_device_position)
        """

    async def calculate_route(
        self,
        *,
        CalculatorName: str,
        DeparturePosition: Sequence[float],
        DestinationPosition: Sequence[float],
        WaypointPositions: Sequence[Sequence[float]] = ...,
        TravelMode: TravelModeType = ...,
        DepartureTime: TimestampTypeDef = ...,
        DepartNow: bool = ...,
        DistanceUnit: DistanceUnitType = ...,
        IncludeLegGeometry: bool = ...,
        CarModeOptions: CalculateRouteCarModeOptionsTypeDef = ...,
        TruckModeOptions: CalculateRouteTruckModeOptionsTypeDef = ...,
        ArrivalTime: TimestampTypeDef = ...,
        OptimizeFor: OptimizationModeType = ...,
        Key: str = ...,
    ) -> CalculateRouteResponseTypeDef:
        """
        [Calculates a
        route](https://docs.aws.amazon.com/location/latest/developerguide/calculate-route.html)
        given the following required parameters: `DeparturePosition` and
        `DestinationPosition`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#calculate_route)
        """

    async def calculate_route_matrix(
        self,
        *,
        CalculatorName: str,
        DeparturePositions: Sequence[Sequence[float]],
        DestinationPositions: Sequence[Sequence[float]],
        TravelMode: TravelModeType = ...,
        DepartureTime: TimestampTypeDef = ...,
        DepartNow: bool = ...,
        DistanceUnit: DistanceUnitType = ...,
        CarModeOptions: CalculateRouteCarModeOptionsTypeDef = ...,
        TruckModeOptions: CalculateRouteTruckModeOptionsTypeDef = ...,
        Key: str = ...,
    ) -> CalculateRouteMatrixResponseTypeDef:
        """
        [Calculates a route
        matrix](https://docs.aws.amazon.com/location/latest/developerguide/calculate-route-matrix.html)
        given the following required parameters: `DeparturePositions` and
        `DestinationPositions`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.calculate_route_matrix)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#calculate_route_matrix)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#close)
        """

    async def create_geofence_collection(
        self,
        *,
        CollectionName: str,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
        KmsKeyId: str = ...,
    ) -> CreateGeofenceCollectionResponseTypeDef:
        """
        Creates a geofence collection, which manages and stores geofences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_geofence_collection)
        """

    async def create_key(
        self,
        *,
        KeyName: str,
        Restrictions: ApiKeyRestrictionsUnionTypeDef,
        Description: str = ...,
        ExpireTime: TimestampTypeDef = ...,
        NoExpiry: bool = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateKeyResponseTypeDef:
        """
        Creates an API key resource in your Amazon Web Services account, which lets you
        grant actions for Amazon Location resources to the API key
        bearer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_key)
        """

    async def create_map(
        self,
        *,
        MapName: str,
        Configuration: MapConfigurationUnionTypeDef,
        PricingPlan: PricingPlanType = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateMapResponseTypeDef:
        """
        Creates a map resource in your Amazon Web Services account, which provides map
        tiles of different styles sourced from global location data
        providers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_map)
        """

    async def create_place_index(
        self,
        *,
        IndexName: str,
        DataSource: str,
        PricingPlan: PricingPlanType = ...,
        Description: str = ...,
        DataSourceConfiguration: DataSourceConfigurationTypeDef = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreatePlaceIndexResponseTypeDef:
        """
        Creates a place index resource in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_place_index)
        """

    async def create_route_calculator(
        self,
        *,
        CalculatorName: str,
        DataSource: str,
        PricingPlan: PricingPlanType = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateRouteCalculatorResponseTypeDef:
        """
        Creates a route calculator resource in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_route_calculator)
        """

    async def create_tracker(
        self,
        *,
        TrackerName: str,
        PricingPlan: PricingPlanType = ...,
        KmsKeyId: str = ...,
        PricingPlanDataSource: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
        PositionFiltering: PositionFilteringType = ...,
        EventBridgeEnabled: bool = ...,
        KmsKeyEnableGeospatialQueries: bool = ...,
    ) -> CreateTrackerResponseTypeDef:
        """
        Creates a tracker resource in your Amazon Web Services account, which lets you
        retrieve current and historical location of
        devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.create_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#create_tracker)
        """

    async def delete_geofence_collection(self, *, CollectionName: str) -> Dict[str, Any]:
        """
        Deletes a geofence collection from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_geofence_collection)
        """

    async def delete_key(self, *, KeyName: str, ForceDelete: bool = ...) -> Dict[str, Any]:
        """
        Deletes the specified API key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_key)
        """

    async def delete_map(self, *, MapName: str) -> Dict[str, Any]:
        """
        Deletes a map resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_map)
        """

    async def delete_place_index(self, *, IndexName: str) -> Dict[str, Any]:
        """
        Deletes a place index resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_place_index)
        """

    async def delete_route_calculator(self, *, CalculatorName: str) -> Dict[str, Any]:
        """
        Deletes a route calculator resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_route_calculator)
        """

    async def delete_tracker(self, *, TrackerName: str) -> Dict[str, Any]:
        """
        Deletes a tracker resource from your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.delete_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#delete_tracker)
        """

    async def describe_geofence_collection(
        self, *, CollectionName: str
    ) -> DescribeGeofenceCollectionResponseTypeDef:
        """
        Retrieves the geofence collection details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_geofence_collection)
        """

    async def describe_key(self, *, KeyName: str) -> DescribeKeyResponseTypeDef:
        """
        Retrieves the API key resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_key)
        """

    async def describe_map(self, *, MapName: str) -> DescribeMapResponseTypeDef:
        """
        Retrieves the map resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_map)
        """

    async def describe_place_index(self, *, IndexName: str) -> DescribePlaceIndexResponseTypeDef:
        """
        Retrieves the place index resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_place_index)
        """

    async def describe_route_calculator(
        self, *, CalculatorName: str
    ) -> DescribeRouteCalculatorResponseTypeDef:
        """
        Retrieves the route calculator resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_route_calculator)
        """

    async def describe_tracker(self, *, TrackerName: str) -> DescribeTrackerResponseTypeDef:
        """
        Retrieves the tracker resource details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.describe_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#describe_tracker)
        """

    async def disassociate_tracker_consumer(
        self, *, TrackerName: str, ConsumerArn: str
    ) -> Dict[str, Any]:
        """
        Removes the association between a tracker resource and a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.disassociate_tracker_consumer)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#disassociate_tracker_consumer)
        """

    async def forecast_geofence_events(
        self,
        *,
        CollectionName: str,
        DeviceState: ForecastGeofenceEventsDeviceStateTypeDef,
        TimeHorizonMinutes: float = ...,
        DistanceUnit: DistanceUnitType = ...,
        SpeedUnit: SpeedUnitType = ...,
        NextToken: str = ...,
        MaxResults: int = ...,
    ) -> ForecastGeofenceEventsResponseTypeDef:
        """
        Evaluates device positions against geofence geometries from a given geofence
        collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.forecast_geofence_events)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#forecast_geofence_events)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#generate_presigned_url)
        """

    async def get_device_position(
        self, *, TrackerName: str, DeviceId: str
    ) -> GetDevicePositionResponseTypeDef:
        """
        Retrieves a device's most recent position according to its sample time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_device_position)
        """

    async def get_device_position_history(
        self,
        *,
        TrackerName: str,
        DeviceId: str,
        NextToken: str = ...,
        StartTimeInclusive: TimestampTypeDef = ...,
        EndTimeExclusive: TimestampTypeDef = ...,
        MaxResults: int = ...,
    ) -> GetDevicePositionHistoryResponseTypeDef:
        """
        Retrieves the device position history from a tracker resource within a
        specified range of
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_device_position_history)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_device_position_history)
        """

    async def get_geofence(
        self, *, CollectionName: str, GeofenceId: str
    ) -> GetGeofenceResponseTypeDef:
        """
        Retrieves the geofence details from a geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_geofence)
        """

    async def get_map_glyphs(
        self, *, MapName: str, FontStack: str, FontUnicodeRange: str, Key: str = ...
    ) -> GetMapGlyphsResponseTypeDef:
        """
        Retrieves glyphs used to display labels on a map.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_glyphs)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_glyphs)
        """

    async def get_map_sprites(
        self, *, MapName: str, FileName: str, Key: str = ...
    ) -> GetMapSpritesResponseTypeDef:
        """
        Retrieves the sprite sheet corresponding to a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_sprites)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_sprites)
        """

    async def get_map_style_descriptor(
        self, *, MapName: str, Key: str = ...
    ) -> GetMapStyleDescriptorResponseTypeDef:
        """
        Retrieves the map style descriptor from a map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_style_descriptor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_style_descriptor)
        """

    async def get_map_tile(
        self, *, MapName: str, Z: str, X: str, Y: str, Key: str = ...
    ) -> GetMapTileResponseTypeDef:
        """
        Retrieves a vector data tile from the map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_map_tile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_map_tile)
        """

    async def get_place(
        self, *, IndexName: str, PlaceId: str, Language: str = ..., Key: str = ...
    ) -> GetPlaceResponseTypeDef:
        """
        Finds a place by its unique ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_place)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_place)
        """

    async def list_device_positions(
        self,
        *,
        TrackerName: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        FilterGeometry: TrackingFilterGeometryTypeDef = ...,
    ) -> ListDevicePositionsResponseTypeDef:
        """
        A batch request to retrieve all device positions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_device_positions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_device_positions)
        """

    async def list_geofence_collections(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListGeofenceCollectionsResponseTypeDef:
        """
        Lists geofence collections in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofence_collections)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_geofence_collections)
        """

    async def list_geofences(
        self, *, CollectionName: str, NextToken: str = ..., MaxResults: int = ...
    ) -> ListGeofencesResponseTypeDef:
        """
        Lists geofences stored in a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_geofences)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_geofences)
        """

    async def list_keys(
        self, *, MaxResults: int = ..., NextToken: str = ..., Filter: ApiKeyFilterTypeDef = ...
    ) -> ListKeysResponseTypeDef:
        """
        Lists API key resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_keys)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_keys)
        """

    async def list_maps(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListMapsResponseTypeDef:
        """
        Lists map resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_maps)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_maps)
        """

    async def list_place_indexes(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListPlaceIndexesResponseTypeDef:
        """
        Lists place index resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_place_indexes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_place_indexes)
        """

    async def list_route_calculators(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListRouteCalculatorsResponseTypeDef:
        """
        Lists route calculator resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_route_calculators)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_route_calculators)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags that are applied to the specified Amazon Location
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_tags_for_resource)
        """

    async def list_tracker_consumers(
        self, *, TrackerName: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTrackerConsumersResponseTypeDef:
        """
        Lists geofence collections currently associated to the given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_tracker_consumers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_tracker_consumers)
        """

    async def list_trackers(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTrackersResponseTypeDef:
        """
        Lists tracker resources in your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.list_trackers)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#list_trackers)
        """

    async def put_geofence(
        self,
        *,
        CollectionName: str,
        GeofenceId: str,
        Geometry: GeofenceGeometryUnionTypeDef,
        GeofenceProperties: Mapping[str, str] = ...,
    ) -> PutGeofenceResponseTypeDef:
        """
        Stores a geofence geometry in a given geofence collection, or updates the
        geometry of an existing geofence if a geofence ID is included in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.put_geofence)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#put_geofence)
        """

    async def search_place_index_for_position(
        self,
        *,
        IndexName: str,
        Position: Sequence[float],
        MaxResults: int = ...,
        Language: str = ...,
        Key: str = ...,
    ) -> SearchPlaceIndexForPositionResponseTypeDef:
        """
        Reverse geocodes a given coordinate and returns a legible address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_position)
        """

    async def search_place_index_for_suggestions(
        self,
        *,
        IndexName: str,
        Text: str,
        BiasPosition: Sequence[float] = ...,
        FilterBBox: Sequence[float] = ...,
        FilterCountries: Sequence[str] = ...,
        MaxResults: int = ...,
        Language: str = ...,
        FilterCategories: Sequence[str] = ...,
        Key: str = ...,
    ) -> SearchPlaceIndexForSuggestionsResponseTypeDef:
        """
        Generates suggestions for addresses and points of interest based on partial or
        misspelled free-form
        text.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_suggestions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_suggestions)
        """

    async def search_place_index_for_text(
        self,
        *,
        IndexName: str,
        Text: str,
        BiasPosition: Sequence[float] = ...,
        FilterBBox: Sequence[float] = ...,
        FilterCountries: Sequence[str] = ...,
        MaxResults: int = ...,
        Language: str = ...,
        FilterCategories: Sequence[str] = ...,
        Key: str = ...,
    ) -> SearchPlaceIndexForTextResponseTypeDef:
        """
        Geocodes free-form text, such as an address, name, city, or region to allow you
        to search for Places or points of
        interest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.search_place_index_for_text)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#search_place_index_for_text)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Assigns one or more tags (key-value pairs) to the specified Amazon Location
        Service
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags from the specified Amazon Location resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#untag_resource)
        """

    async def update_geofence_collection(
        self,
        *,
        CollectionName: str,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...,
        Description: str = ...,
    ) -> UpdateGeofenceCollectionResponseTypeDef:
        """
        Updates the specified properties of a given geofence collection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_geofence_collection)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_geofence_collection)
        """

    async def update_key(
        self,
        *,
        KeyName: str,
        Description: str = ...,
        ExpireTime: TimestampTypeDef = ...,
        NoExpiry: bool = ...,
        ForceUpdate: bool = ...,
        Restrictions: ApiKeyRestrictionsUnionTypeDef = ...,
    ) -> UpdateKeyResponseTypeDef:
        """
        Updates the specified properties of a given API key resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_key)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_key)
        """

    async def update_map(
        self,
        *,
        MapName: str,
        PricingPlan: PricingPlanType = ...,
        Description: str = ...,
        ConfigurationUpdate: MapConfigurationUpdateTypeDef = ...,
    ) -> UpdateMapResponseTypeDef:
        """
        Updates the specified properties of a given map resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_map)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_map)
        """

    async def update_place_index(
        self,
        *,
        IndexName: str,
        PricingPlan: PricingPlanType = ...,
        Description: str = ...,
        DataSourceConfiguration: DataSourceConfigurationTypeDef = ...,
    ) -> UpdatePlaceIndexResponseTypeDef:
        """
        Updates the specified properties of a given place index resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_place_index)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_place_index)
        """

    async def update_route_calculator(
        self, *, CalculatorName: str, PricingPlan: PricingPlanType = ..., Description: str = ...
    ) -> UpdateRouteCalculatorResponseTypeDef:
        """
        Updates the specified properties for a given route calculator resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_route_calculator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_route_calculator)
        """

    async def update_tracker(
        self,
        *,
        TrackerName: str,
        PricingPlan: PricingPlanType = ...,
        PricingPlanDataSource: str = ...,
        Description: str = ...,
        PositionFiltering: PositionFilteringType = ...,
        EventBridgeEnabled: bool = ...,
        KmsKeyEnableGeospatialQueries: bool = ...,
    ) -> UpdateTrackerResponseTypeDef:
        """
        Updates the specified properties of a given tracker resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.update_tracker)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#update_tracker)
        """

    async def verify_device_position(
        self,
        *,
        TrackerName: str,
        DeviceState: DeviceStateTypeDef,
        DistanceUnit: DistanceUnitType = ...,
    ) -> VerifyDevicePositionResponseTypeDef:
        """
        Verifies the integrity of the device's position by determining if it was
        reported behind a proxy, and by comparing it to an inferred position estimated
        based on the device's
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.verify_device_position)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#verify_device_position)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["forecast_geofence_events"]
    ) -> ForecastGeofenceEventsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_device_position_history"]
    ) -> GetDevicePositionHistoryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_device_positions"]
    ) -> ListDevicePositionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_geofence_collections"]
    ) -> ListGeofenceCollectionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_geofences"]) -> ListGeofencesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_keys"]) -> ListKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_maps"]) -> ListMapsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_place_indexes"]
    ) -> ListPlaceIndexesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_route_calculators"]
    ) -> ListRouteCalculatorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tracker_consumers"]
    ) -> ListTrackerConsumersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_trackers"]) -> ListTrackersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/#get_paginator)
        """

    async def __aenter__(self) -> "LocationServiceClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/location.html#LocationService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_location/client/)
        """
