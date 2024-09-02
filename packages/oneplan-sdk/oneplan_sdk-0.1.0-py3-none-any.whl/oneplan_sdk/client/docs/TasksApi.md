# oneplan_sdk.client.swagger_client.TasksApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tasks_dependency_all_get**](TasksApi.md#tasks_dependency_all_get) | **GET** /tasks/dependency/all | 
[**tasks_dependency_task_id_dep_id_delete**](TasksApi.md#tasks_dependency_task_id_dep_id_delete) | **DELETE** /tasks/dependency/{TaskId}/{DepId} | 
[**tasks_dependency_task_id_dep_id_post**](TasksApi.md#tasks_dependency_task_id_dep_id_post) | **POST** /tasks/dependency/{TaskId}/{DepId} | 
[**tasks_dependency_task_id_get**](TasksApi.md#tasks_dependency_task_id_get) | **GET** /tasks/dependency/{TaskId} | 
[**tasks_fields_get**](TasksApi.md#tasks_fields_get) | **GET** /tasks/fields | 
[**tasks_fields_id_delete**](TasksApi.md#tasks_fields_id_delete) | **DELETE** /tasks/fields/{id} | 
[**tasks_fields_id_post**](TasksApi.md#tasks_fields_id_post) | **POST** /tasks/fields/{id} | 
[**tasks_fields_post**](TasksApi.md#tasks_fields_post) | **POST** /tasks/fields | 
[**tasks_id_comments_get**](TasksApi.md#tasks_id_comments_get) | **GET** /tasks/{id}/comments | 
[**tasks_id_comments_post**](TasksApi.md#tasks_id_comments_post) | **POST** /tasks/{id}/comments | 
[**tasks_localfields_get**](TasksApi.md#tasks_localfields_get) | **GET** /tasks/localfields | 
[**tasks_taskid_comments_id_delete**](TasksApi.md#tasks_taskid_comments_id_delete) | **DELETE** /tasks/{taskid}/comments/{id} | 

# **tasks_dependency_all_get**
> list[WorkPlanDep] tasks_dependency_all_get()



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.tasks_dependency_all_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_dependency_all_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[WorkPlanDep]**](WorkPlanDep.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_dependency_task_id_dep_id_delete**
> HttpResponseMessage tasks_dependency_task_id_dep_id_delete(task_id, dep_id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
dep_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_dependency_task_id_dep_id_delete(task_id, dep_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_dependency_task_id_dep_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **dep_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_dependency_task_id_dep_id_post**
> WorkPlanDep tasks_dependency_task_id_dep_id_post(task_id, dep_id, type, lag, lag_unit=lag_unit)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
dep_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
type = oneplan_sdk.client.swagger_client.DependencyType() # DependencyType | 
lag = 56 # int | 
lag_unit = 'lag_unit_example' # str |  (optional)

try:
    api_response = api_instance.tasks_dependency_task_id_dep_id_post(task_id, dep_id, type, lag, lag_unit=lag_unit)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_dependency_task_id_dep_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **dep_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **type** | [**DependencyType**](.md)|  | 
 **lag** | [**int**](.md)|  | 
 **lag_unit** | [**str**](.md)|  | [optional] 

### Return type

[**WorkPlanDep**](WorkPlanDep.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_dependency_task_id_get**
> list[WorkPlanDep] tasks_dependency_task_id_get(task_id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_dependency_task_id_get(task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_dependency_task_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[WorkPlanDep]**](WorkPlanDep.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_fields_get**
> list[PlannerColumn] tasks_fields_get(hide_system=hide_system)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
hide_system = True # bool |  (optional)

try:
    api_response = api_instance.tasks_fields_get(hide_system=hide_system)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_fields_get: %s\n" % e)
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

# **tasks_fields_id_delete**
> list[PlannerColumn] tasks_fields_id_delete(id, work_plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
work_plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_fields_id_delete(id, work_plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_fields_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **work_plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[PlannerColumn]**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_fields_id_post**
> PlannerColumn tasks_fields_id_post(body, work_plan_id, id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlannerColumnPost() # PlannerColumnPost | 
work_plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_fields_id_post(body, work_plan_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_fields_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlannerColumnPost**](PlannerColumnPost.md)|  | 
 **work_plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**PlannerColumn**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_fields_post**
> PlannerColumn tasks_fields_post(body, work_plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlannerColumnPost() # PlannerColumnPost | 
work_plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_fields_post(body, work_plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_fields_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlannerColumnPost**](PlannerColumnPost.md)|  | 
 **work_plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**PlannerColumn**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_id_comments_get**
> CommentsResponse tasks_id_comments_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_id_comments_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_id_comments_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**CommentsResponse**](CommentsResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_id_comments_post**
> TaskComment tasks_id_comments_post(body, notificationid, id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TaskComment() # TaskComment | 
notificationid = 'notificationid_example' # str | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_id_comments_post(body, notificationid, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_id_comments_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TaskComment**](TaskComment.md)|  | 
 **notificationid** | [**str**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**TaskComment**](TaskComment.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_localfields_get**
> list[PlannerColumn] tasks_localfields_get(work_plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
work_plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.tasks_localfields_get(work_plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_localfields_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **work_plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[PlannerColumn]**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tasks_taskid_comments_id_delete**
> HttpResponseMessage tasks_taskid_comments_id_delete(taskid, id, notificationid)



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
api_instance = oneplan_sdk.client.swagger_client.TasksApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
taskid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
notificationid = 'notificationid_example' # str | 

try:
    api_response = api_instance.tasks_taskid_comments_id_delete(taskid, id, notificationid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->tasks_taskid_comments_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **taskid** | [**GloballyUniqueIdentifier**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **notificationid** | [**str**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

