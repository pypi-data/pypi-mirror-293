# oneplan_sdk.client.swagger_client.WorkPlanApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**workplan_dependency_id_delete**](WorkPlanApi.md#workplan_dependency_id_delete) | **DELETE** /workplan/dependency/{id} | 
[**workplan_dependency_id_post**](WorkPlanApi.md#workplan_dependency_id_post) | **POST** /workplan/dependency/{id} | 
[**workplan_dependency_post**](WorkPlanApi.md#workplan_dependency_post) | **POST** /workplan/dependency | 
[**workplan_fields_field_id_post**](WorkPlanApi.md#workplan_fields_field_id_post) | **POST** /workplan/fields/{FieldId} | 
[**workplan_fields_get**](WorkPlanApi.md#workplan_fields_get) | **GET** /workplan/fields | 
[**workplan_fields_post**](WorkPlanApi.md#workplan_fields_post) | **POST** /workplan/fields | 
[**workplan_fields_reorder_post**](WorkPlanApi.md#workplan_fields_reorder_post) | **POST** /workplan/fields/reorder | 
[**workplan_find_post**](WorkPlanApi.md#workplan_find_post) | **POST** /workplan/find | 
[**workplan_fragments_get**](WorkPlanApi.md#workplan_fragments_get) | **GET** /workplan/fragments | 
[**workplan_get**](WorkPlanApi.md#workplan_get) | **GET** /workplan | 
[**workplan_getfragmentfields_get**](WorkPlanApi.md#workplan_getfragmentfields_get) | **GET** /workplan/getfragmentfields | 
[**workplan_getfragmentresources_get**](WorkPlanApi.md#workplan_getfragmentresources_get) | **GET** /workplan/getfragmentresources | 
[**workplan_id_changetype_post**](WorkPlanApi.md#workplan_id_changetype_post) | **POST** /workplan/{Id}/changetype | 
[**workplan_id_config_get**](WorkPlanApi.md#workplan_id_config_get) | **GET** /workplan/{Id}/config | 
[**workplan_id_convert_conversionid_post**](WorkPlanApi.md#workplan_id_convert_conversionid_post) | **POST** /workplan/{id}/convert/{conversionid} | 
[**workplan_id_costs_task_id_post**](WorkPlanApi.md#workplan_id_costs_task_id_post) | **POST** /workplan/{Id}/costs/{taskId} | 
[**workplan_id_delete**](WorkPlanApi.md#workplan_id_delete) | **DELETE** /workplan/{id} | 
[**workplan_id_getastemplate_get**](WorkPlanApi.md#workplan_id_getastemplate_get) | **GET** /workplan/{id}/getastemplate | 
[**workplan_id_insertfragment_post**](WorkPlanApi.md#workplan_id_insertfragment_post) | **POST** /workplan/{id}/insertfragment | 
[**workplan_id_post**](WorkPlanApi.md#workplan_id_post) | **POST** /workplan/{Id} | 
[**workplan_id_revenue_post**](WorkPlanApi.md#workplan_id_revenue_post) | **POST** /workplan/{Id}/revenue | 
[**workplan_id_savefragment_post**](WorkPlanApi.md#workplan_id_savefragment_post) | **POST** /workplan/{id}/savefragment | 
[**workplan_id_split_delete**](WorkPlanApi.md#workplan_id_split_delete) | **DELETE** /workplan/{Id}/split | 
[**workplan_id_split_post**](WorkPlanApi.md#workplan_id_split_post) | **POST** /workplan/{Id}/split | 
[**workplan_id_tasks_get**](WorkPlanApi.md#workplan_id_tasks_get) | **GET** /workplan/{id}/tasks | 
[**workplan_id_tasks_post**](WorkPlanApi.md#workplan_id_tasks_post) | **POST** /workplan/{id}/tasks | 
[**workplan_id_tasks_taskid_assignments_post**](WorkPlanApi.md#workplan_id_tasks_taskid_assignments_post) | **POST** /workplan/{id}/tasks/{taskid}/assignments | 
[**workplan_id_tasks_taskid_assignments_user_id_delete**](WorkPlanApi.md#workplan_id_tasks_taskid_assignments_user_id_delete) | **DELETE** /workplan/{id}/tasks/{taskid}/assignments/{UserId} | 
[**workplan_id_tasks_taskid_delete**](WorkPlanApi.md#workplan_id_tasks_taskid_delete) | **DELETE** /workplan/{id}/tasks/{taskid} | 
[**workplan_id_tasks_taskid_get**](WorkPlanApi.md#workplan_id_tasks_taskid_get) | **GET** /workplan/{id}/tasks/{taskid} | 
[**workplan_id_tasks_taskid_post**](WorkPlanApi.md#workplan_id_tasks_taskid_post) | **POST** /workplan/{id}/tasks/{taskid} | 
[**workplan_id_tasks_taskid_updateassignments_post**](WorkPlanApi.md#workplan_id_tasks_taskid_updateassignments_post) | **POST** /workplan/{id}/tasks/{taskid}/updateassignments | 
[**workplan_id_updatefragment_post**](WorkPlanApi.md#workplan_id_updatefragment_post) | **POST** /workplan/{id}/updatefragment | 
[**workplan_id_versions_did_delete**](WorkPlanApi.md#workplan_id_versions_did_delete) | **DELETE** /workplan/{id}/versions/{did} | 
[**workplan_id_versions_get**](WorkPlanApi.md#workplan_id_versions_get) | **GET** /workplan/{id}/versions | 
[**workplan_plan_id_comments_get**](WorkPlanApi.md#workplan_plan_id_comments_get) | **GET** /workplan/{PlanId}/comments | 
[**workplan_plan_id_comments_id_delete**](WorkPlanApi.md#workplan_plan_id_comments_id_delete) | **DELETE** /workplan/{PlanId}/comments/{id} | 
[**workplan_plan_id_comments_post**](WorkPlanApi.md#workplan_plan_id_comments_post) | **POST** /workplan/{PlanId}/comments | 
[**workplan_plan_id_get**](WorkPlanApi.md#workplan_plan_id_get) | **GET** /workplan/{PlanId} | 
[**workplan_plan_id_processhistory_get**](WorkPlanApi.md#workplan_plan_id_processhistory_get) | **GET** /workplan/{PlanId}/processhistory | 
[**workplan_plan_id_ratetables_post**](WorkPlanApi.md#workplan_plan_id_ratetables_post) | **POST** /workplan/{PlanId}/ratetables | 
[**workplan_plan_id_sharedwithteam_delete**](WorkPlanApi.md#workplan_plan_id_sharedwithteam_delete) | **DELETE** /workplan/{PlanId}/sharedwithteam | 
[**workplan_plan_id_sharedwithteam_get**](WorkPlanApi.md#workplan_plan_id_sharedwithteam_get) | **GET** /workplan/{PlanId}/sharedwithteam | 
[**workplan_plan_id_sharedwithteam_post**](WorkPlanApi.md#workplan_plan_id_sharedwithteam_post) | **POST** /workplan/{PlanId}/sharedwithteam | 
[**workplan_plan_id_siblings_get**](WorkPlanApi.md#workplan_plan_id_siblings_get) | **GET** /workplan/{PlanId}/siblings | 
[**workplan_plan_id_step_approve_post**](WorkPlanApi.md#workplan_plan_id_step_approve_post) | **POST** /workplan/{PlanId}/step/approve | 
[**workplan_plan_id_step_post**](WorkPlanApi.md#workplan_plan_id_step_post) | **POST** /workplan/{PlanId}/step | 
[**workplan_plan_id_subplans_get**](WorkPlanApi.md#workplan_plan_id_subplans_get) | **GET** /workplan/{PlanId}/subplans | 
[**workplan_plan_id_subplans_post**](WorkPlanApi.md#workplan_plan_id_subplans_post) | **POST** /workplan/{PlanId}/subplans | 
[**workplan_plan_id_user_delete**](WorkPlanApi.md#workplan_plan_id_user_delete) | **DELETE** /workplan/{PlanId}/user | 
[**workplan_plan_id_user_get**](WorkPlanApi.md#workplan_plan_id_user_get) | **GET** /workplan/{PlanId}/user | 
[**workplan_plan_id_user_post**](WorkPlanApi.md#workplan_plan_id_user_post) | **POST** /workplan/{PlanId}/user | 
[**workplan_post**](WorkPlanApi.md#workplan_post) | **POST** /workplan | 
[**workplan_uploadaitemplate_post**](WorkPlanApi.md#workplan_uploadaitemplate_post) | **POST** /workplan/uploadaitemplate | 
[**workplan_uploadjson_post**](WorkPlanApi.md#workplan_uploadjson_post) | **POST** /workplan/uploadjson | 
[**workplan_user_levels_get**](WorkPlanApi.md#workplan_user_levels_get) | **GET** /workplan/user/levels | 

# **workplan_dependency_id_delete**
> HttpResponseMessage workplan_dependency_id_delete(id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_dependency_id_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_dependency_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_dependency_id_post**
> PlanDependency workplan_dependency_id_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlanDependency() # PlanDependency | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_dependency_id_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_dependency_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlanDependency**](PlanDependency.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**PlanDependency**](PlanDependency.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_dependency_post**
> PlanDependency workplan_dependency_post(body)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlanDependency() # PlanDependency | 

try:
    api_response = api_instance.workplan_dependency_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_dependency_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlanDependency**](PlanDependency.md)|  | 

### Return type

[**PlanDependency**](PlanDependency.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_fields_field_id_post**
> PlannerColumn workplan_fields_field_id_post(body, field_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlannerColumnPost() # PlannerColumnPost | 
field_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_fields_field_id_post(body, field_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_fields_field_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlannerColumnPost**](PlannerColumnPost.md)|  | 
 **field_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**PlannerColumn**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_fields_get**
> list[PlannerColumn] workplan_fields_get(hide_system=hide_system)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
hide_system = True # bool |  (optional)

try:
    api_response = api_instance.workplan_fields_get(hide_system=hide_system)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_fields_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hide_system** | [**bool**](.md)|  | [optional] 

### Return type

[**list[PlannerColumn]**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_fields_post**
> PlannerColumn workplan_fields_post(body)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlannerColumnPost() # PlannerColumnPost | 

try:
    api_response = api_instance.workplan_fields_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_fields_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlannerColumnPost**](PlannerColumnPost.md)|  | 

### Return type

[**PlannerColumn**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_fields_reorder_post**
> HttpResponseMessage workplan_fields_reorder_post()



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.workplan_fields_reorder_post()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_fields_reorder_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_find_post**
> FindPlansReturn workplan_find_post(body)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.FindPlansRequest() # FindPlansRequest | 

try:
    api_response = api_instance.workplan_find_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_find_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FindPlansRequest**](FindPlansRequest.md)|  | 

### Return type

[**FindPlansReturn**](FindPlansReturn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_fragments_get**
> list[WorkPlanTemplate] workplan_fragments_get(fragment_category)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
fragment_category = 56 # int | 

try:
    api_response = api_instance.workplan_fragments_get(fragment_category)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_fragments_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fragment_category** | [**int**](.md)|  | 

### Return type

[**list[WorkPlanTemplate]**](WorkPlanTemplate.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_get**
> list[WorkPlan] workplan_get(filter_field, filter_value, show_archived=show_archived, show_templates=show_templates, built_in_field=built_in_field)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
filter_field = 'filter_field_example' # str | 
filter_value = 'filter_value_example' # str | 
show_archived = True # bool |  (optional)
show_templates = True # bool |  (optional)
built_in_field = True # bool |  (optional)

try:
    api_response = api_instance.workplan_get(filter_field, filter_value, show_archived=show_archived, show_templates=show_templates, built_in_field=built_in_field)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter_field** | [**str**](.md)|  | 
 **filter_value** | [**str**](.md)|  | 
 **show_archived** | [**bool**](.md)|  | [optional] 
 **show_templates** | [**bool**](.md)|  | [optional] 
 **built_in_field** | [**bool**](.md)|  | [optional] 

### Return type

[**list[WorkPlan]**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_getfragmentfields_get**
> list[FragmentFieldInfo] workplan_getfragmentfields_get(fragment_id, category, sub_category)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
fragment_id = 'fragment_id_example' # str | 
category = 56 # int | 
sub_category = 56 # int | 

try:
    api_response = api_instance.workplan_getfragmentfields_get(fragment_id, category, sub_category)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_getfragmentfields_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fragment_id** | [**str**](.md)|  | 
 **category** | [**int**](.md)|  | 
 **sub_category** | [**int**](.md)|  | 

### Return type

[**list[FragmentFieldInfo]**](FragmentFieldInfo.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_getfragmentresources_get**
> list[FragmentResourceInfo] workplan_getfragmentresources_get(fragment_id, category, sub_category, assignment_column)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
fragment_id = 'fragment_id_example' # str | 
category = 56 # int | 
sub_category = 56 # int | 
assignment_column = 'assignment_column_example' # str | 

try:
    api_response = api_instance.workplan_getfragmentresources_get(fragment_id, category, sub_category, assignment_column)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_getfragmentresources_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **fragment_id** | [**str**](.md)|  | 
 **category** | [**int**](.md)|  | 
 **sub_category** | [**int**](.md)|  | 
 **assignment_column** | [**str**](.md)|  | 

### Return type

[**list[FragmentResourceInfo]**](FragmentResourceInfo.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_changetype_post**
> WorkPlan workplan_id_changetype_post(id, plan_type, new_parent_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
plan_type = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
new_parent_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_changetype_post(id, plan_type, new_parent_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_changetype_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **plan_type** | [**GloballyUniqueIdentifier**](.md)|  | 
 **new_parent_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_config_get**
> WorkPlanConfig workplan_id_config_get(id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_config_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_config_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanConfig**](WorkPlanConfig.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_convert_conversionid_post**
> WorkPlan workplan_id_convert_conversionid_post(id, conversionid)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
conversionid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_convert_conversionid_post(id, conversionid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_convert_conversionid_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **conversionid** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_costs_task_id_post**
> object workplan_id_costs_task_id_post(id, task_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_costs_task_id_post(id, task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_costs_task_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_delete**
> HttpResponseMessage workplan_id_delete(id, archive=archive)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
archive = True # bool |  (optional)

try:
    api_response = api_instance.workplan_id_delete(id, archive=archive)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **archive** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_getastemplate_get**
> HttpResponseMessage workplan_id_getastemplate_get(id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_getastemplate_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_getastemplate_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_insertfragment_post**
> HttpResponseMessage workplan_id_insertfragment_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PostFragmentInfo() # PostFragmentInfo | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_insertfragment_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_insertfragment_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PostFragmentInfo**](PostFragmentInfo.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_post**
> HttpResponseMessage workplan_id_post(body, id, changed_fields=changed_fields)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.WorkPlanRequest() # WorkPlanRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
changed_fields = True # bool |  (optional)

try:
    api_response = api_instance.workplan_id_post(body, id, changed_fields=changed_fields)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkPlanRequest**](WorkPlanRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **changed_fields** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_revenue_post**
> list[CostRevenueResult] workplan_id_revenue_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.CostRevenueRequest() # CostRevenueRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_revenue_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_revenue_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CostRevenueRequest**](CostRevenueRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[CostRevenueResult]**](CostRevenueResult.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_savefragment_post**
> HttpResponseMessage workplan_id_savefragment_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.FragmentInfo() # FragmentInfo | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_savefragment_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_savefragment_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FragmentInfo**](FragmentInfo.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_split_delete**
> WorkPlan workplan_id_split_delete(id, field, lookup_value, split)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
field = 'field_example' # str | 
lookup_value = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
split = oneplan_sdk.client.swagger_client.DecimalNumber() # DecimalNumber | 

try:
    api_response = api_instance.workplan_id_split_delete(id, field, lookup_value, split)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_split_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **field** | [**str**](.md)|  | 
 **lookup_value** | [**GloballyUniqueIdentifier**](.md)|  | 
 **split** | [**DecimalNumber**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_split_post**
> WorkPlan workplan_id_split_post(id, field, lookup_value, split)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
field = 'field_example' # str | 
lookup_value = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
split = oneplan_sdk.client.swagger_client.DecimalNumber() # DecimalNumber | 

try:
    api_response = api_instance.workplan_id_split_post(id, field, lookup_value, split)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_split_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **field** | [**str**](.md)|  | 
 **lookup_value** | [**GloballyUniqueIdentifier**](.md)|  | 
 **split** | [**DecimalNumber**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_get**
> list[WorkPlanTask] workplan_id_tasks_get(id, has_updates, filter_field, filter_value)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
has_updates = True # bool | 
filter_field = 'filter_field_example' # str | 
filter_value = 'filter_value_example' # str | 

try:
    api_response = api_instance.workplan_id_tasks_get(id, has_updates, filter_field, filter_value)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **has_updates** | [**bool**](.md)|  | 
 **filter_field** | [**str**](.md)|  | 
 **filter_value** | [**str**](.md)|  | 

### Return type

[**list[WorkPlanTask]**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_post**
> WorkPlanTask workplan_id_tasks_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TasksRequest() # TasksRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_tasks_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TasksRequest**](TasksRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanTask**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_assignments_post**
> HttpResponseMessage workplan_id_tasks_taskid_assignments_post(id, taskid, user_id, units=units)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
units = 56 # int |  (optional)

try:
    api_response = api_instance.workplan_id_tasks_taskid_assignments_post(id, taskid, user_id, units=units)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_assignments_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **units** | [**int**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_assignments_user_id_delete**
> HttpResponseMessage workplan_id_tasks_taskid_assignments_user_id_delete(id, taskid, user_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_tasks_taskid_assignments_user_id_delete(id, taskid, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_assignments_user_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_delete**
> HttpResponseMessage workplan_id_tasks_taskid_delete(id, taskid, ignore_timesheet_hours=ignore_timesheet_hours)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
ignore_timesheet_hours = True # bool |  (optional)

try:
    api_response = api_instance.workplan_id_tasks_taskid_delete(id, taskid, ignore_timesheet_hours=ignore_timesheet_hours)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 
 **ignore_timesheet_hours** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_get**
> WorkPlanTask workplan_id_tasks_taskid_get(id, taskid)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_tasks_taskid_get(id, taskid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanTask**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_post**
> HttpResponseMessage workplan_id_tasks_taskid_post(body, id, taskid)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TasksRequest() # TasksRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_tasks_taskid_post(body, id, taskid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TasksRequest**](TasksRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_tasks_taskid_updateassignments_post**
> HttpResponseMessage workplan_id_tasks_taskid_updateassignments_post(body, id, taskid)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AssignmentRequest() # AssignmentRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_tasks_taskid_updateassignments_post(body, id, taskid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_tasks_taskid_updateassignments_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AssignmentRequest**](AssignmentRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_updatefragment_post**
> WorkPlan workplan_id_updatefragment_post(body, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.FragmentInfo() # FragmentInfo | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_updatefragment_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_updatefragment_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FragmentInfo**](FragmentInfo.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_versions_did_delete**
> HttpResponseMessage workplan_id_versions_did_delete(id, did)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
did = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_versions_did_delete(id, did)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_versions_did_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **did** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_id_versions_get**
> list[WorkPlanVersion] workplan_id_versions_get(id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_id_versions_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_id_versions_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[WorkPlanVersion]**](WorkPlanVersion.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_comments_get**
> CommentsResponse workplan_plan_id_comments_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_comments_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_comments_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**CommentsResponse**](CommentsResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_comments_id_delete**
> HttpResponseMessage workplan_plan_id_comments_id_delete(plan_id, id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_comments_id_delete(plan_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_comments_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_comments_post**
> TaskComment workplan_plan_id_comments_post(body, plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.CommentPost() # CommentPost | 
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_comments_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_comments_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CommentPost**](CommentPost.md)|  | 
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**TaskComment**](TaskComment.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_get**
> WorkPlan workplan_plan_id_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_processhistory_get**
> list[WorkPlanStageStep] workplan_plan_id_processhistory_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_processhistory_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_processhistory_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[WorkPlanStageStep]**](WorkPlanStageStep.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_ratetables_post**
> WorkPlan workplan_plan_id_ratetables_post(body, plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlanRateTable() # PlanRateTable | 
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_ratetables_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_ratetables_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlanRateTable**](PlanRateTable.md)|  | 
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_sharedwithteam_delete**
> HttpResponseMessage workplan_plan_id_sharedwithteam_delete(plan_id, team_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
team_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_sharedwithteam_delete(plan_id, team_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_sharedwithteam_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **team_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_sharedwithteam_get**
> list[TeamAccess] workplan_plan_id_sharedwithteam_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_sharedwithteam_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_sharedwithteam_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[TeamAccess]**](TeamAccess.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_sharedwithteam_post**
> HttpResponseMessage workplan_plan_id_sharedwithteam_post(body, plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TeamRequest() # TeamRequest | 
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_sharedwithteam_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_sharedwithteam_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamRequest**](TeamRequest.md)|  | 
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_siblings_get**
> list[WorkPlan] workplan_plan_id_siblings_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_siblings_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_siblings_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[WorkPlan]**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_step_approve_post**
> WorkPlan workplan_plan_id_step_approve_post(plan_id, state, comment)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
state = oneplan_sdk.client.swagger_client.ProcessState() # ProcessState | 
comment = 'comment_example' # str | 

try:
    api_response = api_instance.workplan_plan_id_step_approve_post(plan_id, state, comment)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_step_approve_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **state** | [**ProcessState**](.md)|  | 
 **comment** | [**str**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_step_post**
> WorkPlan workplan_plan_id_step_post(plan_id, step_name, step_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
step_name = 'step_name_example' # str | 
step_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_step_post(plan_id, step_name, step_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_step_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **step_name** | [**str**](.md)|  | 
 **step_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_subplans_get**
> list[Object] workplan_plan_id_subplans_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_subplans_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_subplans_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[Object]**](Object.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_subplans_post**
> WorkPlan workplan_plan_id_subplans_post(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_subplans_post(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_subplans_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_user_delete**
> HttpResponseMessage workplan_plan_id_user_delete(plan_id, user_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_user_delete(plan_id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_user_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_user_get**
> list[UserAccess] workplan_plan_id_user_get(plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_user_get(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_user_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[UserAccess]**](UserAccess.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_plan_id_user_post**
> HttpResponseMessage workplan_plan_id_user_post(body, plan_id)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.UserRequest() # UserRequest | 
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.workplan_plan_id_user_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_plan_id_user_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**UserRequest**](UserRequest.md)|  | 
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_post**
> WorkPlan workplan_post(body)



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.WorkPlanRequest() # WorkPlanRequest | 

try:
    api_response = api_instance.workplan_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkPlanRequest**](WorkPlanRequest.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_uploadaitemplate_post**
> HttpResponseMessage workplan_uploadaitemplate_post()



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.workplan_uploadaitemplate_post()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_uploadaitemplate_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_uploadjson_post**
> HttpResponseMessage workplan_uploadjson_post()



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.workplan_uploadjson_post()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_uploadjson_post: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workplan_user_levels_get**
> dict(str, str) workplan_user_levels_get()



### Example
```python
from __future__ import print_function
import time
import oneplan_sdk.client.swagger_client
from oneplan_sdk.client.swagger_client.rest import ApiException
from pprint import pprint
# Configure HTTP basic authorization: oneplan_api_auth
configuration = oneplan_sdk.client.swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = oneplan_sdk.client.swagger_client.WorkPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.workplan_user_levels_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkPlanApi->workplan_user_levels_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**dict(str, str)**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

