# oneplan_sdk.client.swagger_client.GlobalSearchApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**globalsearch_favorite_get**](GlobalSearchApi.md#globalsearch_favorite_get) | **GET** /globalsearch/favorite | 
[**globalsearch_recentplans_get**](GlobalSearchApi.md#globalsearch_recentplans_get) | **GET** /globalsearch/recentplans | 
[**globalsearch_search_post**](GlobalSearchApi.md#globalsearch_search_post) | **POST** /globalsearch/search | 

# **globalsearch_favorite_get**
> list[GlobalSearchPlan] globalsearch_favorite_get()



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
api_instance = oneplan_sdk.client.swagger_client.GlobalSearchApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.globalsearch_favorite_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalSearchApi->globalsearch_favorite_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[GlobalSearchPlan]**](GlobalSearchPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **globalsearch_recentplans_get**
> list[GlobalSearchPlan] globalsearch_recentplans_get()



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
api_instance = oneplan_sdk.client.swagger_client.GlobalSearchApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.globalsearch_recentplans_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalSearchApi->globalsearch_recentplans_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[GlobalSearchPlan]**](GlobalSearchPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **globalsearch_search_post**
> list[GlobalSearchPlan] globalsearch_search_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.GlobalSearchApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.GlobalSearchRequest() # GlobalSearchRequest | 

try:
    api_response = api_instance.globalsearch_search_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling GlobalSearchApi->globalsearch_search_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**GlobalSearchRequest**](GlobalSearchRequest.md)|  | 

### Return type

[**list[GlobalSearchPlan]**](GlobalSearchPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

