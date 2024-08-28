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

class ListDatasetsRequestDatasetsQuery(object):
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
        'firewall_id': 'RimeUUID',
        'scheduled_ct_intervals': 'RimeTimeInterval'
    }

    attribute_map = {
        'firewall_id': 'firewallId',
        'scheduled_ct_intervals': 'scheduledCtIntervals'
    }

    def __init__(self, firewall_id=None, scheduled_ct_intervals=None):  # noqa: E501
        """ListDatasetsRequestDatasetsQuery - a model defined in Swagger"""  # noqa: E501
        self._firewall_id = None
        self._scheduled_ct_intervals = None
        self.discriminator = None
        if firewall_id is not None:
            self.firewall_id = firewall_id
        if scheduled_ct_intervals is not None:
            self.scheduled_ct_intervals = scheduled_ct_intervals

    @property
    def firewall_id(self):
        """Gets the firewall_id of this ListDatasetsRequestDatasetsQuery.  # noqa: E501


        :return: The firewall_id of this ListDatasetsRequestDatasetsQuery.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._firewall_id

    @firewall_id.setter
    def firewall_id(self, firewall_id):
        """Sets the firewall_id of this ListDatasetsRequestDatasetsQuery.


        :param firewall_id: The firewall_id of this ListDatasetsRequestDatasetsQuery.  # noqa: E501
        :type: RimeUUID
        """

        self._firewall_id = firewall_id

    @property
    def scheduled_ct_intervals(self):
        """Gets the scheduled_ct_intervals of this ListDatasetsRequestDatasetsQuery.  # noqa: E501


        :return: The scheduled_ct_intervals of this ListDatasetsRequestDatasetsQuery.  # noqa: E501
        :rtype: RimeTimeInterval
        """
        return self._scheduled_ct_intervals

    @scheduled_ct_intervals.setter
    def scheduled_ct_intervals(self, scheduled_ct_intervals):
        """Sets the scheduled_ct_intervals of this ListDatasetsRequestDatasetsQuery.


        :param scheduled_ct_intervals: The scheduled_ct_intervals of this ListDatasetsRequestDatasetsQuery.  # noqa: E501
        :type: RimeTimeInterval
        """

        self._scheduled_ct_intervals = scheduled_ct_intervals

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
        if issubclass(ListDatasetsRequestDatasetsQuery, dict):
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
        if not isinstance(other, ListDatasetsRequestDatasetsQuery):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
