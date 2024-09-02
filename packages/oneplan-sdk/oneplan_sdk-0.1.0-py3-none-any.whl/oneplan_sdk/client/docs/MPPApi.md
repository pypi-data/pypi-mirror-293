# oneplan_sdk.client.swagger_client.MPPApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mpp_createplan_post**](MPPApi.md#mpp_createplan_post) | **POST** /mpp/createplan | 
[**mpp_templates_get**](MPPApi.md#mpp_templates_get) | **GET** /mpp/templates | 

# **mpp_createplan_post**
> WorkPlan mpp_createplan_post(template, plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.MPPApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
template = 'template_example' # str | 
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.mpp_createplan_post(template, plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MPPApi->mpp_createplan_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **template** | [**str**](.md)|  | 
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**WorkPlan**](WorkPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mpp_templates_get**
> list[MPPTemplate] mpp_templates_get()



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
api_instance = oneplan_sdk.client.swagger_client.MPPApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.mpp_templates_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MPPApi->mpp_templates_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[MPPTemplate]**](MPPTemplate.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

