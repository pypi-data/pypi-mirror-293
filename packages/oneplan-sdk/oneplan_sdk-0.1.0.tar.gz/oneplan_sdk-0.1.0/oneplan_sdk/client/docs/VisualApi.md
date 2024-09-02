# oneplan_sdk.client.swagger_client.VisualApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**visual_dependency_post**](VisualApi.md#visual_dependency_post) | **POST** /visual/dependency | 
[**visual_modeler_dependency_post**](VisualApi.md#visual_modeler_dependency_post) | **POST** /visual/modeler/dependency | 
[**visual_modeler_runway_post**](VisualApi.md#visual_modeler_runway_post) | **POST** /visual/modeler/runway | 
[**visual_runway_post**](VisualApi.md#visual_runway_post) | **POST** /visual/runway | 

# **visual_dependency_post**
> list[RunwayResponsePlan] visual_dependency_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.VisualApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.RunwayPost() # RunwayPost | 

try:
    api_response = api_instance.visual_dependency_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VisualApi->visual_dependency_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RunwayPost**](RunwayPost.md)|  | 

### Return type

[**list[RunwayResponsePlan]**](RunwayResponsePlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **visual_modeler_dependency_post**
> list[RunwayResponsePlan] visual_modeler_dependency_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.VisualApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OrderedPost() # OrderedPost | 

try:
    api_response = api_instance.visual_modeler_dependency_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VisualApi->visual_modeler_dependency_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrderedPost**](OrderedPost.md)|  | 

### Return type

[**list[RunwayResponsePlan]**](RunwayResponsePlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **visual_modeler_runway_post**
> list[RunwayResponsePlan] visual_modeler_runway_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.VisualApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OrderedPost() # OrderedPost | 

try:
    api_response = api_instance.visual_modeler_runway_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VisualApi->visual_modeler_runway_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OrderedPost**](OrderedPost.md)|  | 

### Return type

[**list[RunwayResponsePlan]**](RunwayResponsePlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **visual_runway_post**
> list[RunwayResponsePlan] visual_runway_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.VisualApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.RunwayPost() # RunwayPost | 

try:
    api_response = api_instance.visual_runway_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VisualApi->visual_runway_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RunwayPost**](RunwayPost.md)|  | 

### Return type

[**list[RunwayResponsePlan]**](RunwayResponsePlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

