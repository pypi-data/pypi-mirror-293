# oneplan_sdk.client.swagger_client.InsightsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**insights_all_get**](InsightsApi.md#insights_all_get) | **GET** /insights/all | 
[**insights_allplans_get**](InsightsApi.md#insights_allplans_get) | **GET** /insights/allplans | 
[**insights_comments_get**](InsightsApi.md#insights_comments_get) | **GET** /insights/comments | 
[**insights_favorite_get**](InsightsApi.md#insights_favorite_get) | **GET** /insights/favorite | 
[**insights_myplans_get**](InsightsApi.md#insights_myplans_get) | **GET** /insights/myplans | 
[**insights_recent_get**](InsightsApi.md#insights_recent_get) | **GET** /insights/recent | 
[**insights_sharedplans_get**](InsightsApi.md#insights_sharedplans_get) | **GET** /insights/sharedplans | 
[**insights_work_get**](InsightsApi.md#insights_work_get) | **GET** /insights/work | 

# **insights_all_get**
> list[InsightResult] insights_all_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_all_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_all_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[InsightResult]**](InsightResult.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_allplans_get**
> list[RecentPlan] insights_allplans_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_allplans_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_allplans_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RecentPlan]**](RecentPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_comments_get**
> list[InsightComment] insights_comments_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_comments_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_comments_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[InsightComment]**](InsightComment.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_favorite_get**
> list[RecentPlan] insights_favorite_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_favorite_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_favorite_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RecentPlan]**](RecentPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_myplans_get**
> list[RecentPlan] insights_myplans_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_myplans_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_myplans_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RecentPlan]**](RecentPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_recent_get**
> list[RecentPlan] insights_recent_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_recent_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_recent_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RecentPlan]**](RecentPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_sharedplans_get**
> list[RecentPlan] insights_sharedplans_get()



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.insights_sharedplans_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_sharedplans_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RecentPlan]**](RecentPlan.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **insights_work_get**
> list[WorkPlanTask] insights_work_get(due)



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
api_instance = oneplan_sdk.client.swagger_client.InsightsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
due = 56 # int | 

try:
    api_response = api_instance.insights_work_get(due)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InsightsApi->insights_work_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **due** | [**int**](.md)|  | 

### Return type

[**list[WorkPlanTask]**](WorkPlanTask.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

