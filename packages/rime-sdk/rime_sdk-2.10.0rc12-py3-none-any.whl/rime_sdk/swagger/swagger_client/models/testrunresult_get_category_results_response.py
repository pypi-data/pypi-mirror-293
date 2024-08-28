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

class TestrunresultGetCategoryResultsResponse(object):
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
        'category_test_results': 'list[RimeCategoryTestResult]'
    }

    attribute_map = {
        'category_test_results': 'categoryTestResults'
    }

    def __init__(self, category_test_results=None):  # noqa: E501
        """TestrunresultGetCategoryResultsResponse - a model defined in Swagger"""  # noqa: E501
        self._category_test_results = None
        self.discriminator = None
        if category_test_results is not None:
            self.category_test_results = category_test_results

    @property
    def category_test_results(self):
        """Gets the category_test_results of this TestrunresultGetCategoryResultsResponse.  # noqa: E501

        The list of summary test results.  # noqa: E501

        :return: The category_test_results of this TestrunresultGetCategoryResultsResponse.  # noqa: E501
        :rtype: list[RimeCategoryTestResult]
        """
        return self._category_test_results

    @category_test_results.setter
    def category_test_results(self, category_test_results):
        """Sets the category_test_results of this TestrunresultGetCategoryResultsResponse.

        The list of summary test results.  # noqa: E501

        :param category_test_results: The category_test_results of this TestrunresultGetCategoryResultsResponse.  # noqa: E501
        :type: list[RimeCategoryTestResult]
        """

        self._category_test_results = category_test_results

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
        if issubclass(TestrunresultGetCategoryResultsResponse, dict):
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
        if not isinstance(other, TestrunresultGetCategoryResultsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
