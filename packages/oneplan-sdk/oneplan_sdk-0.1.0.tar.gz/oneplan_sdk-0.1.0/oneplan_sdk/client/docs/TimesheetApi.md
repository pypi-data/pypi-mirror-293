# oneplan_sdk.client.swagger_client.TimesheetApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**timesheet_id_lines_line_id_delete**](TimesheetApi.md#timesheet_id_lines_line_id_delete) | **DELETE** /timesheet/{Id}/lines/{LineId} | 
[**timesheet_id_lines_put**](TimesheetApi.md#timesheet_id_lines_put) | **PUT** /timesheet/{Id}/lines | 
[**timesheet_id_recall_post**](TimesheetApi.md#timesheet_id_recall_post) | **POST** /timesheet/{Id}/recall | 
[**timesheet_id_submit_post**](TimesheetApi.md#timesheet_id_submit_post) | **POST** /timesheet/{Id}/submit | 
[**timesheet_id_workflow_line_id_get**](TimesheetApi.md#timesheet_id_workflow_line_id_get) | **GET** /timesheet/{Id}/workflow/{lineId} | 
[**timesheet_lines_get**](TimesheetApi.md#timesheet_lines_get) | **GET** /timesheet/lines | 
[**ts_fields_get**](TimesheetApi.md#ts_fields_get) | **GET** /ts/fields | 
[**ts_periods_get**](TimesheetApi.md#ts_periods_get) | **GET** /ts/periods | 
[**ts_search_get**](TimesheetApi.md#ts_search_get) | **GET** /ts/search | 
[**ts_stopwatch_start_post**](TimesheetApi.md#ts_stopwatch_start_post) | **POST** /ts/stopwatch/start | 
[**ts_stopwatch_stop_post**](TimesheetApi.md#ts_stopwatch_stop_post) | **POST** /ts/stopwatch/stop | 
[**ts_stopwatch_validate_post**](TimesheetApi.md#ts_stopwatch_validate_post) | **POST** /ts/stopwatch/validate | 
[**ts_timesheet_get**](TimesheetApi.md#ts_timesheet_get) | **GET** /ts/timesheet | 
[**ts_timesheet_lines_get**](TimesheetApi.md#ts_timesheet_lines_get) | **GET** /ts/timesheet/lines | 
[**ts_timesheet_lines_post**](TimesheetApi.md#ts_timesheet_lines_post) | **POST** /ts/timesheet/lines | 

# **timesheet_id_lines_line_id_delete**
> HttpResponseMessage timesheet_id_lines_line_id_delete(id, line_id, user_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.timesheet_id_lines_line_id_delete(id, line_id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_id_lines_line_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **timesheet_id_lines_put**
> HttpResponseMessage timesheet_id_lines_put(id, user_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.timesheet_id_lines_put(id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_id_lines_put: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **timesheet_id_recall_post**
> HttpResponseMessage timesheet_id_recall_post(id, user_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.timesheet_id_recall_post(id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_id_recall_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **timesheet_id_submit_post**
> HttpResponseMessage timesheet_id_submit_post(id, user_id, all_rows=all_rows)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
all_rows = True # bool |  (optional)

try:
    api_response = api_instance.timesheet_id_submit_post(id, user_id, all_rows=all_rows)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_id_submit_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **all_rows** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **timesheet_id_workflow_line_id_get**
> HttpResponseMessage timesheet_id_workflow_line_id_get(id, line_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.timesheet_id_workflow_line_id_get(id, line_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_id_workflow_line_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **line_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **timesheet_lines_get**
> TimesheetInfo timesheet_lines_get(period_id, user_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
period_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.timesheet_lines_get(period_id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->timesheet_lines_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**TimesheetInfo**](TimesheetInfo.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_fields_get**
> DataTable ts_fields_get()



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.ts_fields_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_fields_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**DataTable**](DataTable.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_periods_get**
> DataTable ts_periods_get(closed=closed)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
closed = True # bool |  (optional)

try:
    api_response = api_instance.ts_periods_get(closed=closed)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_periods_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **closed** | [**bool**](.md)|  | [optional] 

### Return type

[**DataTable**](DataTable.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_search_get**
> list[Object] ts_search_get(search_string, user_id, assigned_to_me=assigned_to_me)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
search_string = 'search_string_example' # str | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
assigned_to_me = True # bool |  (optional)

try:
    api_response = api_instance.ts_search_get(search_string, user_id, assigned_to_me=assigned_to_me)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_search_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_string** | [**str**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **assigned_to_me** | [**bool**](.md)|  | [optional] 

### Return type

[**list[Object]**](Object.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_stopwatch_start_post**
> list[Stopwatch] ts_stopwatch_start_post(body, user_id, offset)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.Stopwatch() # Stopwatch | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
offset = 56 # int | 

try:
    api_response = api_instance.ts_stopwatch_start_post(body, user_id, offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_stopwatch_start_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Stopwatch**](Stopwatch.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **offset** | [**int**](.md)|  | 

### Return type

[**list[Stopwatch]**](Stopwatch.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_stopwatch_stop_post**
> Stopwatch ts_stopwatch_stop_post(timesheet_line_id, current_time, user_id, offset)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
timesheet_line_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
current_time = '2013-10-20' # date | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
offset = 56 # int | 

try:
    api_response = api_instance.ts_stopwatch_stop_post(timesheet_line_id, current_time, user_id, offset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_stopwatch_stop_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **timesheet_line_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **current_time** | [**date**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **offset** | [**int**](.md)|  | 

### Return type

[**Stopwatch**](Stopwatch.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_stopwatch_validate_post**
> Stopwatch ts_stopwatch_validate_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.Stopwatch() # Stopwatch | 

try:
    api_response = api_instance.ts_stopwatch_validate_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_stopwatch_validate_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Stopwatch**](Stopwatch.md)|  | 

### Return type

[**Stopwatch**](Stopwatch.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_timesheet_get**
> object ts_timesheet_get(period_id, user_id)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
period_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.ts_timesheet_get(period_id, user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_timesheet_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

**object**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_timesheet_lines_get**
> HttpResponseMessage ts_timesheet_lines_get(period_id, user_id, my_approvals=my_approvals)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
period_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
user_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
my_approvals = True # bool |  (optional)

try:
    api_response = api_instance.ts_timesheet_lines_get(period_id, user_id, my_approvals=my_approvals)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_timesheet_lines_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **period_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **user_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **my_approvals** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ts_timesheet_lines_post**
> HttpResponseMessage ts_timesheet_lines_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.TimesheetApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.SaveLineObject() # SaveLineObject | 

try:
    api_response = api_instance.ts_timesheet_lines_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TimesheetApi->ts_timesheet_lines_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**SaveLineObject**](SaveLineObject.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

