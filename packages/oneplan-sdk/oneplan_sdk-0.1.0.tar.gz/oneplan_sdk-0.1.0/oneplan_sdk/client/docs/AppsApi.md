# oneplan_sdk.client.swagger_client.AppsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**allapps_get**](AppsApi.md#allapps_get) | **GET** /allapps | 
[**apps_delete**](AppsApi.md#apps_delete) | **DELETE** /apps | 
[**apps_get**](AppsApi.md#apps_get) | **GET** /apps | 
[**apps_post**](AppsApi.md#apps_post) | **POST** /apps | 

# **allapps_get**
> list[AppDefinition] allapps_get(hide_installed=hide_installed)



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
api_instance = oneplan_sdk.client.swagger_client.AppsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
hide_installed = True # bool |  (optional)

try:
    api_response = api_instance.allapps_get(hide_installed=hide_installed)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppsApi->allapps_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hide_installed** | [**bool**](.md)|  | [optional] 

### Return type

[**list[AppDefinition]**](AppDefinition.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apps_delete**
> HttpResponseMessage apps_delete(app_id)



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
api_instance = oneplan_sdk.client.swagger_client.AppsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
app_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.apps_delete(app_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppsApi->apps_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apps_get**
> list[AppDefinition] apps_get(closed=closed)



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
api_instance = oneplan_sdk.client.swagger_client.AppsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
closed = True # bool |  (optional)

try:
    api_response = api_instance.apps_get(closed=closed)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppsApi->apps_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **closed** | [**bool**](.md)|  | [optional] 

### Return type

[**list[AppDefinition]**](AppDefinition.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apps_post**
> HttpResponseMessage apps_post(app_id)



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
api_instance = oneplan_sdk.client.swagger_client.AppsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
app_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.apps_post(app_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AppsApi->apps_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **app_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

