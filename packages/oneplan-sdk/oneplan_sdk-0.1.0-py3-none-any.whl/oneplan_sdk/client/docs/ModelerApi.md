# oneplan_sdk.client.swagger_client.ModelerApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**modeler_currencyfields_get**](ModelerApi.md#modeler_currencyfields_get) | **GET** /modeler/currencyfields | 
[**modeler_delete_delete**](ModelerApi.md#modeler_delete_delete) | **DELETE** /modeler/delete | 
[**modeler_folder_delete_delete**](ModelerApi.md#modeler_folder_delete_delete) | **DELETE** /modeler/folder/delete | 
[**modeler_folder_new_post**](ModelerApi.md#modeler_folder_new_post) | **POST** /modeler/folder/new | 
[**modeler_folder_tree_get**](ModelerApi.md#modeler_folder_tree_get) | **GET** /modeler/folder/tree | 
[**modeler_folder_update_post**](ModelerApi.md#modeler_folder_update_post) | **POST** /modeler/folder/update | 
[**modeler_folders_get**](ModelerApi.md#modeler_folders_get) | **GET** /modeler/folders | 
[**modeler_model_get**](ModelerApi.md#modeler_model_get) | **GET** /modeler/model | 
[**modeler_model_loadgantt_post**](ModelerApi.md#modeler_model_loadgantt_post) | **POST** /modeler/model/loadgantt | 
[**modeler_models_get**](ModelerApi.md#modeler_models_get) | **GET** /modeler/models | 
[**modeler_new_post**](ModelerApi.md#modeler_new_post) | **POST** /modeler/new | 
[**modeler_scenarios_get**](ModelerApi.md#modeler_scenarios_get) | **GET** /modeler/scenarios | 
[**modeler_tree_get**](ModelerApi.md#modeler_tree_get) | **GET** /modeler/tree | 
[**modeler_update_post**](ModelerApi.md#modeler_update_post) | **POST** /modeler/update | 
[**modeler_users_addupdateuser_post**](ModelerApi.md#modeler_users_addupdateuser_post) | **POST** /modeler/users/addupdateuser | 
[**modeler_users_deleteuser_post**](ModelerApi.md#modeler_users_deleteuser_post) | **POST** /modeler/users/deleteuser | 
[**modeler_users_get**](ModelerApi.md#modeler_users_get) | **GET** /modeler/users | 

# **modeler_currencyfields_get**
> list[PlannerColumn] modeler_currencyfields_get(hide_system=hide_system)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
hide_system = True # bool |  (optional)

try:
    api_response = api_instance.modeler_currencyfields_get(hide_system=hide_system)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_currencyfields_get: %s\n" % e)
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

# **modeler_delete_delete**
> HttpResponseMessage modeler_delete_delete()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_delete_delete()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_delete_delete: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_folder_delete_delete**
> HttpResponseMessage modeler_folder_delete_delete()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_folder_delete_delete()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_folder_delete_delete: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_folder_new_post**
> ModelerFolder modeler_folder_new_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ModelerFolder() # ModelerFolder | 

try:
    api_response = api_instance.modeler_folder_new_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_folder_new_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelerFolder**](ModelerFolder.md)|  | 

### Return type

[**ModelerFolder**](ModelerFolder.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_folder_tree_get**
> object modeler_folder_tree_get()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_folder_tree_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_folder_tree_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_folder_update_post**
> ModelerFolder modeler_folder_update_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ModelerFolder() # ModelerFolder | 

try:
    api_response = api_instance.modeler_folder_update_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_folder_update_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelerFolder**](ModelerFolder.md)|  | 

### Return type

[**ModelerFolder**](ModelerFolder.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_folders_get**
> list[ModelerFolder] modeler_folders_get()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_folders_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_folders_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ModelerFolder]**](ModelerFolder.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_model_get**
> ModelerModel modeler_model_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.modeler_model_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_model_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**ModelerModel**](ModelerModel.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_model_loadgantt_post**
> object modeler_model_loadgantt_post(id, current_scenario_info)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
current_scenario_info = 'current_scenario_info_example' # str | 

try:
    api_response = api_instance.modeler_model_loadgantt_post(id, current_scenario_info)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_model_loadgantt_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **current_scenario_info** | [**str**](.md)|  | 

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_models_get**
> list[ModelerModel] modeler_models_get()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_models_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_models_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ModelerModel]**](ModelerModel.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_new_post**
> ModelerModel modeler_new_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ModelerModel() # ModelerModel | 

try:
    api_response = api_instance.modeler_new_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_new_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelerModel**](ModelerModel.md)|  | 

### Return type

[**ModelerModel**](ModelerModel.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_scenarios_get**
> list[ModelScenario] modeler_scenarios_get()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_scenarios_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_scenarios_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ModelScenario]**](ModelScenario.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_tree_get**
> object modeler_tree_get()



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.modeler_tree_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_tree_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_update_post**
> ModelerModel modeler_update_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ModelerModel() # ModelerModel | 

try:
    api_response = api_instance.modeler_update_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_update_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelerModel**](ModelerModel.md)|  | 

### Return type

[**ModelerModel**](ModelerModel.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_users_addupdateuser_post**
> list[User] modeler_users_addupdateuser_post(body, entity_id, is_folder)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.User() # User | 
entity_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
is_folder = True # bool | 

try:
    api_response = api_instance.modeler_users_addupdateuser_post(body, entity_id, is_folder)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_users_addupdateuser_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**User**](User.md)|  | 
 **entity_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **is_folder** | [**bool**](.md)|  | 

### Return type

[**list[User]**](User.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_users_deleteuser_post**
> HttpResponseMessage modeler_users_deleteuser_post(entity_id, user_id, is_folder)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
entity_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
is_folder = True # bool | 

try:
    api_response = api_instance.modeler_users_deleteuser_post(entity_id, user_id, is_folder)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_users_deleteuser_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entity_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **is_folder** | [**bool**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modeler_users_get**
> list[User] modeler_users_get(id, is_folder)



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
api_instance = oneplan_sdk.client.swagger_client.ModelerApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
is_folder = True # bool | 

try:
    api_response = api_instance.modeler_users_get(id, is_folder)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ModelerApi->modeler_users_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **is_folder** | [**bool**](.md)|  | 

### Return type

[**list[User]**](User.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

