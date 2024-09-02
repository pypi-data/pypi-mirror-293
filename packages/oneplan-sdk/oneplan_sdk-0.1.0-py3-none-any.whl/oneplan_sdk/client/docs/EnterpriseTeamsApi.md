# oneplan_sdk.client.swagger_client.EnterpriseTeamsApi

All URIs are relative to *https://eu.oneplan.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**enterpriseteams_get**](EnterpriseTeamsApi.md#enterpriseteams_get) | **GET** /enterpriseteams | 
[**enterpriseteams_id_delete**](EnterpriseTeamsApi.md#enterpriseteams_id_delete) | **DELETE** /enterpriseteams/{id} | 
[**enterpriseteams_id_deletemembers_delete**](EnterpriseTeamsApi.md#enterpriseteams_id_deletemembers_delete) | **DELETE** /enterpriseteams/{id}/deletemembers | 
[**enterpriseteams_id_get**](EnterpriseTeamsApi.md#enterpriseteams_id_get) | **GET** /enterpriseteams/{id} | 
[**enterpriseteams_id_members_get**](EnterpriseTeamsApi.md#enterpriseteams_id_members_get) | **GET** /enterpriseteams/{id}/members | 
[**enterpriseteams_id_post**](EnterpriseTeamsApi.md#enterpriseteams_id_post) | **POST** /enterpriseteams/{id} | 
[**enterpriseteams_id_updatemembers_post**](EnterpriseTeamsApi.md#enterpriseteams_id_updatemembers_post) | **POST** /enterpriseteams/{id}/updatemembers | 
[**enterpriseteams_list_my_get**](EnterpriseTeamsApi.md#enterpriseteams_list_my_get) | **GET** /enterpriseteams/list/my | 
[**enterpriseteams_post**](EnterpriseTeamsApi.md#enterpriseteams_post) | **POST** /enterpriseteams | 
[**enterpriseteams_team_id_allocations_post**](EnterpriseTeamsApi.md#enterpriseteams_team_id_allocations_post) | **POST** /enterpriseteams/{TeamId}/allocations | 
[**enterpriseteams_team_id_allocations_resource_id_delete**](EnterpriseTeamsApi.md#enterpriseteams_team_id_allocations_resource_id_delete) | **DELETE** /enterpriseteams/{TeamId}/allocations/{ResourceId} | 
[**enterpriseteams_team_id_updateallocation_post**](EnterpriseTeamsApi.md#enterpriseteams_team_id_updateallocation_post) | **POST** /enterpriseteams/{TeamId}/updateallocation | 

# **enterpriseteams_get**
> list[OnePlanTeam] enterpriseteams_get()



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.enterpriseteams_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OnePlanTeam]**](OnePlanTeam.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_id_delete**
> HttpResponseMessage enterpriseteams_id_delete(id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_id_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_delete: %s\n" % e)
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

# **enterpriseteams_id_deletemembers_delete**
> HttpResponseMessage enterpriseteams_id_deletemembers_delete(id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_id_deletemembers_delete(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_deletemembers_delete: %s\n" % e)
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

# **enterpriseteams_id_get**
> OnePlanTeam enterpriseteams_id_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_id_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**OnePlanTeam**](OnePlanTeam.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_id_members_get**
> list[Resource] enterpriseteams_id_members_get(id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_id_members_get(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_members_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**list[Resource]**](Resource.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_id_post**
> HttpResponseMessage enterpriseteams_id_post(body, id, mod_members=mod_members)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanTeamRequest() # OnePlanTeamRequest | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
mod_members = True # bool |  (optional)

try:
    api_response = api_instance.enterpriseteams_id_post(body, id, mod_members=mod_members)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanTeamRequest**](OnePlanTeamRequest.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **mod_members** | [**bool**](.md)|  | [optional] 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_id_updatemembers_post**
> HttpResponseMessage enterpriseteams_id_updatemembers_post(body, id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TeamMember() # TeamMember | 
id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_id_updatemembers_post(body, id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_id_updatemembers_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamMember**](TeamMember.md)|  | 
 **id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_list_my_get**
> list[OnePlanTeam] enterpriseteams_list_my_get()



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))

try:
    api_response = api_instance.enterpriseteams_list_my_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_list_my_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OnePlanTeam]**](OnePlanTeam.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_post**
> HttpResponseMessage enterpriseteams_post(body)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.OnePlanTeam() # OnePlanTeam | 

try:
    api_response = api_instance.enterpriseteams_post(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OnePlanTeam**](OnePlanTeam.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_team_id_allocations_post**
> list[dict(str, Object)] enterpriseteams_team_id_allocations_post(body, team_id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TeamAllocationsRequest() # TeamAllocationsRequest | 
team_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_team_id_allocations_post(body, team_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_team_id_allocations_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamAllocationsRequest**](TeamAllocationsRequest.md)|  | 
 **team_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

**list[dict(str, Object)]**

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_team_id_allocations_resource_id_delete**
> HttpResponseMessage enterpriseteams_team_id_allocations_resource_id_delete(team_id, resource_id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
team_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 
resource_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_team_id_allocations_resource_id_delete(team_id, resource_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_team_id_allocations_resource_id_delete: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **team_id** | [**GloballyUniqueIdentifier**](.md)|  | 
 **resource_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**HttpResponseMessage**](HttpResponseMessage.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enterpriseteams_team_id_updateallocation_post**
> dict(str, DecimalNumber) enterpriseteams_team_id_updateallocation_post(body, team_id)



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
api_instance = oneplan_sdk.client.swagger_client.EnterpriseTeamsApi(oneplan_sdk.client.swagger_client.ApiClient(configuration))
body = oneplan_sdk.client.swagger_client.TeamAllocationRequest() # TeamAllocationRequest | 
team_id = oneplan_sdk.client.swagger_client.GloballyUniqueIdentifier() # GloballyUniqueIdentifier | 

try:
    api_response = api_instance.enterpriseteams_team_id_updateallocation_post(body, team_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EnterpriseTeamsApi->enterpriseteams_team_id_updateallocation_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TeamAllocationRequest**](TeamAllocationRequest.md)|  | 
 **team_id** | [**GloballyUniqueIdentifier**](.md)|  | 

### Return type

[**dict(str, DecimalNumber)**](DecimalNumber.md)

### Authorization

[oneplan_api_auth](../README.md#oneplan_api_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

