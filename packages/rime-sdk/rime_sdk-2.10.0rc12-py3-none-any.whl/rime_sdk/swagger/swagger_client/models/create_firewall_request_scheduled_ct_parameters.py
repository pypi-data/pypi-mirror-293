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

class CreateFirewallRequestScheduledCTParameters(object):
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
        'eval_data_integration_id': 'RimeUUID',
        'eval_data_info': 'RegistryDataInfo',
        'eval_pred_integration_id': 'RimeUUID',
        'eval_pred_info': 'RegistryPredInfo'
    }

    attribute_map = {
        'eval_data_integration_id': 'evalDataIntegrationId',
        'eval_data_info': 'evalDataInfo',
        'eval_pred_integration_id': 'evalPredIntegrationId',
        'eval_pred_info': 'evalPredInfo'
    }

    def __init__(self, eval_data_integration_id=None, eval_data_info=None, eval_pred_integration_id=None, eval_pred_info=None):  # noqa: E501
        """CreateFirewallRequestScheduledCTParameters - a model defined in Swagger"""  # noqa: E501
        self._eval_data_integration_id = None
        self._eval_data_info = None
        self._eval_pred_integration_id = None
        self._eval_pred_info = None
        self.discriminator = None
        if eval_data_integration_id is not None:
            self.eval_data_integration_id = eval_data_integration_id
        if eval_data_info is not None:
            self.eval_data_info = eval_data_info
        if eval_pred_integration_id is not None:
            self.eval_pred_integration_id = eval_pred_integration_id
        if eval_pred_info is not None:
            self.eval_pred_info = eval_pred_info

    @property
    def eval_data_integration_id(self):
        """Gets the eval_data_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501


        :return: The eval_data_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._eval_data_integration_id

    @eval_data_integration_id.setter
    def eval_data_integration_id(self, eval_data_integration_id):
        """Sets the eval_data_integration_id of this CreateFirewallRequestScheduledCTParameters.


        :param eval_data_integration_id: The eval_data_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :type: RimeUUID
        """

        self._eval_data_integration_id = eval_data_integration_id

    @property
    def eval_data_info(self):
        """Gets the eval_data_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501


        :return: The eval_data_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :rtype: RegistryDataInfo
        """
        return self._eval_data_info

    @eval_data_info.setter
    def eval_data_info(self, eval_data_info):
        """Sets the eval_data_info of this CreateFirewallRequestScheduledCTParameters.


        :param eval_data_info: The eval_data_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :type: RegistryDataInfo
        """

        self._eval_data_info = eval_data_info

    @property
    def eval_pred_integration_id(self):
        """Gets the eval_pred_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501


        :return: The eval_pred_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._eval_pred_integration_id

    @eval_pred_integration_id.setter
    def eval_pred_integration_id(self, eval_pred_integration_id):
        """Sets the eval_pred_integration_id of this CreateFirewallRequestScheduledCTParameters.


        :param eval_pred_integration_id: The eval_pred_integration_id of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :type: RimeUUID
        """

        self._eval_pred_integration_id = eval_pred_integration_id

    @property
    def eval_pred_info(self):
        """Gets the eval_pred_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501


        :return: The eval_pred_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :rtype: RegistryPredInfo
        """
        return self._eval_pred_info

    @eval_pred_info.setter
    def eval_pred_info(self, eval_pred_info):
        """Sets the eval_pred_info of this CreateFirewallRequestScheduledCTParameters.


        :param eval_pred_info: The eval_pred_info of this CreateFirewallRequestScheduledCTParameters.  # noqa: E501
        :type: RegistryPredInfo
        """

        self._eval_pred_info = eval_pred_info

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
        if issubclass(CreateFirewallRequestScheduledCTParameters, dict):
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
        if not isinstance(other, CreateFirewallRequestScheduledCTParameters):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
