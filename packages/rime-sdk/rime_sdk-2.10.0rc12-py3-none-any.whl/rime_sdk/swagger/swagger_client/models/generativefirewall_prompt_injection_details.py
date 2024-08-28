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

class GenerativefirewallPromptInjectionDetails(object):
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
        'objectives': 'list[RimeAttackObjective]',
        'techniques': 'list[RimeAttackTechnique]'
    }

    attribute_map = {
        'objectives': 'objectives',
        'techniques': 'techniques'
    }

    def __init__(self, objectives=None, techniques=None):  # noqa: E501
        """GenerativefirewallPromptInjectionDetails - a model defined in Swagger"""  # noqa: E501
        self._objectives = None
        self._techniques = None
        self.discriminator = None
        if objectives is not None:
            self.objectives = objectives
        if techniques is not None:
            self.techniques = techniques

    @property
    def objectives(self):
        """Gets the objectives of this GenerativefirewallPromptInjectionDetails.  # noqa: E501

        Objectives represent the attack objectives found in the text, such as privacy or abuse violations.  # noqa: E501

        :return: The objectives of this GenerativefirewallPromptInjectionDetails.  # noqa: E501
        :rtype: list[RimeAttackObjective]
        """
        return self._objectives

    @objectives.setter
    def objectives(self, objectives):
        """Sets the objectives of this GenerativefirewallPromptInjectionDetails.

        Objectives represent the attack objectives found in the text, such as privacy or abuse violations.  # noqa: E501

        :param objectives: The objectives of this GenerativefirewallPromptInjectionDetails.  # noqa: E501
        :type: list[RimeAttackObjective]
        """

        self._objectives = objectives

    @property
    def techniques(self):
        """Gets the techniques of this GenerativefirewallPromptInjectionDetails.  # noqa: E501

        Attack Techniques represent the technique used in a prompt injection for example: unicode obfuscation, base64 etc. These values may change between versions.  # noqa: E501

        :return: The techniques of this GenerativefirewallPromptInjectionDetails.  # noqa: E501
        :rtype: list[RimeAttackTechnique]
        """
        return self._techniques

    @techniques.setter
    def techniques(self, techniques):
        """Sets the techniques of this GenerativefirewallPromptInjectionDetails.

        Attack Techniques represent the technique used in a prompt injection for example: unicode obfuscation, base64 etc. These values may change between versions.  # noqa: E501

        :param techniques: The techniques of this GenerativefirewallPromptInjectionDetails.  # noqa: E501
        :type: list[RimeAttackTechnique]
        """

        self._techniques = techniques

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
        if issubclass(GenerativefirewallPromptInjectionDetails, dict):
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
        if not isinstance(other, GenerativefirewallPromptInjectionDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
