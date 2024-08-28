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

class FirewallInstanceIdUuidValidateBody(object):
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
        'user_input_text': 'str',
        'contexts': 'list[str]',
        'output_text': 'str',
        'firewall_instance_id': 'object'
    }

    attribute_map = {
        'user_input_text': 'userInputText',
        'contexts': 'contexts',
        'output_text': 'outputText',
        'firewall_instance_id': 'firewallInstanceId'
    }

    def __init__(self, user_input_text=None, contexts=None, output_text=None, firewall_instance_id=None):  # noqa: E501
        """FirewallInstanceIdUuidValidateBody - a model defined in Swagger"""  # noqa: E501
        self._user_input_text = None
        self._contexts = None
        self._output_text = None
        self._firewall_instance_id = None
        self.discriminator = None
        if user_input_text is not None:
            self.user_input_text = user_input_text
        if contexts is not None:
            self.contexts = contexts
        if output_text is not None:
            self.output_text = output_text
        if firewall_instance_id is not None:
            self.firewall_instance_id = firewall_instance_id

    @property
    def user_input_text(self):
        """Gets the user_input_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501

        Input text is the raw user input. The generative firewall performs validation on input to prevent risk configured by firewall rules.  # noqa: E501

        :return: The user_input_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :rtype: str
        """
        return self._user_input_text

    @user_input_text.setter
    def user_input_text(self, user_input_text):
        """Sets the user_input_text of this FirewallInstanceIdUuidValidateBody.

        Input text is the raw user input. The generative firewall performs validation on input to prevent risk configured by firewall rules.  # noqa: E501

        :param user_input_text: The user_input_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :type: str
        """

        self._user_input_text = user_input_text

    @property
    def contexts(self):
        """Gets the contexts of this FirewallInstanceIdUuidValidateBody.  # noqa: E501

        Documents that represent relevant context for the input query that is fed into the model. e.g. in a RAG application this will be the documents loaded during the RAG Retrieval phase to augment the LLM's response.  # noqa: E501

        :return: The contexts of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :rtype: list[str]
        """
        return self._contexts

    @contexts.setter
    def contexts(self, contexts):
        """Sets the contexts of this FirewallInstanceIdUuidValidateBody.

        Documents that represent relevant context for the input query that is fed into the model. e.g. in a RAG application this will be the documents loaded during the RAG Retrieval phase to augment the LLM's response.  # noqa: E501

        :param contexts: The contexts of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :type: list[str]
        """

        self._contexts = contexts

    @property
    def output_text(self):
        """Gets the output_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501

        Output text is the raw output text of the model. The generative firewall performs validation on the output so the system can determine whether to show it to users.  # noqa: E501

        :return: The output_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :rtype: str
        """
        return self._output_text

    @output_text.setter
    def output_text(self, output_text):
        """Sets the output_text of this FirewallInstanceIdUuidValidateBody.

        Output text is the raw output text of the model. The generative firewall performs validation on the output so the system can determine whether to show it to users.  # noqa: E501

        :param output_text: The output_text of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :type: str
        """

        self._output_text = output_text

    @property
    def firewall_instance_id(self):
        """Gets the firewall_instance_id of this FirewallInstanceIdUuidValidateBody.  # noqa: E501

        Unique ID of an object in RIME.  # noqa: E501

        :return: The firewall_instance_id of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :rtype: object
        """
        return self._firewall_instance_id

    @firewall_instance_id.setter
    def firewall_instance_id(self, firewall_instance_id):
        """Sets the firewall_instance_id of this FirewallInstanceIdUuidValidateBody.

        Unique ID of an object in RIME.  # noqa: E501

        :param firewall_instance_id: The firewall_instance_id of this FirewallInstanceIdUuidValidateBody.  # noqa: E501
        :type: object
        """

        self._firewall_instance_id = firewall_instance_id

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
        if issubclass(FirewallInstanceIdUuidValidateBody, dict):
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
        if not isinstance(other, FirewallInstanceIdUuidValidateBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
