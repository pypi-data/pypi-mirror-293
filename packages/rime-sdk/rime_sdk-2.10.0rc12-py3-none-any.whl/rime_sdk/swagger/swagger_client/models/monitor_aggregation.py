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

class MonitorAggregation(object):
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
        'aggregation_type': 'MonitorAggregationType',
        'time_window': 'str'
    }

    attribute_map = {
        'aggregation_type': 'aggregationType',
        'time_window': 'timeWindow'
    }

    def __init__(self, aggregation_type=None, time_window=None):  # noqa: E501
        """MonitorAggregation - a model defined in Swagger"""  # noqa: E501
        self._aggregation_type = None
        self._time_window = None
        self.discriminator = None
        if aggregation_type is not None:
            self.aggregation_type = aggregation_type
        if time_window is not None:
            self.time_window = time_window

    @property
    def aggregation_type(self):
        """Gets the aggregation_type of this MonitorAggregation.  # noqa: E501


        :return: The aggregation_type of this MonitorAggregation.  # noqa: E501
        :rtype: MonitorAggregationType
        """
        return self._aggregation_type

    @aggregation_type.setter
    def aggregation_type(self, aggregation_type):
        """Sets the aggregation_type of this MonitorAggregation.


        :param aggregation_type: The aggregation_type of this MonitorAggregation.  # noqa: E501
        :type: MonitorAggregationType
        """

        self._aggregation_type = aggregation_type

    @property
    def time_window(self):
        """Gets the time_window of this MonitorAggregation.  # noqa: E501


        :return: The time_window of this MonitorAggregation.  # noqa: E501
        :rtype: str
        """
        return self._time_window

    @time_window.setter
    def time_window(self, time_window):
        """Sets the time_window of this MonitorAggregation.


        :param time_window: The time_window of this MonitorAggregation.  # noqa: E501
        :type: str
        """

        self._time_window = time_window

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
        if issubclass(MonitorAggregation, dict):
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
        if not isinstance(other, MonitorAggregation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
