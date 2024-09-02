# ModelScenario

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**name** | **str** |  | [optional] 
**parent_model_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**plans** | [**list[ModelScenarioPlan]**](ModelScenarioPlan.md) |  | [optional] 
**properties** | [**dict(str, Object)**](Object.md) |  | [optional] 
**total_checked_plans** | **int** |  | [optional] 
**total_plans** | **int** |  | [optional] 
**total_cost_fields** | [**dict(str, DecimalNumber)**](DecimalNumber.md) |  | [optional] 
**total_benefit_fields** | [**dict(str, DecimalNumber)**](DecimalNumber.md) |  | [optional] 
**target_cost_fields** | [**dict(str, DecimalNumber)**](DecimalNumber.md) |  | [optional] 
**target_benefit_fields** | [**dict(str, DecimalNumber)**](DecimalNumber.md) |  | [optional] 
**cost_planner_targets** | [**list[ScenarioCostTarget]**](ScenarioCostTarget.md) |  | [optional] 
**id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**config_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

