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

class RimeAgentDesiredState(object):
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
        'version': 'str',
        'custom_values': 'dict(str, str)',
        'upgrade_status': 'RimeDetailedUpgradeStatus'
    }

    attribute_map = {
        'version': 'version',
        'custom_values': 'customValues',
        'upgrade_status': 'upgradeStatus'
    }

    def __init__(self, version=None, custom_values=None, upgrade_status=None):  # noqa: E501
        """RimeAgentDesiredState - a model defined in Swagger"""  # noqa: E501
        self._version = None
        self._custom_values = None
        self._upgrade_status = None
        self.discriminator = None
        if version is not None:
            self.version = version
        if custom_values is not None:
            self.custom_values = custom_values
        if upgrade_status is not None:
            self.upgrade_status = upgrade_status

    @property
    def version(self):
        """Gets the version of this RimeAgentDesiredState.  # noqa: E501

        Desired agent release version. E.g., 2.7.1 This is always set to the current control plane version.  # noqa: E501

        :return: The version of this RimeAgentDesiredState.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this RimeAgentDesiredState.

        Desired agent release version. E.g., 2.7.1 This is always set to the current control plane version.  # noqa: E501

        :param version: The version of this RimeAgentDesiredState.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def custom_values(self):
        """Gets the custom_values of this RimeAgentDesiredState.  # noqa: E501

        Example:   {     \"rimeAgent.images.agentImage.registry\": \"docker.io\",   }  # noqa: E501

        :return: The custom_values of this RimeAgentDesiredState.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._custom_values

    @custom_values.setter
    def custom_values(self, custom_values):
        """Sets the custom_values of this RimeAgentDesiredState.

        Example:   {     \"rimeAgent.images.agentImage.registry\": \"docker.io\",   }  # noqa: E501

        :param custom_values: The custom_values of this RimeAgentDesiredState.  # noqa: E501
        :type: dict(str, str)
        """

        self._custom_values = custom_values

    @property
    def upgrade_status(self):
        """Gets the upgrade_status of this RimeAgentDesiredState.  # noqa: E501


        :return: The upgrade_status of this RimeAgentDesiredState.  # noqa: E501
        :rtype: RimeDetailedUpgradeStatus
        """
        return self._upgrade_status

    @upgrade_status.setter
    def upgrade_status(self, upgrade_status):
        """Sets the upgrade_status of this RimeAgentDesiredState.


        :param upgrade_status: The upgrade_status of this RimeAgentDesiredState.  # noqa: E501
        :type: RimeDetailedUpgradeStatus
        """

        self._upgrade_status = upgrade_status

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
        if issubclass(RimeAgentDesiredState, dict):
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
        if not isinstance(other, RimeAgentDesiredState):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
