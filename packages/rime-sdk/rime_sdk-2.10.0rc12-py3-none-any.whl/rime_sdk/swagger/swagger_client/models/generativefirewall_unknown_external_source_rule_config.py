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

class GenerativefirewallUnknownExternalSourceRuleConfig(object):
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
        'whitelisted_urls': 'list[str]',
        'ignore_contexts': 'bool'
    }

    attribute_map = {
        'whitelisted_urls': 'whitelistedUrls',
        'ignore_contexts': 'ignoreContexts'
    }

    def __init__(self, whitelisted_urls=None, ignore_contexts=None):  # noqa: E501
        """GenerativefirewallUnknownExternalSourceRuleConfig - a model defined in Swagger"""  # noqa: E501
        self._whitelisted_urls = None
        self._ignore_contexts = None
        self.discriminator = None
        if whitelisted_urls is not None:
            self.whitelisted_urls = whitelisted_urls
        if ignore_contexts is not None:
            self.ignore_contexts = ignore_contexts

    @property
    def whitelisted_urls(self):
        """Gets the whitelisted_urls of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501

        Whitelisted URLs is a list of the URL domains that should not be flagged by the unknown external source rule.  # noqa: E501

        :return: The whitelisted_urls of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._whitelisted_urls

    @whitelisted_urls.setter
    def whitelisted_urls(self, whitelisted_urls):
        """Sets the whitelisted_urls of this GenerativefirewallUnknownExternalSourceRuleConfig.

        Whitelisted URLs is a list of the URL domains that should not be flagged by the unknown external source rule.  # noqa: E501

        :param whitelisted_urls: The whitelisted_urls of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501
        :type: list[str]
        """

        self._whitelisted_urls = whitelisted_urls

    @property
    def ignore_contexts(self):
        """Gets the ignore_contexts of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501

        Ignore contexts specifies whether the firewall should skip the contexts field of the model input in the firewall validate request.  # noqa: E501

        :return: The ignore_contexts of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501
        :rtype: bool
        """
        return self._ignore_contexts

    @ignore_contexts.setter
    def ignore_contexts(self, ignore_contexts):
        """Sets the ignore_contexts of this GenerativefirewallUnknownExternalSourceRuleConfig.

        Ignore contexts specifies whether the firewall should skip the contexts field of the model input in the firewall validate request.  # noqa: E501

        :param ignore_contexts: The ignore_contexts of this GenerativefirewallUnknownExternalSourceRuleConfig.  # noqa: E501
        :type: bool
        """

        self._ignore_contexts = ignore_contexts

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
        if issubclass(GenerativefirewallUnknownExternalSourceRuleConfig, dict):
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
        if not isinstance(other, GenerativefirewallUnknownExternalSourceRuleConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
