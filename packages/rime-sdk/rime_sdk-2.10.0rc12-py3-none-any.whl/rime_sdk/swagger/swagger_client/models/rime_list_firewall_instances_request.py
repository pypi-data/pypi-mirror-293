# coding: utf-8

"""
    Robust Intelligence REST API

    API methods for Robust Intelligence. Users must authenticate using the `X-Firewall-Auth-Token` for all the firewall methods and `rime-api-key` for all other methods.  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: dev@robustintelligence.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class RimeListFirewallInstancesRequest(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'page_size': 'str',
        'page_token': 'str',
        'first_page_query': 'ListFirewallInstancesRequestListFirewallInstancesQuery'
    }

    attribute_map = {
        'page_size': 'pageSize',
        'page_token': 'pageToken',
        'first_page_query': 'firstPageQuery'
    }

    def __init__(self, page_size=None, page_token=None, first_page_query=None):  # noqa: E501
        """RimeListFirewallInstancesRequest - a model defined in Swagger"""  # noqa: E501
        self._page_size = None
        self._page_token = None
        self._first_page_query = None
        self.discriminator = None
        if page_size is not None:
            self.page_size = page_size
        if page_token is not None:
            self.page_token = page_token
        if first_page_query is not None:
            self.first_page_query = first_page_query

    @property
    def page_size(self):
        """Gets the page_size of this RimeListFirewallInstancesRequest.  # noqa: E501


        :return: The page_size of this RimeListFirewallInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """Sets the page_size of this RimeListFirewallInstancesRequest.


        :param page_size: The page_size of this RimeListFirewallInstancesRequest.  # noqa: E501
        :type: str
        """

        self._page_size = page_size

    @property
    def page_token(self):
        """Gets the page_token of this RimeListFirewallInstancesRequest.  # noqa: E501

        Specifies a page of the list returned by a ListFirewallInstances query. The ListFirewallInstances query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field.  # noqa: E501

        :return: The page_token of this RimeListFirewallInstancesRequest.  # noqa: E501
        :rtype: str
        """
        return self._page_token

    @page_token.setter
    def page_token(self, page_token):
        """Sets the page_token of this RimeListFirewallInstancesRequest.

        Specifies a page of the list returned by a ListFirewallInstances query. The ListFirewallInstances query returns a pageToken when there is more than one page of results. Specify either this field or the firstPageQuery field.  # noqa: E501

        :param page_token: The page_token of this RimeListFirewallInstancesRequest.  # noqa: E501
        :type: str
        """

        self._page_token = page_token

    @property
    def first_page_query(self):
        """Gets the first_page_query of this RimeListFirewallInstancesRequest.  # noqa: E501


        :return: The first_page_query of this RimeListFirewallInstancesRequest.  # noqa: E501
        :rtype: ListFirewallInstancesRequestListFirewallInstancesQuery
        """
        return self._first_page_query

    @first_page_query.setter
    def first_page_query(self, first_page_query):
        """Sets the first_page_query of this RimeListFirewallInstancesRequest.


        :param first_page_query: The first_page_query of this RimeListFirewallInstancesRequest.  # noqa: E501
        :type: ListFirewallInstancesRequestListFirewallInstancesQuery
        """

        self._first_page_query = first_page_query

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(RimeListFirewallInstancesRequest, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RimeListFirewallInstancesRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
