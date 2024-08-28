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

class RimeCreateAPITokenRequest(object):
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
        'name': 'str',
        'workspace_id': 'RimeUUID',
        'token_type': 'RimeTokenType',
        'agent_id': 'RimeUUID',
        'expiry_days': 'int'
    }

    attribute_map = {
        'name': 'name',
        'workspace_id': 'workspaceId',
        'token_type': 'tokenType',
        'agent_id': 'agentId',
        'expiry_days': 'expiryDays'
    }

    def __init__(self, name=None, workspace_id=None, token_type=None, agent_id=None, expiry_days=None):  # noqa: E501
        """RimeCreateAPITokenRequest - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._workspace_id = None
        self._token_type = None
        self._agent_id = None
        self._expiry_days = None
        self.discriminator = None
        self.name = name
        if workspace_id is not None:
            self.workspace_id = workspace_id
        if token_type is not None:
            self.token_type = token_type
        if agent_id is not None:
            self.agent_id = agent_id
        if expiry_days is not None:
            self.expiry_days = expiry_days

    @property
    def name(self):
        """Gets the name of this RimeCreateAPITokenRequest.  # noqa: E501

        Name of the API token.  # noqa: E501

        :return: The name of this RimeCreateAPITokenRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this RimeCreateAPITokenRequest.

        Name of the API token.  # noqa: E501

        :param name: The name of this RimeCreateAPITokenRequest.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def workspace_id(self):
        """Gets the workspace_id of this RimeCreateAPITokenRequest.  # noqa: E501


        :return: The workspace_id of this RimeCreateAPITokenRequest.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._workspace_id

    @workspace_id.setter
    def workspace_id(self, workspace_id):
        """Sets the workspace_id of this RimeCreateAPITokenRequest.


        :param workspace_id: The workspace_id of this RimeCreateAPITokenRequest.  # noqa: E501
        :type: RimeUUID
        """

        self._workspace_id = workspace_id

    @property
    def token_type(self):
        """Gets the token_type of this RimeCreateAPITokenRequest.  # noqa: E501


        :return: The token_type of this RimeCreateAPITokenRequest.  # noqa: E501
        :rtype: RimeTokenType
        """
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        """Sets the token_type of this RimeCreateAPITokenRequest.


        :param token_type: The token_type of this RimeCreateAPITokenRequest.  # noqa: E501
        :type: RimeTokenType
        """

        self._token_type = token_type

    @property
    def agent_id(self):
        """Gets the agent_id of this RimeCreateAPITokenRequest.  # noqa: E501


        :return: The agent_id of this RimeCreateAPITokenRequest.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        """Sets the agent_id of this RimeCreateAPITokenRequest.


        :param agent_id: The agent_id of this RimeCreateAPITokenRequest.  # noqa: E501
        :type: RimeUUID
        """

        self._agent_id = agent_id

    @property
    def expiry_days(self):
        """Gets the expiry_days of this RimeCreateAPITokenRequest.  # noqa: E501


        :return: The expiry_days of this RimeCreateAPITokenRequest.  # noqa: E501
        :rtype: int
        """
        return self._expiry_days

    @expiry_days.setter
    def expiry_days(self, expiry_days):
        """Sets the expiry_days of this RimeCreateAPITokenRequest.


        :param expiry_days: The expiry_days of this RimeCreateAPITokenRequest.  # noqa: E501
        :type: int
        """

        self._expiry_days = expiry_days

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
        if issubclass(RimeCreateAPITokenRequest, dict):
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
        if not isinstance(other, RimeCreateAPITokenRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
