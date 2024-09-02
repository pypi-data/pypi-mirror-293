# oneplan_sdk.client.swagger_client.ResPlanApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**modeler_resplan_capacitychart_post**](ResPlanApi.md#modeler_resplan_capacitychart_post) | **POST** /modeler/resplan/capacitychart | 
[**resplan_capacitychart_post**](ResPlanApi.md#resplan_capacitychart_post) | **POST** /resplan/capacitychart | 
[**resplan_externalimport_post**](ResPlanApi.md#resplan_externalimport_post) | **POST** /resplan/externalimport | 
[**resplan_id_addresource_post**](ResPlanApi.md#resplan_id_addresource_post) | **POST** /resplan/{id}/addresource | 
[**resplan_id_allocate_post**](ResPlanApi.md#resplan_id_allocate_post) | **POST** /resplan/{id}/allocate | 
[**resplan_id_capacity_get**](ResPlanApi.md#resplan_id_capacity_get) | **GET** /resplan/{id}/capacity | 
[**resplan_id_copy_post**](ResPlanApi.md#resplan_id_copy_post) | **POST** /resplan/{id}/copy | 
[**resplan_id_lineid_delete**](ResPlanApi.md#resplan_id_lineid_delete) | **DELETE** /resplan/{id}/{lineid} | 
[**resplan_id_post**](ResPlanApi.md#resplan_id_post) | **POST** /resplan/{id} | 
[**resplan_id_replaceresource_post**](ResPlanApi.md#resplan_id_replaceresource_post) | **POST** /resplan/{id}/replaceresource | 
[**resplan_line_id_comment_get**](ResPlanApi.md#resplan_line_id_comment_get) | **GET** /resplan/{LineId}/comment | 
[**resplan_line_id_comment_id_delete**](ResPlanApi.md#resplan_line_id_comment_id_delete) | **DELETE** /resplan/{LineId}/comment/{id} | 
[**resplan_line_id_comment_post**](ResPlanApi.md#resplan_line_id_comment_post) | **POST** /resplan/{LineId}/comment | 
[**resplan_line_id_reallocate_post**](ResPlanApi.md#resplan_line_id_reallocate_post) | **POST** /resplan/{LineId}/reallocate | 

# **modeler_resplan_capacitychart_post**
> list[dict(str, Object)] modeler_resplan_capacitychart_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ModelerResPlanCapacityPost() # ModelerResPlanCapacityPost | 

try:
    api_response = api_instance.modeler_resplan_capacitychart_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->modeler_resplan_capacitychart_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ModelerResPlanCapacityPost**](ModelerResPlanCapacityPost.md)|  | 

### Return type

**list[dict(str, Object)]**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_capacitychart_post**
> list[dict(str, Object)] resplan_capacitychart_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.CandidatesPost() # CandidatesPost | 

try:
    api_response = api_instance.resplan_capacitychart_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_capacitychart_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CandidatesPost**](CandidatesPost.md)|  | 

### Return type

**list[dict(str, Object)]**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_externalimport_post**
> ImportResult resplan_externalimport_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ImportResPlanObject() # ImportResPlanObject | 

try:
    api_response = api_instance.resplan_externalimport_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_externalimport_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ImportResPlanObject**](ImportResPlanObject.md)|  | 

### Return type

[**ImportResult**](ImportResult.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_addresource_post**
> list[dict(str, Object)] resplan_id_addresource_post(body, replacing, id, res_mode=res_mode)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AddResourcePost() # AddResourcePost | 
replacing = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
res_mode = True # bool |  (optional)

try:
    api_response = api_instance.resplan_id_addresource_post(body, replacing, id, res_mode=res_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_addresource_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AddResourcePost**](AddResourcePost.md)|  | 
 **replacing** | [**GloballyUniqueIdentifier**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **res_mode** | [**bool**](.md)|  | [optional] 

### Return type

**list[dict(str, Object)]**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_allocate_post**
> dict(str, dict(str, Object)) resplan_id_allocate_post(body, id, res_mode=res_mode)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.AllocationPost() # AllocationPost | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
res_mode = True # bool |  (optional)

try:
    api_response = api_instance.resplan_id_allocate_post(body, id, res_mode=res_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_allocate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**AllocationPost**](AllocationPost.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **res_mode** | [**bool**](.md)|  | [optional] 

### Return type

**dict(str, dict(str, Object))**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_capacity_get**
> list[ResourceCapacity] resplan_id_capacity_get(id, start, end, zoom)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
start = '2013-10-20' # date | 
end = '2013-10-20' # date | 
zoom = oneplan_sdk.client.swagger_client.Zoom() # Zoom | 

try:
    api_response = api_instance.resplan_id_capacity_get(id, start, end, zoom)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_capacity_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **start** | [**date**](.md)|  | 
 **end** | [**date**](.md)|  | 
 **zoom** | [**Zoom**](.md)|  | 

### Return type

[**list[ResourceCapacity]**](ResourceCapacity.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_copy_post**
> HttpResponseMessage resplan_id_copy_post(body, id)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ResourcePlanCopy() # ResourcePlanCopy | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.resplan_id_copy_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_copy_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResourcePlanCopy**](ResourcePlanCopy.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_lineid_delete**
> HttpResponseMessage resplan_id_lineid_delete(id, lineid)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
lineid = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.resplan_id_lineid_delete(id, lineid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_lineid_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **lineid** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_post**
> dict(str, dict(str, Object)) resplan_id_post(body, id, res_mode=res_mode)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ResUpdate() # ResUpdate | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
res_mode = True # bool |  (optional)

try:
    api_response = api_instance.resplan_id_post(body, id, res_mode=res_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ResUpdate**](ResUpdate.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **res_mode** | [**bool**](.md)|  | [optional] 

### Return type

**dict(str, dict(str, Object))**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_id_replaceresource_post**
> object resplan_id_replaceresource_post(body, id, res_mode=res_mode)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.ReplaceResourcePost() # ReplaceResourcePost | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
res_mode = True # bool |  (optional)

try:
    api_response = api_instance.resplan_id_replaceresource_post(body, id, res_mode=res_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_id_replaceresource_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ReplaceResourcePost**](ReplaceResourcePost.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **res_mode** | [**bool**](.md)|  | [optional] 

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_line_id_comment_get**
> CommentsResponse resplan_line_id_comment_get(line_id)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.resplan_line_id_comment_get(line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_line_id_comment_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**CommentsResponse**](CommentsResponse.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_line_id_comment_id_delete**
> HttpResponseMessage resplan_line_id_comment_id_delete(line_id, id)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.resplan_line_id_comment_id_delete(line_id, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_line_id_comment_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_line_id_comment_post**
> TaskComment resplan_line_id_comment_post(body, line_id)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.CommentPost() # CommentPost | 
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.resplan_line_id_comment_post(body, line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_line_id_comment_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CommentPost**](CommentPost.md)|  | 
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**TaskComment**](TaskComment.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resplan_line_id_reallocate_post**
> dict(str, dict(str, Object)) resplan_line_id_reallocate_post(line_id, res_mode=res_mode)



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
api_instance = oneplan_sdk.client.swagger_client.ResPlanApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
res_mode = True # bool |  (optional)

try:
    api_response = api_instance.resplan_line_id_reallocate_post(line_id, res_mode=res_mode)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ResPlanApi->resplan_line_id_reallocate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **res_mode** | [**bool**](.md)|  | [optional] 

### Return type

**dict(str, dict(str, Object))**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

