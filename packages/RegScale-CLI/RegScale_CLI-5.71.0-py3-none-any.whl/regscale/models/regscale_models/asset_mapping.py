import logging
from typing import Optional, List, Dict

from pydantic import ConfigDict, Field

from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models.regscale_models import Asset
from regscale.models.regscale_models.regscale_model import RegScaleModel
from regscale.models.regscale_models.regscale_model import T

logger = logging.getLogger(__name__)


class AssetMapping(RegScaleModel):
    """
    AssetMapping model class.
    """

    _module_slug = "assetmapping"
    _unique_fields = ["componentId", "assetId"]
    _parent_id_field = "componentId"

    id: Optional[int] = 0
    uuid: Optional[str] = None
    assetId: int
    componentId: int
    createdById: Optional[str] = None
    dateCreated: Optional[str] = Field(default_factory=get_current_datetime)
    lastUpdatedById: Optional[str] = None
    isPublic: Optional[bool] = True
    dateLastUpdated: Optional[str] = Field(default_factory=get_current_datetime)
    tenantsId: Optional[int] = 1

    @staticmethod
    def get_assets(component_id: int) -> List[T]:
        """
        Get assets for a given component ID.

        :param int component_id: The ID of the component
        :return: A list of assets
        :rtype: List[T]
        """
        asset_mappings = AssetMapping.find_mappings(component_id=component_id)
        assets = []
        for asset_mapping in asset_mappings:
            assets.append(Asset.get_object(object_id=asset_mapping.assetId))
        return assets

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the AssetMapping model.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict(
            get_all_by_parent="/api/{model_slug}/getMappingsAsComponents/{intParentID}",
            filter_asset_mappings="/api/{model_slug}/filterAssetMappings/{intAsset}/{intComp}/{strSearch}/{intPage}/{intPageSize}",
            find_mappings="/api/{model_slug}/findMappings/{intId}",
            get_mappings_as_components="/api/{model_slug}/getMappingsAsComponents/{intId}",
            get_mappings_as_assets="/api/{model_slug}/getMappingsAsAssets/{intId}/{strSortBy}/{strDirection}/{intPage}/{intPageSize}",
        )

    @classmethod
    def cast_list_object(
        cls,
        item: Dict,
        parent_id: Optional[int] = None,
        parent_module: Optional[str] = None,
    ) -> "AssetMapping":
        """
        Cast list of items to class instances.

        :param Dict item: item to cast
        :param Optional[int] parent_id: Parent ID, defaults to None
        :param Optional[str] parent_module: Parent module, defaults to None
        :return: Class instance created from the item
        :rtype: "AssetMapping"
        """
        item["assetId"] = parent_id or item.get("assetId")
        item["id"] = item["mappingId"]
        return cls(**item)
