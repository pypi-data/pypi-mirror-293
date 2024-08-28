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

class GenerativefirewallValidateResponse(object):
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
        'input_results': 'dict(str, GenerativefirewallRuleOutput)',
        'output_results': 'dict(str, GenerativefirewallRuleOutput)',
        'metadata': 'ValidateResponseProductMetadata',
        'processed_req': 'ValidateResponseProcessedRequest',
        'api_schema_version': 'str'
    }

    attribute_map = {
        'input_results': 'inputResults',
        'output_results': 'outputResults',
        'metadata': 'metadata',
        'processed_req': 'processedReq',
        'api_schema_version': 'apiSchemaVersion'
    }

    def __init__(self, input_results=None, output_results=None, metadata=None, processed_req=None, api_schema_version=None):  # noqa: E501
        """GenerativefirewallValidateResponse - a model defined in Swagger"""  # noqa: E501
        self._input_results = None
        self._output_results = None
        self._metadata = None
        self._processed_req = None
        self._api_schema_version = None
        self.discriminator = None
        if input_results is not None:
            self.input_results = input_results
        if output_results is not None:
            self.output_results = output_results
        if metadata is not None:
            self.metadata = metadata
        if processed_req is not None:
            self.processed_req = processed_req
        if api_schema_version is not None:
            self.api_schema_version = api_schema_version

    @property
    def input_results(self):
        """Gets the input_results of this GenerativefirewallValidateResponse.  # noqa: E501

        Results of the firewall for user input. The key is a rule name.  # noqa: E501

        :return: The input_results of this GenerativefirewallValidateResponse.  # noqa: E501
        :rtype: dict(str, GenerativefirewallRuleOutput)
        """
        return self._input_results

    @input_results.setter
    def input_results(self, input_results):
        """Sets the input_results of this GenerativefirewallValidateResponse.

        Results of the firewall for user input. The key is a rule name.  # noqa: E501

        :param input_results: The input_results of this GenerativefirewallValidateResponse.  # noqa: E501
        :type: dict(str, GenerativefirewallRuleOutput)
        """

        self._input_results = input_results

    @property
    def output_results(self):
        """Gets the output_results of this GenerativefirewallValidateResponse.  # noqa: E501

        Results of the firewall for model output. The key is a rule name.  # noqa: E501

        :return: The output_results of this GenerativefirewallValidateResponse.  # noqa: E501
        :rtype: dict(str, GenerativefirewallRuleOutput)
        """
        return self._output_results

    @output_results.setter
    def output_results(self, output_results):
        """Sets the output_results of this GenerativefirewallValidateResponse.

        Results of the firewall for model output. The key is a rule name.  # noqa: E501

        :param output_results: The output_results of this GenerativefirewallValidateResponse.  # noqa: E501
        :type: dict(str, GenerativefirewallRuleOutput)
        """

        self._output_results = output_results

    @property
    def metadata(self):
        """Gets the metadata of this GenerativefirewallValidateResponse.  # noqa: E501


        :return: The metadata of this GenerativefirewallValidateResponse.  # noqa: E501
        :rtype: ValidateResponseProductMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this GenerativefirewallValidateResponse.


        :param metadata: The metadata of this GenerativefirewallValidateResponse.  # noqa: E501
        :type: ValidateResponseProductMetadata
        """

        self._metadata = metadata

    @property
    def processed_req(self):
        """Gets the processed_req of this GenerativefirewallValidateResponse.  # noqa: E501


        :return: The processed_req of this GenerativefirewallValidateResponse.  # noqa: E501
        :rtype: ValidateResponseProcessedRequest
        """
        return self._processed_req

    @processed_req.setter
    def processed_req(self, processed_req):
        """Sets the processed_req of this GenerativefirewallValidateResponse.


        :param processed_req: The processed_req of this GenerativefirewallValidateResponse.  # noqa: E501
        :type: ValidateResponseProcessedRequest
        """

        self._processed_req = processed_req

    @property
    def api_schema_version(self):
        """Gets the api_schema_version of this GenerativefirewallValidateResponse.  # noqa: E501

        API schema version is the version of the API response. This should be updated whenever we make semantic changes to the response.  # noqa: E501

        :return: The api_schema_version of this GenerativefirewallValidateResponse.  # noqa: E501
        :rtype: str
        """
        return self._api_schema_version

    @api_schema_version.setter
    def api_schema_version(self, api_schema_version):
        """Sets the api_schema_version of this GenerativefirewallValidateResponse.

        API schema version is the version of the API response. This should be updated whenever we make semantic changes to the response.  # noqa: E501

        :param api_schema_version: The api_schema_version of this GenerativefirewallValidateResponse.  # noqa: E501
        :type: str
        """

        self._api_schema_version = api_schema_version

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
        if issubclass(GenerativefirewallValidateResponse, dict):
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
        if not isinstance(other, GenerativefirewallValidateResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
