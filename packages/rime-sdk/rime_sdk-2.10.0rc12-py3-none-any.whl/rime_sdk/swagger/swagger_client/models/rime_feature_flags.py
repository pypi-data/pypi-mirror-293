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

class RimeFeatureFlags(object):
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
        'customer_name': 'str',
        'subscription_expiration_time': 'datetime',
        'upload_size_bytes': 'str',
        'enable_model_cards': 'bool'
    }

    attribute_map = {
        'customer_name': 'customerName',
        'subscription_expiration_time': 'subscriptionExpirationTime',
        'upload_size_bytes': 'uploadSizeBytes',
        'enable_model_cards': 'enableModelCards'
    }

    def __init__(self, customer_name=None, subscription_expiration_time=None, upload_size_bytes=None, enable_model_cards=None):  # noqa: E501
        """RimeFeatureFlags - a model defined in Swagger"""  # noqa: E501
        self._customer_name = None
        self._subscription_expiration_time = None
        self._upload_size_bytes = None
        self._enable_model_cards = None
        self.discriminator = None
        if customer_name is not None:
            self.customer_name = customer_name
        if subscription_expiration_time is not None:
            self.subscription_expiration_time = subscription_expiration_time
        if upload_size_bytes is not None:
            self.upload_size_bytes = upload_size_bytes
        if enable_model_cards is not None:
            self.enable_model_cards = enable_model_cards

    @property
    def customer_name(self):
        """Gets the customer_name of this RimeFeatureFlags.  # noqa: E501

        Customer Name. We maintain 1 set per customer. We need this for multi-tenancy (N customers in 1 cluster).  # noqa: E501

        :return: The customer_name of this RimeFeatureFlags.  # noqa: E501
        :rtype: str
        """
        return self._customer_name

    @customer_name.setter
    def customer_name(self, customer_name):
        """Sets the customer_name of this RimeFeatureFlags.

        Customer Name. We maintain 1 set per customer. We need this for multi-tenancy (N customers in 1 cluster).  # noqa: E501

        :param customer_name: The customer_name of this RimeFeatureFlags.  # noqa: E501
        :type: str
        """

        self._customer_name = customer_name

    @property
    def subscription_expiration_time(self):
        """Gets the subscription_expiration_time of this RimeFeatureFlags.  # noqa: E501

        Subscription time.  # noqa: E501

        :return: The subscription_expiration_time of this RimeFeatureFlags.  # noqa: E501
        :rtype: datetime
        """
        return self._subscription_expiration_time

    @subscription_expiration_time.setter
    def subscription_expiration_time(self, subscription_expiration_time):
        """Sets the subscription_expiration_time of this RimeFeatureFlags.

        Subscription time.  # noqa: E501

        :param subscription_expiration_time: The subscription_expiration_time of this RimeFeatureFlags.  # noqa: E501
        :type: datetime
        """

        self._subscription_expiration_time = subscription_expiration_time

    @property
    def upload_size_bytes(self):
        """Gets the upload_size_bytes of this RimeFeatureFlags.  # noqa: E501

        Upload data size.  # noqa: E501

        :return: The upload_size_bytes of this RimeFeatureFlags.  # noqa: E501
        :rtype: str
        """
        return self._upload_size_bytes

    @upload_size_bytes.setter
    def upload_size_bytes(self, upload_size_bytes):
        """Sets the upload_size_bytes of this RimeFeatureFlags.

        Upload data size.  # noqa: E501

        :param upload_size_bytes: The upload_size_bytes of this RimeFeatureFlags.  # noqa: E501
        :type: str
        """

        self._upload_size_bytes = upload_size_bytes

    @property
    def enable_model_cards(self):
        """Gets the enable_model_cards of this RimeFeatureFlags.  # noqa: E501

        Compliance model cards feature.  # noqa: E501

        :return: The enable_model_cards of this RimeFeatureFlags.  # noqa: E501
        :rtype: bool
        """
        return self._enable_model_cards

    @enable_model_cards.setter
    def enable_model_cards(self, enable_model_cards):
        """Sets the enable_model_cards of this RimeFeatureFlags.

        Compliance model cards feature.  # noqa: E501

        :param enable_model_cards: The enable_model_cards of this RimeFeatureFlags.  # noqa: E501
        :type: bool
        """

        self._enable_model_cards = enable_model_cards

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
        if issubclass(RimeFeatureFlags, dict):
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
        if not isinstance(other, RimeFeatureFlags):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
