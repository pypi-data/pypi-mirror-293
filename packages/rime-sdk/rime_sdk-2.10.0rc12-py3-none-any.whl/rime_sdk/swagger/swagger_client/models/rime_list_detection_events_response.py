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

class RimeListDetectionEventsResponse(object):
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
        'events': 'list[DetectionDetectionEvent]',
        'next_page_token': 'str',
        'has_more': 'bool'
    }

    attribute_map = {
        'events': 'events',
        'next_page_token': 'nextPageToken',
        'has_more': 'hasMore'
    }

    def __init__(self, events=None, next_page_token=None, has_more=None):  # noqa: E501
        """RimeListDetectionEventsResponse - a model defined in Swagger"""  # noqa: E501
        self._events = None
        self._next_page_token = None
        self._has_more = None
        self.discriminator = None
        if events is not None:
            self.events = events
        if next_page_token is not None:
            self.next_page_token = next_page_token
        if has_more is not None:
            self.has_more = has_more

    @property
    def events(self):
        """Gets the events of this RimeListDetectionEventsResponse.  # noqa: E501

        Page of events returned from the backend.  # noqa: E501

        :return: The events of this RimeListDetectionEventsResponse.  # noqa: E501
        :rtype: list[DetectionDetectionEvent]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this RimeListDetectionEventsResponse.

        Page of events returned from the backend.  # noqa: E501

        :param events: The events of this RimeListDetectionEventsResponse.  # noqa: E501
        :type: list[DetectionDetectionEvent]
        """

        self._events = events

    @property
    def next_page_token(self):
        """Gets the next_page_token of this RimeListDetectionEventsResponse.  # noqa: E501

        Page token to use in the next ListDetectionEvents call.  # noqa: E501

        :return: The next_page_token of this RimeListDetectionEventsResponse.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """Sets the next_page_token of this RimeListDetectionEventsResponse.

        Page token to use in the next ListDetectionEvents call.  # noqa: E501

        :param next_page_token: The next_page_token of this RimeListDetectionEventsResponse.  # noqa: E501
        :type: str
        """

        self._next_page_token = next_page_token

    @property
    def has_more(self):
        """Gets the has_more of this RimeListDetectionEventsResponse.  # noqa: E501

        Indicates whether there are more events to return.  # noqa: E501

        :return: The has_more of this RimeListDetectionEventsResponse.  # noqa: E501
        :rtype: bool
        """
        return self._has_more

    @has_more.setter
    def has_more(self, has_more):
        """Sets the has_more of this RimeListDetectionEventsResponse.

        Indicates whether there are more events to return.  # noqa: E501

        :param has_more: The has_more of this RimeListDetectionEventsResponse.  # noqa: E501
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
        if issubclass(RimeListDetectionEventsResponse, dict):
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
        if not isinstance(other, RimeListDetectionEventsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
