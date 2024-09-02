# oneplan_sdk.client.swagger_client.StatusReportsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**statusreports_id_approve_post**](StatusReportsApi.md#statusreports_id_approve_post) | **POST** /statusreports/{id}/approve | 
[**statusreports_id_delete**](StatusReportsApi.md#statusreports_id_delete) | **DELETE** /statusreports/{id} | 
[**statusreports_id_doc_get**](StatusReportsApi.md#statusreports_id_doc_get) | **GET** /statusreports/{id}/doc | 
[**statusreports_id_pdf_get**](StatusReportsApi.md#statusreports_id_pdf_get) | **GET** /statusreports/{id}/pdf | 
[**statusreports_id_ppt_get**](StatusReportsApi.md#statusreports_id_ppt_get) | **GET** /statusreports/{id}/ppt | 
[**statusreports_id_recall_post**](StatusReportsApi.md#statusreports_id_recall_post) | **POST** /statusreports/{id}/recall | 
[**statusreports_id_reject_post**](StatusReportsApi.md#statusreports_id_reject_post) | **POST** /statusreports/{id}/reject | 
[**statusreports_id_submit_post**](StatusReportsApi.md#statusreports_id_submit_post) | **POST** /statusreports/{id}/submit | 
[**statusreports_my_get**](StatusReportsApi.md#statusreports_my_get) | **GET** /statusreports/my | 
[**statusreports_mysubmit_get**](StatusReportsApi.md#statusreports_mysubmit_get) | **GET** /statusreports/mysubmit | 
[**statusreports_plan_id_get**](StatusReportsApi.md#statusreports_plan_id_get) | **GET** /statusreports/{PlanId} | 

# **statusreports_id_approve_post**
> StatusReport statusreports_id_approve_post(id, comments)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
comments = 'comments_example' # str | 

try:
    api_response = api_instance.statusreports_id_approve_post(id, comments)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_approve_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **comments** | [**str**](.md)|  | 

### Return type

[**StatusReport**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_id_delete**
> HttpResponseMessage statusreports_id_delete(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_delete: %s\n" % e)
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

# **statusreports_id_doc_get**
> HttpResponseMessage statusreports_id_doc_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_doc_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_doc_get: %s\n" % e)
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

# **statusreports_id_pdf_get**
> HttpResponseMessage statusreports_id_pdf_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_pdf_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_pdf_get: %s\n" % e)
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

# **statusreports_id_ppt_get**
> HttpResponseMessage statusreports_id_ppt_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_ppt_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_ppt_get: %s\n" % e)
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

# **statusreports_id_recall_post**
> StatusReport statusreports_id_recall_post(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_recall_post(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_recall_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**StatusReport**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_id_reject_post**
> StatusReport statusreports_id_reject_post(id, comments)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
comments = 'comments_example' # str | 

try:
    api_response = api_instance.statusreports_id_reject_post(id, comments)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_reject_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **comments** | [**str**](.md)|  | 

### Return type

[**StatusReport**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_id_submit_post**
> StatusReport statusreports_id_submit_post(id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_id_submit_post(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_id_submit_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**StatusReport**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_my_get**
> list[StatusReport] statusreports_my_get(states)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
states = oneplan_sdk.client.swagger_client.StatusReportState() # StatusReportState | 

try:
    api_response = api_instance.statusreports_my_get(states)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_my_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **states** | [**StatusReportState**](.md)|  | 

### Return type

[**list[StatusReport]**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_mysubmit_get**
> list[StatusReport] statusreports_mysubmit_get()



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.statusreports_mysubmit_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_mysubmit_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[StatusReport]**](StatusReport.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **statusreports_plan_id_get**
> StatusReportInfo statusreports_plan_id_get(plan_id, report_id)



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
api_instance = oneplan_sdk.client.swagger_client.StatusReportsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
report_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.statusreports_plan_id_get(plan_id, report_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusReportsApi->statusreports_plan_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **report_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**StatusReportInfo**](StatusReportInfo.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

