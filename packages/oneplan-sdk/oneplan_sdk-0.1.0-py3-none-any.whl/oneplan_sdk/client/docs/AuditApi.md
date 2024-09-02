# oneplan_sdk.client.swagger_client.AuditApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**audit_financials_post**](AuditApi.md#audit_financials_post) | **POST** /audit/financials | 
[**audit_plan_post**](AuditApi.md#audit_plan_post) | **POST** /audit/plan | 
[**audit_plans_deleted_post**](AuditApi.md#audit_plans_deleted_post) | **POST** /audit/plans/deleted | 
[**audit_resource_post**](AuditApi.md#audit_resource_post) | **POST** /audit/resource | 
[**audit_resources_deleted_post**](AuditApi.md#audit_resources_deleted_post) | **POST** /audit/resources/deleted | 
[**audit_resources_plan_id_post**](AuditApi.md#audit_resources_plan_id_post) | **POST** /audit/resources/{planId} | 
[**audit_sharedwith_plan_id_post**](AuditApi.md#audit_sharedwith_plan_id_post) | **POST** /audit/sharedwith/{planId} | 
[**audit_tasks_post**](AuditApi.md#audit_tasks_post) | **POST** /audit/tasks | 

# **audit_financials_post**
> list[AuditFinancialPlans] audit_financials_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditFinancialPlansQuery() # AuditFinancialPlansQuery | 

try:
    api_response = api_instance.audit_financials_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_financials_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditFinancialPlansQuery**](AuditFinancialPlansQuery.md)|  | 

### Return type

[**list[AuditFinancialPlans]**](AuditFinancialPlans.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_plan_post**
> list[AuditPlans] audit_plan_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditPlansQuery() # AuditPlansQuery | 

try:
    api_response = api_instance.audit_plan_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_plan_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditPlansQuery**](AuditPlansQuery.md)|  | 

### Return type

[**list[AuditPlans]**](AuditPlans.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_plans_deleted_post**
> list[AuditPlans] audit_plans_deleted_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditPlansQuery() # AuditPlansQuery | 

try:
    api_response = api_instance.audit_plans_deleted_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_plans_deleted_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditPlansQuery**](AuditPlansQuery.md)|  | 

### Return type

[**list[AuditPlans]**](AuditPlans.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_resource_post**
> list[AuditResource] audit_resource_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditResourceQuery() # AuditResourceQuery | 

try:
    api_response = api_instance.audit_resource_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_resource_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditResourceQuery**](AuditResourceQuery.md)|  | 

### Return type

[**list[AuditResource]**](AuditResource.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_resources_deleted_post**
> list[AuditResource] audit_resources_deleted_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditResourceQuery() # AuditResourceQuery | 

try:
    api_response = api_instance.audit_resources_deleted_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_resources_deleted_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditResourceQuery**](AuditResourceQuery.md)|  | 

### Return type

[**list[AuditResource]**](AuditResource.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_resources_plan_id_post**
> list[AuditResourcePlans] audit_resources_plan_id_post(body, plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditResourcePlansQuery() # AuditResourcePlansQuery | 
plan_id = 'plan_id_example' # str | 

try:
    api_response = api_instance.audit_resources_plan_id_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_resources_plan_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditResourcePlansQuery**](AuditResourcePlansQuery.md)|  | 
 **plan_id** | [**str**](.md)|  | 

### Return type

[**list[AuditResourcePlans]**](AuditResourcePlans.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_sharedwith_plan_id_post**
> list[AuditSharedWith] audit_sharedwith_plan_id_post(body, plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditSharedWithQuery() # AuditSharedWithQuery | 
plan_id = 'plan_id_example' # str | 

try:
    api_response = api_instance.audit_sharedwith_plan_id_post(body, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_sharedwith_plan_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditSharedWithQuery**](AuditSharedWithQuery.md)|  | 
 **plan_id** | [**str**](.md)|  | 

### Return type

[**list[AuditSharedWith]**](AuditSharedWith.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **audit_tasks_post**
> list[AuditTasks] audit_tasks_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.AuditApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AuditTasksQuery() # AuditTasksQuery | 

try:
    api_response = api_instance.audit_tasks_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuditApi->audit_tasks_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AuditTasksQuery**](AuditTasksQuery.md)|  | 

### Return type

[**list[AuditTasks]**](AuditTasks.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

