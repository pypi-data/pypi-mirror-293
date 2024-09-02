# PlannerColumnPost

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**order** | **int** |  | [optional] 
**display_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**internal_name** | **str** |  | [optional] 
**parent_filter_field** | **str** |  | [optional] 
**column_type** | [**ColumnTypeEnum**](ColumnTypeEnum.md) |  | [optional] 
**column_aggregate** | [**ColumnAggEnum**](ColumnAggEnum.md) |  | [optional] 
**choices** | **dict(str, str)** |  | [optional] 
**choice_parents** | **dict(str, str)** |  | [optional] 
**numeric_values** | [**dict(str, DecimalNumber)**](DecimalNumber.md) |  | [optional] 
**read_only** | **bool** |  | [optional] 
**required** | **bool** |  | [optional] 
**percentage** | **bool** |  | [optional] 
**decimals** | **int** |  | [optional] 
**default_value** | **str** |  | [optional] 
**allow_additions** | **bool** |  | [optional] 
**plan_type_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**writeable_plan_types** | [**list[GloballyUniqueIdentifier]**](GloballyUniqueIdentifier.md) |  | [optional] 
**function** | [**FieldFunction**](FieldFunction.md) |  | [optional] 
**rollup_work_type** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**rollup_aggregate** | [**ColumnAggEnum**](ColumnAggEnum.md) |  | [optional] 
**rollup_lookup_field** | **str** |  | [optional] 
**rollup_field** | **str** |  | [optional] 
**rollup_filter** | **str** |  | [optional] 
**calculations** | [**list[ColumnCalculation]**](ColumnCalculation.md) |  | [optional] 
**filter** | [**TableFilter**](TableFilter.md) |  | [optional] 
**hidden** | **bool** |  | [optional] 
**show_in_quick_start** | **bool** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

