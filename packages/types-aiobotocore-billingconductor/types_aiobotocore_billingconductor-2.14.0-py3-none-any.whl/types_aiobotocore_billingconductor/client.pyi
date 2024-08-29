"""
Type annotations for billingconductor service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_billingconductor.client import BillingConductorClient

    session = get_session()
    async with session.create_client("billingconductor") as client:
        client: BillingConductorClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .literals import (
    BillingGroupStatusType,
    GroupByAttributeNameType,
    PricingRuleScopeType,
    PricingRuleTypeType,
)
from .paginator import (
    ListAccountAssociationsPaginator,
    ListBillingGroupCostReportsPaginator,
    ListBillingGroupsPaginator,
    ListCustomLineItemsPaginator,
    ListCustomLineItemVersionsPaginator,
    ListPricingPlansAssociatedWithPricingRulePaginator,
    ListPricingPlansPaginator,
    ListPricingRulesAssociatedToPricingPlanPaginator,
    ListPricingRulesPaginator,
    ListResourcesAssociatedToCustomLineItemPaginator,
)
from .type_defs import (
    AccountGroupingTypeDef,
    AssociateAccountsOutputTypeDef,
    AssociatePricingRulesOutputTypeDef,
    BatchAssociateResourcesToCustomLineItemOutputTypeDef,
    BatchDisassociateResourcesFromCustomLineItemOutputTypeDef,
    BillingPeriodRangeTypeDef,
    ComputationPreferenceTypeDef,
    CreateBillingGroupOutputTypeDef,
    CreateCustomLineItemOutputTypeDef,
    CreatePricingPlanOutputTypeDef,
    CreatePricingRuleOutputTypeDef,
    CreateTieringInputTypeDef,
    CustomLineItemBillingPeriodRangeTypeDef,
    CustomLineItemChargeDetailsTypeDef,
    DeleteBillingGroupOutputTypeDef,
    DeleteCustomLineItemOutputTypeDef,
    DeletePricingPlanOutputTypeDef,
    DeletePricingRuleOutputTypeDef,
    DisassociateAccountsOutputTypeDef,
    DisassociatePricingRulesOutputTypeDef,
    GetBillingGroupCostReportOutputTypeDef,
    ListAccountAssociationsFilterTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsFilterTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsFilterTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsFilterTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListCustomLineItemVersionsFilterTypeDef,
    ListCustomLineItemVersionsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansFilterTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesFilterTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemFilterTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
    ListTagsForResourceResponseTypeDef,
    UpdateBillingGroupAccountGroupingTypeDef,
    UpdateBillingGroupOutputTypeDef,
    UpdateCustomLineItemChargeDetailsTypeDef,
    UpdateCustomLineItemOutputTypeDef,
    UpdatePricingPlanOutputTypeDef,
    UpdatePricingRuleOutputTypeDef,
    UpdateTieringInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("BillingConductorClient",)

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
    ServiceLimitExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class BillingConductorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        BillingConductorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#exceptions)
        """

    async def associate_accounts(
        self, *, Arn: str, AccountIds: Sequence[str]
    ) -> AssociateAccountsOutputTypeDef:
        """
        Connects an array of account IDs in a consolidated billing family to a
        predefined billing
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.associate_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#associate_accounts)
        """

    async def associate_pricing_rules(
        self, *, Arn: str, PricingRuleArns: Sequence[str]
    ) -> AssociatePricingRulesOutputTypeDef:
        """
        Connects an array of `PricingRuleArns` to a defined `PricingPlan`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.associate_pricing_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#associate_pricing_rules)
        """

    async def batch_associate_resources_to_custom_line_item(
        self,
        *,
        TargetArn: str,
        ResourceArns: Sequence[str],
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...,
    ) -> BatchAssociateResourcesToCustomLineItemOutputTypeDef:
        """
        Associates a batch of resources to a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.batch_associate_resources_to_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#batch_associate_resources_to_custom_line_item)
        """

    async def batch_disassociate_resources_from_custom_line_item(
        self,
        *,
        TargetArn: str,
        ResourceArns: Sequence[str],
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...,
    ) -> BatchDisassociateResourcesFromCustomLineItemOutputTypeDef:
        """
        Disassociates a batch of resources from a percentage custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.batch_disassociate_resources_from_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#batch_disassociate_resources_from_custom_line_item)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#close)
        """

    async def create_billing_group(
        self,
        *,
        Name: str,
        AccountGrouping: AccountGroupingTypeDef,
        ComputationPreference: ComputationPreferenceTypeDef,
        ClientToken: str = ...,
        PrimaryAccountId: str = ...,
        Description: str = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreateBillingGroupOutputTypeDef:
        """
        Creates a billing group that resembles a consolidated billing family that
        Amazon Web Services charges, based off of the predefined pricing plan
        computation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#create_billing_group)
        """

    async def create_custom_line_item(
        self,
        *,
        Name: str,
        Description: str,
        BillingGroupArn: str,
        ChargeDetails: CustomLineItemChargeDetailsTypeDef,
        ClientToken: str = ...,
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...,
        Tags: Mapping[str, str] = ...,
        AccountId: str = ...,
    ) -> CreateCustomLineItemOutputTypeDef:
        """
        Creates a custom line item that can be used to create a one-time fixed charge
        that can be applied to a single billing group for the current or previous
        billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#create_custom_line_item)
        """

    async def create_pricing_plan(
        self,
        *,
        Name: str,
        ClientToken: str = ...,
        Description: str = ...,
        PricingRuleArns: Sequence[str] = ...,
        Tags: Mapping[str, str] = ...,
    ) -> CreatePricingPlanOutputTypeDef:
        """
        Creates a pricing plan that is used for computing Amazon Web Services charges
        for billing
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_pricing_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#create_pricing_plan)
        """

    async def create_pricing_rule(
        self,
        *,
        Name: str,
        Scope: PricingRuleScopeType,
        Type: PricingRuleTypeType,
        ClientToken: str = ...,
        Description: str = ...,
        ModifierPercentage: float = ...,
        Service: str = ...,
        Tags: Mapping[str, str] = ...,
        BillingEntity: str = ...,
        Tiering: CreateTieringInputTypeDef = ...,
        UsageType: str = ...,
        Operation: str = ...,
    ) -> CreatePricingRuleOutputTypeDef:
        """
        Creates a pricing rule can be associated to a pricing plan, or a set of pricing
        plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.create_pricing_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#create_pricing_rule)
        """

    async def delete_billing_group(self, *, Arn: str) -> DeleteBillingGroupOutputTypeDef:
        """
        Deletes a billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#delete_billing_group)
        """

    async def delete_custom_line_item(
        self, *, Arn: str, BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...
    ) -> DeleteCustomLineItemOutputTypeDef:
        """
        Deletes the custom line item identified by the given ARN in the current, or
        previous billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#delete_custom_line_item)
        """

    async def delete_pricing_plan(self, *, Arn: str) -> DeletePricingPlanOutputTypeDef:
        """
        Deletes a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_pricing_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#delete_pricing_plan)
        """

    async def delete_pricing_rule(self, *, Arn: str) -> DeletePricingRuleOutputTypeDef:
        """
        Deletes the pricing rule that's identified by the input Amazon Resource Name
        (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.delete_pricing_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#delete_pricing_rule)
        """

    async def disassociate_accounts(
        self, *, Arn: str, AccountIds: Sequence[str]
    ) -> DisassociateAccountsOutputTypeDef:
        """
        Removes the specified list of account IDs from the given billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.disassociate_accounts)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#disassociate_accounts)
        """

    async def disassociate_pricing_rules(
        self, *, Arn: str, PricingRuleArns: Sequence[str]
    ) -> DisassociatePricingRulesOutputTypeDef:
        """
        Disassociates a list of pricing rules from a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.disassociate_pricing_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#disassociate_pricing_rules)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#generate_presigned_url)
        """

    async def get_billing_group_cost_report(
        self,
        *,
        Arn: str,
        BillingPeriodRange: BillingPeriodRangeTypeDef = ...,
        GroupBy: Sequence[GroupByAttributeNameType] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> GetBillingGroupCostReportOutputTypeDef:
        """
        Retrieves the margin summary report, which includes the Amazon Web Services
        cost and charged amount (pro forma cost) by Amazon Web Service for a specific
        billing
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_billing_group_cost_report)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_billing_group_cost_report)
        """

    async def list_account_associations(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListAccountAssociationsFilterTypeDef = ...,
        NextToken: str = ...,
    ) -> ListAccountAssociationsOutputTypeDef:
        """
        This is a paginated call to list linked accounts that are linked to the payer
        account for the specified time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_account_associations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_account_associations)
        """

    async def list_billing_group_cost_reports(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListBillingGroupCostReportsFilterTypeDef = ...,
    ) -> ListBillingGroupCostReportsOutputTypeDef:
        """
        A paginated call to retrieve a summary report of actual Amazon Web Services
        charges and the calculated Amazon Web Services charges based on the associated
        pricing plan of a billing
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_billing_group_cost_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_billing_group_cost_reports)
        """

    async def list_billing_groups(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListBillingGroupsFilterTypeDef = ...,
    ) -> ListBillingGroupsOutputTypeDef:
        """
        A paginated call to retrieve a list of billing groups for the given billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_billing_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_billing_groups)
        """

    async def list_custom_line_item_versions(
        self,
        *,
        Arn: str,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListCustomLineItemVersionsFilterTypeDef = ...,
    ) -> ListCustomLineItemVersionsOutputTypeDef:
        """
        A paginated call to get a list of all custom line item versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_custom_line_item_versions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_custom_line_item_versions)
        """

    async def list_custom_line_items(
        self,
        *,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListCustomLineItemsFilterTypeDef = ...,
    ) -> ListCustomLineItemsOutputTypeDef:
        """
        A paginated call to get a list of all custom line items (FFLIs) for the given
        billing
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_custom_line_items)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_custom_line_items)
        """

    async def list_pricing_plans(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingPlansFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListPricingPlansOutputTypeDef:
        """
        A paginated call to get pricing plans for the given billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_plans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_pricing_plans)
        """

    async def list_pricing_plans_associated_with_pricing_rule(
        self,
        *,
        PricingRuleArn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListPricingPlansAssociatedWithPricingRuleOutputTypeDef:
        """
        A list of the pricing plans that are associated with a pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_plans_associated_with_pricing_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_pricing_plans_associated_with_pricing_rule)
        """

    async def list_pricing_rules(
        self,
        *,
        BillingPeriod: str = ...,
        Filters: ListPricingRulesFilterTypeDef = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListPricingRulesOutputTypeDef:
        """
        Describes a pricing rule that can be associated to a pricing plan, or set of
        pricing
        plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_rules)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_pricing_rules)
        """

    async def list_pricing_rules_associated_to_pricing_plan(
        self,
        *,
        PricingPlanArn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> ListPricingRulesAssociatedToPricingPlanOutputTypeDef:
        """
        Lists the pricing rules that are associated with a pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_pricing_rules_associated_to_pricing_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_pricing_rules_associated_to_pricing_plan)
        """

    async def list_resources_associated_to_custom_line_item(
        self,
        *,
        Arn: str,
        BillingPeriod: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        Filters: ListResourcesAssociatedToCustomLineItemFilterTypeDef = ...,
    ) -> ListResourcesAssociatedToCustomLineItemOutputTypeDef:
        """
        List the resources that are associated to a custom line item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_resources_associated_to_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_resources_associated_to_custom_line_item)
        """

    async def list_tags_for_resource(
        self, *, ResourceArn: str
    ) -> ListTagsForResourceResponseTypeDef:
        """
        A list the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#list_tags_for_resource)
        """

    async def tag_resource(self, *, ResourceArn: str, Tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Associates the specified tags to a resource with the specified `resourceArn`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#tag_resource)
        """

    async def untag_resource(self, *, ResourceArn: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Deletes specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#untag_resource)
        """

    async def update_billing_group(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Status: BillingGroupStatusType = ...,
        ComputationPreference: ComputationPreferenceTypeDef = ...,
        Description: str = ...,
        AccountGrouping: UpdateBillingGroupAccountGroupingTypeDef = ...,
    ) -> UpdateBillingGroupOutputTypeDef:
        """
        This updates an existing billing group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_billing_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#update_billing_group)
        """

    async def update_custom_line_item(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Description: str = ...,
        ChargeDetails: UpdateCustomLineItemChargeDetailsTypeDef = ...,
        BillingPeriodRange: CustomLineItemBillingPeriodRangeTypeDef = ...,
    ) -> UpdateCustomLineItemOutputTypeDef:
        """
        Update an existing custom line item in the current or previous billing period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_custom_line_item)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#update_custom_line_item)
        """

    async def update_pricing_plan(
        self, *, Arn: str, Name: str = ..., Description: str = ...
    ) -> UpdatePricingPlanOutputTypeDef:
        """
        This updates an existing pricing plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_pricing_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#update_pricing_plan)
        """

    async def update_pricing_rule(
        self,
        *,
        Arn: str,
        Name: str = ...,
        Description: str = ...,
        Type: PricingRuleTypeType = ...,
        ModifierPercentage: float = ...,
        Tiering: UpdateTieringInputTypeDef = ...,
    ) -> UpdatePricingRuleOutputTypeDef:
        """
        Updates an existing pricing rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.update_pricing_rule)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#update_pricing_rule)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_account_associations"]
    ) -> ListAccountAssociationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_group_cost_reports"]
    ) -> ListBillingGroupCostReportsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_billing_groups"]
    ) -> ListBillingGroupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_line_item_versions"]
    ) -> ListCustomLineItemVersionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_custom_line_items"]
    ) -> ListCustomLineItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans"]
    ) -> ListPricingPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_plans_associated_with_pricing_rule"]
    ) -> ListPricingPlansAssociatedWithPricingRulePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules"]
    ) -> ListPricingRulesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_pricing_rules_associated_to_pricing_plan"]
    ) -> ListPricingRulesAssociatedToPricingPlanPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_resources_associated_to_custom_line_item"]
    ) -> ListResourcesAssociatedToCustomLineItemPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/#get_paginator)
        """

    async def __aenter__(self) -> "BillingConductorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor.html#BillingConductor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/client/)
        """
