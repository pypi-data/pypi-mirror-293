# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` for all the firewall methods and `rime-api-key` for all other methods.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from rime_sdk.swagger.swagger_client.api_client import ApiClient


class DetectionApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def list_detection_events(self, project_id_uuid, **kwargs):  # noqa: E501
        """ListDetectionEvents  # noqa: E501

        List out events for a given project. Detection events represent problems Robust Intelligence detects in different risk categories, such as performance degradation or security risk. This is a paginated method.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_detection_events(project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id_uuid: Unique object ID. (required)
        :param str first_page_req_event_object_id: Optional: return a series of detection events for a single object.
        :param datetime first_page_req_event_time_range_start_time:
        :param datetime first_page_req_event_time_range_end_time:
        :param str first_page_req_severity: Optional: When unspecified, returns all.   - SEVERITY_UNSPECIFIED: Indicates that no test runs for the specified metric.  - SEVERITY_PASS: Indicates that the specified metric is lower than the low threshold in the case where the Monitor is configured to trigger on an increase of a metric.  - SEVERITY_WARNING: Indicates that the specified metric is higher than the low threshold but still lower than the high threshold, in the case that a Monitor is configured to trigger on an increase of a metric. Warning and Alert severity levels will trigger a Degradation event.  - SEVERITY_ALERT: Indicates that the specified metric is higher than the high threshold in the case that the Monitor is configured to trigger on an increase of a metric. Warning and Alert severity level will trigger a Degradation event.
        :param list[str] first_page_req_event_types: Optional: When the list is empty, returns all.
        :param list[str] first_page_req_risk_category_types: Optional: When the list is empty, returns all.
        :param list[str] first_page_req_test_categories: Optional: When the list is empty, return all.
        :param str first_page_req_sort_sort_order:
        :param str first_page_req_sort_sort_by:
        :param bool first_page_req_include_resolved:
        :param str page_token: Specifies a page of the list returned by a ListDetectionEvents query. The ListDetectionEvents query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field.
        :param str page_size: The maximum number of Detection Event objects to return in a single page.
        :return: RimeListDetectionEventsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.list_detection_events_with_http_info(project_id_uuid, **kwargs)  # noqa: E501
        else:
            (data) = self.list_detection_events_with_http_info(project_id_uuid, **kwargs)  # noqa: E501
            return data

    def list_detection_events_with_http_info(self, project_id_uuid, **kwargs):  # noqa: E501
        """ListDetectionEvents  # noqa: E501

        List out events for a given project. Detection events represent problems Robust Intelligence detects in different risk categories, such as performance degradation or security risk. This is a paginated method.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_detection_events_with_http_info(project_id_uuid, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str project_id_uuid: Unique object ID. (required)
        :param str first_page_req_event_object_id: Optional: return a series of detection events for a single object.
        :param datetime first_page_req_event_time_range_start_time:
        :param datetime first_page_req_event_time_range_end_time:
        :param str first_page_req_severity: Optional: When unspecified, returns all.   - SEVERITY_UNSPECIFIED: Indicates that no test runs for the specified metric.  - SEVERITY_PASS: Indicates that the specified metric is lower than the low threshold in the case where the Monitor is configured to trigger on an increase of a metric.  - SEVERITY_WARNING: Indicates that the specified metric is higher than the low threshold but still lower than the high threshold, in the case that a Monitor is configured to trigger on an increase of a metric. Warning and Alert severity levels will trigger a Degradation event.  - SEVERITY_ALERT: Indicates that the specified metric is higher than the high threshold in the case that the Monitor is configured to trigger on an increase of a metric. Warning and Alert severity level will trigger a Degradation event.
        :param list[str] first_page_req_event_types: Optional: When the list is empty, returns all.
        :param list[str] first_page_req_risk_category_types: Optional: When the list is empty, returns all.
        :param list[str] first_page_req_test_categories: Optional: When the list is empty, return all.
        :param str first_page_req_sort_sort_order:
        :param str first_page_req_sort_sort_by:
        :param bool first_page_req_include_resolved:
        :param str page_token: Specifies a page of the list returned by a ListDetectionEvents query. The ListDetectionEvents query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageReq field.
        :param str page_size: The maximum number of Detection Event objects to return in a single page.
        :return: RimeListDetectionEventsResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['project_id_uuid', 'first_page_req_event_object_id', 'first_page_req_event_time_range_start_time', 'first_page_req_event_time_range_end_time', 'first_page_req_severity', 'first_page_req_event_types', 'first_page_req_risk_category_types', 'first_page_req_test_categories', 'first_page_req_sort_sort_order', 'first_page_req_sort_sort_by', 'first_page_req_include_resolved', 'page_token', 'page_size']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_detection_events" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'project_id_uuid' is set
        if ('project_id_uuid' not in params or
                params['project_id_uuid'] is None):
            raise ValueError("Missing the required parameter `project_id_uuid` when calling `list_detection_events`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'project_id_uuid' in params:
            path_params['projectId.uuid'] = params['project_id_uuid']  # noqa: E501

        query_params = []
        if 'first_page_req_event_object_id' in params:
            query_params.append(('firstPageReq.eventObjectId', params['first_page_req_event_object_id']))  # noqa: E501
        if 'first_page_req_event_time_range_start_time' in params:
            query_params.append(('firstPageReq.eventTimeRange.startTime', params['first_page_req_event_time_range_start_time']))  # noqa: E501
        if 'first_page_req_event_time_range_end_time' in params:
            query_params.append(('firstPageReq.eventTimeRange.endTime', params['first_page_req_event_time_range_end_time']))  # noqa: E501
        if 'first_page_req_severity' in params:
            query_params.append(('firstPageReq.severity', params['first_page_req_severity']))  # noqa: E501
        if 'first_page_req_event_types' in params:
            query_params.append(('firstPageReq.eventTypes', params['first_page_req_event_types']))  # noqa: E501
            collection_formats['firstPageReq.eventTypes'] = 'multi'  # noqa: E501
        if 'first_page_req_risk_category_types' in params:
            query_params.append(('firstPageReq.riskCategoryTypes', params['first_page_req_risk_category_types']))  # noqa: E501
            collection_formats['firstPageReq.riskCategoryTypes'] = 'multi'  # noqa: E501
        if 'first_page_req_test_categories' in params:
            query_params.append(('firstPageReq.testCategories', params['first_page_req_test_categories']))  # noqa: E501
            collection_formats['firstPageReq.testCategories'] = 'multi'  # noqa: E501
        if 'first_page_req_sort_sort_order' in params:
            query_params.append(('firstPageReq.sort.sortOrder', params['first_page_req_sort_sort_order']))  # noqa: E501
        if 'first_page_req_sort_sort_by' in params:
            query_params.append(('firstPageReq.sort.sortBy', params['first_page_req_sort_sort_by']))  # noqa: E501
        if 'first_page_req_include_resolved' in params:
            query_params.append(('firstPageReq.includeResolved', params['first_page_req_include_resolved']))  # noqa: E501
        if 'page_token' in params:
            query_params.append(('pageToken', params['page_token']))  # noqa: E501
        if 'page_size' in params:
            query_params.append(('pageSize', params['page_size']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['X-Firewall-Auth-Token', 'rime-api-key']  # noqa: E501

        return self.api_client.call_api(
            '/v1-beta/detection-events/{projectId.uuid}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='RimeListDetectionEventsResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
