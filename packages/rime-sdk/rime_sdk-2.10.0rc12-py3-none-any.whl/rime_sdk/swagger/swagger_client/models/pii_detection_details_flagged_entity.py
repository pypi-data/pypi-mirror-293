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

class PiiDetectionDetailsFlaggedEntity(object):
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
        'entity_type': 'GenerativefirewallPiiEntityType',
        'custom_entity_name': 'str',
        'flagged_substring': 'GenerativefirewallFlaggedSubstring',
        'confidence_score': 'float'
    }

    attribute_map = {
        'entity_type': 'entityType',
        'custom_entity_name': 'customEntityName',
        'flagged_substring': 'flaggedSubstring',
        'confidence_score': 'confidenceScore'
    }

    def __init__(self, entity_type=None, custom_entity_name=None, flagged_substring=None, confidence_score=None):  # noqa: E501
        """PiiDetectionDetailsFlaggedEntity - a model defined in Swagger"""  # noqa: E501
        self._entity_type = None
        self._custom_entity_name = None
        self._flagged_substring = None
        self._confidence_score = None
        self.discriminator = None
        if entity_type is not None:
            self.entity_type = entity_type
        if custom_entity_name is not None:
            self.custom_entity_name = custom_entity_name
        if flagged_substring is not None:
            self.flagged_substring = flagged_substring
        if confidence_score is not None:
            self.confidence_score = confidence_score

    @property
    def entity_type(self):
        """Gets the entity_type of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501


        :return: The entity_type of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :rtype: GenerativefirewallPiiEntityType
        """
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        """Sets the entity_type of this PiiDetectionDetailsFlaggedEntity.


        :param entity_type: The entity_type of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :type: GenerativefirewallPiiEntityType
        """

        self._entity_type = entity_type

    @property
    def custom_entity_name(self):
        """Gets the custom_entity_name of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501

        Custom entity name is the name of the custom-defined entity that was detected for this substring, if applicable.  # noqa: E501

        :return: The custom_entity_name of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :rtype: str
        """
        return self._custom_entity_name

    @custom_entity_name.setter
    def custom_entity_name(self, custom_entity_name):
        """Sets the custom_entity_name of this PiiDetectionDetailsFlaggedEntity.

        Custom entity name is the name of the custom-defined entity that was detected for this substring, if applicable.  # noqa: E501

        :param custom_entity_name: The custom_entity_name of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :type: str
        """

        self._custom_entity_name = custom_entity_name

    @property
    def flagged_substring(self):
        """Gets the flagged_substring of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501


        :return: The flagged_substring of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :rtype: GenerativefirewallFlaggedSubstring
        """
        return self._flagged_substring

    @flagged_substring.setter
    def flagged_substring(self, flagged_substring):
        """Sets the flagged_substring of this PiiDetectionDetailsFlaggedEntity.


        :param flagged_substring: The flagged_substring of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :type: GenerativefirewallFlaggedSubstring
        """

        self._flagged_substring = flagged_substring

    @property
    def confidence_score(self):
        """Gets the confidence_score of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501

        Confidence score is a metric of how confident (on a scale of 0-1) the rule is about this entity being flagged.  # noqa: E501

        :return: The confidence_score of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :rtype: float
        """
        return self._confidence_score

    @confidence_score.setter
    def confidence_score(self, confidence_score):
        """Sets the confidence_score of this PiiDetectionDetailsFlaggedEntity.

        Confidence score is a metric of how confident (on a scale of 0-1) the rule is about this entity being flagged.  # noqa: E501

        :param confidence_score: The confidence_score of this PiiDetectionDetailsFlaggedEntity.  # noqa: E501
        :type: float
        """

        self._confidence_score = confidence_score

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
        if issubclass(PiiDetectionDetailsFlaggedEntity, dict):
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
        if not isinstance(other, PiiDetectionDetailsFlaggedEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
