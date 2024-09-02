# oneplan_sdk.client.swagger_client.PlanNotificationsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**notifications_plan_config_check_get**](PlanNotificationsApi.md#notifications_plan_config_check_get) | **GET** /notifications/plan/config/check | 
[**notifications_plan_config_time_hour_post**](PlanNotificationsApi.md#notifications_plan_config_time_hour_post) | **POST** /notifications/plan/config/time/{hour} | 
[**notifications_plan_create_post**](PlanNotificationsApi.md#notifications_plan_create_post) | **POST** /notifications/plan/create | 
[**notifications_plan_id_delete_delete**](PlanNotificationsApi.md#notifications_plan_id_delete_delete) | **DELETE** /notifications/plan/{id}/delete | 
[**notifications_plan_notification_id_update_post**](PlanNotificationsApi.md#notifications_plan_notification_id_update_post) | **POST** /notifications/plan/{notificationId}/update | 
[**notifications_plan_plan_id_list_post**](PlanNotificationsApi.md#notifications_plan_plan_id_list_post) | **POST** /notifications/plan/{planId}/list | 

# **notifications_plan_config_check_get**
> bool notifications_plan_config_check_get()



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.notifications_plan_config_check_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_config_check_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**bool**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_plan_config_time_hour_post**
> CoreSchedule notifications_plan_config_time_hour_post(hour)



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
hour = 56 # int | 

try:
    api_response = api_instance.notifications_plan_config_time_hour_post(hour)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_config_time_hour_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hour** | [**int**](.md)|  | 

### Return type

[**CoreSchedule**](CoreSchedule.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_plan_create_post**
> PlanNotification notifications_plan_create_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlanNotification() # PlanNotification | 

try:
    api_response = api_instance.notifications_plan_create_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_create_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlanNotification**](PlanNotification.md)|  | 

### Return type

[**PlanNotification**](PlanNotification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_plan_id_delete_delete**
> HttpResponseMessage notifications_plan_id_delete_delete(id)



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.notifications_plan_id_delete_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_id_delete_delete: %s\n" % e)
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

# **notifications_plan_notification_id_update_post**
> PlanNotification notifications_plan_notification_id_update_post(body, notification_id)



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.PlanNotification() # PlanNotification | 
notification_id = 'notification_id_example' # str | 

try:
    api_response = api_instance.notifications_plan_notification_id_update_post(body, notification_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_notification_id_update_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PlanNotification**](PlanNotification.md)|  | 
 **notification_id** | [**str**](.md)|  | 

### Return type

[**PlanNotification**](PlanNotification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_plan_plan_id_list_post**
> list[PlanNotification] notifications_plan_plan_id_list_post(plan_id)



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
api_instance = oneplan_sdk.client.swagger_client.PlanNotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
plan_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.notifications_plan_plan_id_list_post(plan_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PlanNotificationsApi->notifications_plan_plan_id_list_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **plan_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[PlanNotification]**](PlanNotification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

