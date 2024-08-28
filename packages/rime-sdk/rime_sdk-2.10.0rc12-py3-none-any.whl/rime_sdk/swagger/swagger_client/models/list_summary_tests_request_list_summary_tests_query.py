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

class ListSummaryTestsRequestListSummaryTestsQuery(object):
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
        'test_run_id': 'str'
    }

    attribute_map = {
        'test_run_id': 'testRunId'
    }

    def __init__(self, test_run_id=None):  # noqa: E501
        """ListSummaryTestsRequestListSummaryTestsQuery - a model defined in Swagger"""  # noqa: E501
        self._test_run_id = None
        self.discriminator = None
        if test_run_id is not None:
            self.test_run_id = test_run_id

    @property
    def test_run_id(self):
        """Gets the test_run_id of this ListSummaryTestsRequestListSummaryTestsQuery.  # noqa: E501

        The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field.  # noqa: E501

        :return: The test_run_id of this ListSummaryTestsRequestListSummaryTestsQuery.  # noqa: E501
        :rtype: str
        """
        return self._test_run_id

    @test_run_id.setter
    def test_run_id(self, test_run_id):
        """Sets the test_run_id of this ListSummaryTestsRequestListSummaryTestsQuery.

        The ID of the test run associated with summary tests. Specify exactly one of the page_token field or this field.  # noqa: E501

        :param test_run_id: The test_run_id of this ListSummaryTestsRequestListSummaryTestsQuery.  # noqa: E501
        :type: str
        """

        self._test_run_id = test_run_id

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
        if issubclass(ListSummaryTestsRequestListSummaryTestsQuery, dict):
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
        if not isinstance(other, ListSummaryTestsRequestListSummaryTestsQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
