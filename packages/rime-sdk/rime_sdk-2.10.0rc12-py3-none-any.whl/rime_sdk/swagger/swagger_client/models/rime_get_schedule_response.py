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

class RimeGetScheduleResponse(object):
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
        'schedule': 'ScheduleSchedule',
        'next_run_time': 'datetime'
    }

    attribute_map = {
        'schedule': 'schedule',
        'next_run_time': 'nextRunTime'
    }

    def __init__(self, schedule=None, next_run_time=None):  # noqa: E501
        """RimeGetScheduleResponse - a model defined in Swagger"""  # noqa: E501
        self._schedule = None
        self._next_run_time = None
        self.discriminator = None
        if schedule is not None:
            self.schedule = schedule
        if next_run_time is not None:
            self.next_run_time = next_run_time

    @property
    def schedule(self):
        """Gets the schedule of this RimeGetScheduleResponse.  # noqa: E501


        :return: The schedule of this RimeGetScheduleResponse.  # noqa: E501
        :rtype: ScheduleSchedule
        """
        return self._schedule

    @schedule.setter
    def schedule(self, schedule):
        """Sets the schedule of this RimeGetScheduleResponse.


        :param schedule: The schedule of this RimeGetScheduleResponse.  # noqa: E501
        :type: ScheduleSchedule
        """

        self._schedule = schedule

    @property
    def next_run_time(self):
        """Gets the next_run_time of this RimeGetScheduleResponse.  # noqa: E501


        :return: The next_run_time of this RimeGetScheduleResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._next_run_time

    @next_run_time.setter
    def next_run_time(self, next_run_time):
        """Sets the next_run_time of this RimeGetScheduleResponse.


        :param next_run_time: The next_run_time of this RimeGetScheduleResponse.  # noqa: E501
        :type: datetime
        """

        self._next_run_time = next_run_time

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
        if issubclass(RimeGetScheduleResponse, dict):
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
        if not isinstance(other, RimeGetScheduleResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
