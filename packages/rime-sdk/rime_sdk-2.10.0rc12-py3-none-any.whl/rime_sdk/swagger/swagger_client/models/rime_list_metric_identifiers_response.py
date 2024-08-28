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

class RimeListMetricIdentifiersResponse(object):
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
        'aggregated_metrics': 'list[ListMetricIdentifiersResponseAggregatedMetric]',
        'feature_metrics': 'dict(str, ListMetricIdentifiersResponseFeatureMetrics)'
    }

    attribute_map = {
        'aggregated_metrics': 'aggregatedMetrics',
        'feature_metrics': 'featureMetrics'
    }

    def __init__(self, aggregated_metrics=None, feature_metrics=None):  # noqa: E501
        """RimeListMetricIdentifiersResponse - a model defined in Swagger"""  # noqa: E501
        self._aggregated_metrics = None
        self._feature_metrics = None
        self.discriminator = None
        if aggregated_metrics is not None:
            self.aggregated_metrics = aggregated_metrics
        if feature_metrics is not None:
            self.feature_metrics = feature_metrics

    @property
    def aggregated_metrics(self):
        """Gets the aggregated_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501


        :return: The aggregated_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501
        :rtype: list[ListMetricIdentifiersResponseAggregatedMetric]
        """
        return self._aggregated_metrics

    @aggregated_metrics.setter
    def aggregated_metrics(self, aggregated_metrics):
        """Sets the aggregated_metrics of this RimeListMetricIdentifiersResponse.


        :param aggregated_metrics: The aggregated_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501
        :type: list[ListMetricIdentifiersResponseAggregatedMetric]
        """

        self._aggregated_metrics = aggregated_metrics

    @property
    def feature_metrics(self):
        """Gets the feature_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501


        :return: The feature_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501
        :rtype: dict(str, ListMetricIdentifiersResponseFeatureMetrics)
        """
        return self._feature_metrics

    @feature_metrics.setter
    def feature_metrics(self, feature_metrics):
        """Sets the feature_metrics of this RimeListMetricIdentifiersResponse.


        :param feature_metrics: The feature_metrics of this RimeListMetricIdentifiersResponse.  # noqa: E501
        :type: dict(str, ListMetricIdentifiersResponseFeatureMetrics)
        """

        self._feature_metrics = feature_metrics

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
        if issubclass(RimeListMetricIdentifiersResponse, dict):
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
        if not isinstance(other, RimeListMetricIdentifiersResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
