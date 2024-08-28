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

class DetectionEventDetail(object):
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
        'metric_degradation': 'DetectionMetricDegradationEventDetails',
        'security': 'DetectionSecurityEventDetails'
    }

    attribute_map = {
        'metric_degradation': 'metricDegradation',
        'security': 'security'
    }

    def __init__(self, metric_degradation=None, security=None):  # noqa: E501
        """DetectionEventDetail - a model defined in Swagger"""  # noqa: E501
        self._metric_degradation = None
        self._security = None
        self.discriminator = None
        if metric_degradation is not None:
            self.metric_degradation = metric_degradation
        if security is not None:
            self.security = security

    @property
    def metric_degradation(self):
        """Gets the metric_degradation of this DetectionEventDetail.  # noqa: E501


        :return: The metric_degradation of this DetectionEventDetail.  # noqa: E501
        :rtype: DetectionMetricDegradationEventDetails
        """
        return self._metric_degradation

    @metric_degradation.setter
    def metric_degradation(self, metric_degradation):
        """Sets the metric_degradation of this DetectionEventDetail.


        :param metric_degradation: The metric_degradation of this DetectionEventDetail.  # noqa: E501
        :type: DetectionMetricDegradationEventDetails
        """

        self._metric_degradation = metric_degradation

    @property
    def security(self):
        """Gets the security of this DetectionEventDetail.  # noqa: E501


        :return: The security of this DetectionEventDetail.  # noqa: E501
        :rtype: DetectionSecurityEventDetails
        """
        return self._security

    @security.setter
    def security(self, security):
        """Sets the security of this DetectionEventDetail.


        :param security: The security of this DetectionEventDetail.  # noqa: E501
        :type: DetectionSecurityEventDetails
        """

        self._security = security

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
        if issubclass(DetectionEventDetail, dict):
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
        if not isinstance(other, DetectionEventDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
