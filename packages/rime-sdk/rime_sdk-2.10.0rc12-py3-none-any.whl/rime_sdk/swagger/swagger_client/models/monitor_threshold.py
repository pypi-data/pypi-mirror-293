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

class MonitorThreshold(object):
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
        'low': 'float',
        'high': 'float',
        'type': 'MonitorThresholdType'
    }

    attribute_map = {
        'low': 'low',
        'high': 'high',
        'type': 'type'
    }

    def __init__(self, low=None, high=None, type=None):  # noqa: E501
        """MonitorThreshold - a model defined in Swagger"""  # noqa: E501
        self._low = None
        self._high = None
        self._type = None
        self.discriminator = None
        if low is not None:
            self.low = low
        if high is not None:
            self.high = high
        if type is not None:
            self.type = type

    @property
    def low(self):
        """Gets the low of this MonitorThreshold.  # noqa: E501

        The threshold for warning.  # noqa: E501

        :return: The low of this MonitorThreshold.  # noqa: E501
        :rtype: float
        """
        return self._low

    @low.setter
    def low(self, low):
        """Sets the low of this MonitorThreshold.

        The threshold for warning.  # noqa: E501

        :param low: The low of this MonitorThreshold.  # noqa: E501
        :type: float
        """

        self._low = low

    @property
    def high(self):
        """Gets the high of this MonitorThreshold.  # noqa: E501

        The threshold for alert.  # noqa: E501

        :return: The high of this MonitorThreshold.  # noqa: E501
        :rtype: float
        """
        return self._high

    @high.setter
    def high(self, high):
        """Sets the high of this MonitorThreshold.

        The threshold for alert.  # noqa: E501

        :param high: The high of this MonitorThreshold.  # noqa: E501
        :type: float
        """

        self._high = high

    @property
    def type(self):
        """Gets the type of this MonitorThreshold.  # noqa: E501


        :return: The type of this MonitorThreshold.  # noqa: E501
        :rtype: MonitorThresholdType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this MonitorThreshold.


        :param type: The type of this MonitorThreshold.  # noqa: E501
        :type: MonitorThresholdType
        """

        self._type = type

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
        if issubclass(MonitorThreshold, dict):
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
        if not isinstance(other, MonitorThreshold):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
