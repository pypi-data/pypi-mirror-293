# WorkPlanTask

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**work_type_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**name** | **str** |  | [optional] 
**created** | **date** |  | [optional] 
**modified** | **date** |  | [optional] 
**author** | **str** |  | [optional] 
**editor** | **str** |  | [optional] 
**assigned_to** | [**list[GloballyUniqueIdentifier]**](GloballyUniqueIdentifier.md) |  | [optional] 
**assignments** | [**list[TaskAssignment]**](TaskAssignment.md) |  | [optional] 
**parent_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**work_type_parent_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**work_type_index** | **int** |  | [optional] 
**fields** | [**dict(str, Object)**](Object.md) |  | [optional] 
**index** | **int** |  | [optional] 
**complete** | **bool** |  | [optional] 
**comments** | [**list[TaskComment]**](TaskComment.md) |  | [optional] 
**start_date** | **date** |  | [optional] 
**due_date** | **date** |  | [optional] 
**task_schedule_type** | [**TaskType**](TaskType.md) |  | [optional] 
**status_update** | [**StatusUpdateClass**](StatusUpdateClass.md) |  | [optional] 
**last_comment** | **date** |  | [optional] 
**is_scheduled** | **bool** |  | [optional] 
**integration** | [**TaskIntegrationInfo**](TaskIntegrationInfo.md) |  | [optional] 
**work_plan_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**config_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

