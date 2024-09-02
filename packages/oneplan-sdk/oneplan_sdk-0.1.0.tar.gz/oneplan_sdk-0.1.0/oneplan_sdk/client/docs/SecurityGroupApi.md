# oneplan_sdk.client.swagger_client.SecurityGroupApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**securitygroups_admin_get**](SecurityGroupApi.md#securitygroups_admin_get) | **GET** /securitygroups/admin | 
[**securitygroups_bulk_patch**](SecurityGroupApi.md#securitygroups_bulk_patch) | **PATCH** /securitygroups/bulk | 
[**securitygroups_bulk_post**](SecurityGroupApi.md#securitygroups_bulk_post) | **POST** /securitygroups/bulk | 
[**securitygroups_default_get**](SecurityGroupApi.md#securitygroups_default_get) | **GET** /securitygroups/default | 
[**securitygroups_get**](SecurityGroupApi.md#securitygroups_get) | **GET** /securitygroups | 
[**securitygroups_id_delete**](SecurityGroupApi.md#securitygroups_id_delete) | **DELETE** /securitygroups/{id} | 
[**securitygroups_id_get**](SecurityGroupApi.md#securitygroups_id_get) | **GET** /securitygroups/{id} | 
[**securitygroups_id_post**](SecurityGroupApi.md#securitygroups_id_post) | **POST** /securitygroups/{id} | 
[**securitygroups_post**](SecurityGroupApi.md#securitygroups_post) | **POST** /securitygroups | 
[**securitygroups_setdefaultproperty_post**](SecurityGroupApi.md#securitygroups_setdefaultproperty_post) | **POST** /securitygroups/setdefaultproperty | 

# **securitygroups_admin_get**
> list[OnePlanSecurityGroup] securitygroups_admin_get()



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.securitygroups_admin_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_admin_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OnePlanSecurityGroup]**](OnePlanSecurityGroup.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_bulk_patch**
> HttpResponseMessage securitygroups_bulk_patch(body)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanSecurityGroup() # OnePlanSecurityGroup | 

try:
    api_response = api_instance.securitygroups_bulk_patch(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_bulk_patch: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_bulk_post**
> HttpResponseMessage securitygroups_bulk_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanSecurityGroup() # OnePlanSecurityGroup | 

try:
    api_response = api_instance.securitygroups_bulk_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_bulk_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_default_get**
> OnePlanSecurityGroup securitygroups_default_get()



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.securitygroups_default_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_default_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_get**
> list[OnePlanSecurityGroup] securitygroups_get()



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.securitygroups_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OnePlanSecurityGroup]**](OnePlanSecurityGroup.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_id_delete**
> HttpResponseMessage securitygroups_id_delete(id)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.securitygroups_id_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_id_delete: %s\n" % e)
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

# **securitygroups_id_get**
> OnePlanSecurityGroup securitygroups_id_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.securitygroups_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_id_post**
> HttpResponseMessage securitygroups_id_post(body, id)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanSecurityGroup() # OnePlanSecurityGroup | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.securitygroups_id_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_post**
> HttpResponseMessage securitygroups_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanSecurityGroup() # OnePlanSecurityGroup | 

try:
    api_response = api_instance.securitygroups_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanSecurityGroup**](OnePlanSecurityGroup.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **securitygroups_setdefaultproperty_post**
> HttpResponseMessage securitygroups_setdefaultproperty_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.SecurityGroupApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.SecurityGroupDefaultPropertyRequest() # SecurityGroupDefaultPropertyRequest | 

try:
    api_response = api_instance.securitygroups_setdefaultproperty_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecurityGroupApi->securitygroups_setdefaultproperty_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SecurityGroupDefaultPropertyRequest**](SecurityGroupDefaultPropertyRequest.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

