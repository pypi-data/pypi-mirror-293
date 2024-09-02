# oneplan_sdk.client.swagger_client.TestGanttApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**testgantt_gantt_post**](TestGanttApi.md#testgantt_gantt_post) | **POST** /testgantt/gantt | 

# **testgantt_gantt_post**
> GanttSyncResponse testgantt_gantt_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.TestGanttApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.SyncRequest() # SyncRequest | 

try:
    api_response = api_instance.testgantt_gantt_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TestGanttApi->testgantt_gantt_post: %s\n" % e)
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

