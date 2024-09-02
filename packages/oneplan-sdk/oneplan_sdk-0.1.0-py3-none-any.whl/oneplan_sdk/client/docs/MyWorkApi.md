# oneplan_sdk.client.swagger_client.MyWorkApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mywork_accept_update_post**](MyWorkApi.md#mywork_accept_update_post) | **POST** /mywork/AcceptUpdate | 
[**mywork_activities_get**](MyWorkApi.md#mywork_activities_get) | **GET** /mywork/activities | 
[**mywork_activities_post**](MyWorkApi.md#mywork_activities_post) | **POST** /mywork/activities | 
[**mywork_getupdate_id_get**](MyWorkApi.md#mywork_getupdate_id_get) | **GET** /mywork/getupdate/{id} | 
[**mywork_id_post**](MyWorkApi.md#mywork_id_post) | **POST** /mywork/{id} | 
[**mywork_reject_update_post**](MyWorkApi.md#mywork_reject_update_post) | **POST** /mywork/RejectUpdate | 
[**mywork_statusfields_get**](MyWorkApi.md#mywork_statusfields_get) | **GET** /mywork/statusfields | 
[**mywork_tasks_get**](MyWorkApi.md#mywork_tasks_get) | **GET** /mywork/tasks | 

# **mywork_accept_update_post**
> WorkPlanTask mywork_accept_update_post(task_id)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.mywork_accept_update_post(task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_accept_update_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanTask**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_activities_get**
> BoardResponse mywork_activities_get()



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.mywork_activities_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_activities_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**BoardResponse**](BoardResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_activities_post**
> GanttSyncResponse mywork_activities_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.SyncRequest() # SyncRequest | 

try:
    api_response = api_instance.mywork_activities_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_activities_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SyncRequest**](SyncRequest.md)|  | 

### Return type

[**GanttSyncResponse**](GanttSyncResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_getupdate_id_get**
> StatusUpdateClass mywork_getupdate_id_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.mywork_getupdate_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_getupdate_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**StatusUpdateClass**](StatusUpdateClass.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_id_post**
> WorkPlanTask mywork_id_post(id)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.mywork_id_post(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanTask**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_reject_update_post**
> WorkPlanTask mywork_reject_update_post(task_id)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.mywork_reject_update_post(task_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_reject_update_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlanTask**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_statusfields_get**
> list[PlannerColumn] mywork_statusfields_get()



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.mywork_statusfields_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_statusfields_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[PlannerColumn]**](PlannerColumn.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mywork_tasks_get**
> list[WorkPlanTask] mywork_tasks_get(period_start, period_end, user_id, show_complete=show_complete)



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
api_instance = oneplan_sdk.client.swagger_client.MyWorkApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
period_start = '2013-10-20' # date | 
period_end = '2013-10-20' # date | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
show_complete = True # bool |  (optional)

try:
    api_response = api_instance.mywork_tasks_get(period_start, period_end, user_id, show_complete=show_complete)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MyWorkApi->mywork_tasks_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period_start** | [**date**](.md)|  | 
 **period_end** | [**date**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **show_complete** | [**bool**](.md)|  | [optional] 

### Return type

[**list[WorkPlanTask]**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

