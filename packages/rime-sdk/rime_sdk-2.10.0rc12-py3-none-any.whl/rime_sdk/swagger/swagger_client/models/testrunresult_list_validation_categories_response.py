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

class TestrunresultListValidationCategoriesResponse(object):
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
        'categories': 'list[TestrunTestCategoryType]'
    }

    attribute_map = {
        'categories': 'categories'
    }

    def __init__(self, categories=None):  # noqa: E501
        """TestrunresultListValidationCategoriesResponse - a model defined in Swagger"""  # noqa: E501
        self._categories = None
        self.discriminator = None
        if categories is not None:
            self.categories = categories

    @property
    def categories(self):
        """Gets the categories of this TestrunresultListValidationCategoriesResponse.  # noqa: E501


        :return: The categories of this TestrunresultListValidationCategoriesResponse.  # noqa: E501
        :rtype: list[TestrunTestCategoryType]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this TestrunresultListValidationCategoriesResponse.


        :param categories: The categories of this TestrunresultListValidationCategoriesResponse.  # noqa: E501
        :type: list[TestrunTestCategoryType]
        """

        self._categories = categories

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
        if issubclass(TestrunresultListValidationCategoriesResponse, dict):
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
        if not isinstance(other, TestrunresultListValidationCategoriesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
