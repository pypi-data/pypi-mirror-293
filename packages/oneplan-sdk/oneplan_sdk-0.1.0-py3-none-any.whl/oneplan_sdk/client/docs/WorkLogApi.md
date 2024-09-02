# oneplan_sdk.client.swagger_client.WorkLogApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**worklog_classes_get**](WorkLogApi.md#worklog_classes_get) | **GET** /worklog/classes | 
[**worklog_get**](WorkLogApi.md#worklog_get) | **GET** /worklog | 
[**worklog_post**](WorkLogApi.md#worklog_post) | **POST** /worklog | 

# **worklog_classes_get**
> DataTable worklog_classes_get(task_id, external_id, integration_id)



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
api_instance = oneplan_sdk.client.swagger_client.WorkLogApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
external_id = 'external_id_example' # str | 
integration_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.worklog_classes_get(task_id, external_id, integration_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkLogApi->worklog_classes_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **external_id** | [**str**](.md)|  | 
 **integration_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**DataTable**](DataTable.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **worklog_get**
> WorkLogInfo worklog_get(task_id, external_id, integration_id, log_date)



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
api_instance = oneplan_sdk.client.swagger_client.WorkLogApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
task_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
external_id = 'external_id_example' # str | 
integration_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
log_date = '2013-10-20' # date | 

try:
    api_response = api_instance.worklog_get(task_id, external_id, integration_id, log_date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkLogApi->worklog_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **task_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **external_id** | [**str**](.md)|  | 
 **integration_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **log_date** | [**date**](.md)|  | 

### Return type

[**WorkLogInfo**](WorkLogInfo.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **worklog_post**
> WorkLogResponse worklog_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.WorkLogApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.WorkLogPost() # WorkLogPost | 

try:
    api_response = api_instance.worklog_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WorkLogApi->worklog_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WorkLogPost**](WorkLogPost.md)|  | 

### Return type

[**WorkLogResponse**](WorkLogResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

