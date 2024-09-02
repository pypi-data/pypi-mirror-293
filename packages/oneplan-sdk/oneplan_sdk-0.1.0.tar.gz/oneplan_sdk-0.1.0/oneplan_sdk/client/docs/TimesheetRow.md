# TimesheetRow

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**timesheet_line_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**timesheet_id** | [**GloballyUniqueIdentifier**](GloballyUniqueIdentifier.md) |  | [optional] 
**row_total** | [**DecimalNumber**](DecimalNumber.md) |  | [optional] 
**row_progress** | [**DecimalNumber**](DecimalNumber.md) |  | [optional] 
**submitted** | **bool** |  | [optional] 
**time_approved** | **int** |  | [optional] 
**plan_approved** | **int** |  | [optional] 
**plan** | [**WorkPlan**](WorkPlan.md) |  | [optional] 
**task** | [**WorkPlanTask**](WorkPlanTask.md) |  | [optional] 
**fields** | [**dict(str, Object)**](Object.md) |  | [optional] 
**data** | [**list[TimesheetRowDate]**](TimesheetRowDate.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

