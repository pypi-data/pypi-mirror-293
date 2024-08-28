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

class TestrunresultListTestRunsResponse(object):
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
        'test_runs': 'list[TestrunresultTestRunDetail]',
        'next_page_token': 'str',
        'has_more': 'bool'
    }

    attribute_map = {
        'test_runs': 'testRuns',
        'next_page_token': 'nextPageToken',
        'has_more': 'hasMore'
    }

    def __init__(self, test_runs=None, next_page_token=None, has_more=None):  # noqa: E501
        """TestrunresultListTestRunsResponse - a model defined in Swagger"""  # noqa: E501
        self._test_runs = None
        self._next_page_token = None
        self._has_more = None
        self.discriminator = None
        if test_runs is not None:
            self.test_runs = test_runs
        if next_page_token is not None:
            self.next_page_token = next_page_token
        if has_more is not None:
            self.has_more = has_more

    @property
    def test_runs(self):
        """Gets the test_runs of this TestrunresultListTestRunsResponse.  # noqa: E501

        The details of the test runs.  # noqa: E501

        :return: The test_runs of this TestrunresultListTestRunsResponse.  # noqa: E501
        :rtype: list[TestrunresultTestRunDetail]
        """
        return self._test_runs

    @test_runs.setter
    def test_runs(self, test_runs):
        """Sets the test_runs of this TestrunresultListTestRunsResponse.

        The details of the test runs.  # noqa: E501

        :param test_runs: The test_runs of this TestrunresultListTestRunsResponse.  # noqa: E501
        :type: list[TestrunresultTestRunDetail]
        """

        self._test_runs = test_runs

    @property
    def next_page_token(self):
        """Gets the next_page_token of this TestrunresultListTestRunsResponse.  # noqa: E501

        A token representing the next page from the list returned by a ListTestRuns query.  # noqa: E501

        :return: The next_page_token of this TestrunresultListTestRunsResponse.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """Sets the next_page_token of this TestrunresultListTestRunsResponse.

        A token representing the next page from the list returned by a ListTestRuns query.  # noqa: E501

        :param next_page_token: The next_page_token of this TestrunresultListTestRunsResponse.  # noqa: E501
        :type: str
        """

        self._next_page_token = next_page_token

    @property
    def has_more(self):
        """Gets the has_more of this TestrunresultListTestRunsResponse.  # noqa: E501

        A Boolean that specifies whether there are more test runs to return.  # noqa: E501

        :return: The has_more of this TestrunresultListTestRunsResponse.  # noqa: E501
        :rtype: bool
        """
        return self._has_more

    @has_more.setter
    def has_more(self, has_more):
        """Sets the has_more of this TestrunresultListTestRunsResponse.

        A Boolean that specifies whether there are more test runs to return.  # noqa: E501

        :param has_more: The has_more of this TestrunresultListTestRunsResponse.  # noqa: E501
        :type: bool
        """

        self._has_more = has_more

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
        if issubclass(TestrunresultListTestRunsResponse, dict):
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
        if not isinstance(other, TestrunresultListTestRunsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
