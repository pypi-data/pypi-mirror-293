# oneplan_sdk.client.swagger_client.NotificationsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**notifications_get**](NotificationsApi.md#notifications_get) | **GET** /notifications | 
[**notifications_id_read_post**](NotificationsApi.md#notifications_id_read_post) | **POST** /notifications/{id}/read | 
[**notifications_new_get**](NotificationsApi.md#notifications_new_get) | **GET** /notifications/new | 
[**notifications_read_post**](NotificationsApi.md#notifications_read_post) | **POST** /notifications/read | 
[**notifications_sid_read_post**](NotificationsApi.md#notifications_sid_read_post) | **POST** /notifications/s/{id}/read | 
[**notifications_surveys_get**](NotificationsApi.md#notifications_surveys_get) | **GET** /notifications/surveys | 

# **notifications_get**
> list[Notification] notifications_get()



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.notifications_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Notification]**](Notification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_id_read_post**
> Notification notifications_id_read_post(id)



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.notifications_id_read_post(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_id_read_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**Notification**](Notification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_new_get**
> list[Notification] notifications_new_get()



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.notifications_new_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_new_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[Notification]**](Notification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **notifications_read_post**
> HttpResponseMessage notifications_read_post()



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.notifications_read_post()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_read_post: %s\n" % e)
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

# **notifications_sid_read_post**
> HttpResponseMessage notifications_sid_read_post(id)



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.notifications_sid_read_post(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_sid_read_post: %s\n" % e)
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

# **notifications_surveys_get**
> list[SystemNotification] notifications_surveys_get()



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
api_instance = oneplan_sdk.client.swagger_client.NotificationsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.notifications_surveys_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NotificationsApi->notifications_surveys_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[SystemNotification]**](SystemNotification.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

