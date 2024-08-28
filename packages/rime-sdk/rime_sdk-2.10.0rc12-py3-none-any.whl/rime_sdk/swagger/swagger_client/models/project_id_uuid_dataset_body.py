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

class ProjectIdUuidDatasetBody(object):
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
        'project_id': 'object',
        'name': 'str',
        'metadata': 'RegistryMetadata',
        'integration_id': 'RimeUUID',
        'data_info': 'RegistryDataInfo',
        'ct_info': 'DatasetCTInfo',
        'skip_validation': 'bool',
        'agent_id': 'RimeUUID'
    }

    attribute_map = {
        'project_id': 'projectId',
        'name': 'name',
        'metadata': 'metadata',
        'integration_id': 'integrationId',
        'data_info': 'dataInfo',
        'ct_info': 'ctInfo',
        'skip_validation': 'skipValidation',
        'agent_id': 'agentId'
    }

    def __init__(self, project_id=None, name=None, metadata=None, integration_id=None, data_info=None, ct_info=None, skip_validation=None, agent_id=None):  # noqa: E501
        """ProjectIdUuidDatasetBody - a model defined in Swagger"""  # noqa: E501
        self._project_id = None
        self._name = None
        self._metadata = None
        self._integration_id = None
        self._data_info = None
        self._ct_info = None
        self._skip_validation = None
        self._agent_id = None
        self.discriminator = None
        if project_id is not None:
            self.project_id = project_id
        self.name = name
        if metadata is not None:
            self.metadata = metadata
        if integration_id is not None:
            self.integration_id = integration_id
        if data_info is not None:
            self.data_info = data_info
        if ct_info is not None:
            self.ct_info = ct_info
        if skip_validation is not None:
            self.skip_validation = skip_validation
        if agent_id is not None:
            self.agent_id = agent_id

    @property
    def project_id(self):
        """Gets the project_id of this ProjectIdUuidDatasetBody.  # noqa: E501

        Uniquely specifies a Project.  # noqa: E501

        :return: The project_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: object
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ProjectIdUuidDatasetBody.

        Uniquely specifies a Project.  # noqa: E501

        :param project_id: The project_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: object
        """

        self._project_id = project_id

    @property
    def name(self):
        """Gets the name of this ProjectIdUuidDatasetBody.  # noqa: E501

        Unique name of the Dataset.  # noqa: E501

        :return: The name of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ProjectIdUuidDatasetBody.

        Unique name of the Dataset.  # noqa: E501

        :param name: The name of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def metadata(self):
        """Gets the metadata of this ProjectIdUuidDatasetBody.  # noqa: E501


        :return: The metadata of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: RegistryMetadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this ProjectIdUuidDatasetBody.


        :param metadata: The metadata of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: RegistryMetadata
        """

        self._metadata = metadata

    @property
    def integration_id(self):
        """Gets the integration_id of this ProjectIdUuidDatasetBody.  # noqa: E501


        :return: The integration_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._integration_id

    @integration_id.setter
    def integration_id(self, integration_id):
        """Sets the integration_id of this ProjectIdUuidDatasetBody.


        :param integration_id: The integration_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: RimeUUID
        """

        self._integration_id = integration_id

    @property
    def data_info(self):
        """Gets the data_info of this ProjectIdUuidDatasetBody.  # noqa: E501


        :return: The data_info of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: RegistryDataInfo
        """
        return self._data_info

    @data_info.setter
    def data_info(self, data_info):
        """Sets the data_info of this ProjectIdUuidDatasetBody.


        :param data_info: The data_info of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: RegistryDataInfo
        """

        self._data_info = data_info

    @property
    def ct_info(self):
        """Gets the ct_info of this ProjectIdUuidDatasetBody.  # noqa: E501


        :return: The ct_info of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: DatasetCTInfo
        """
        return self._ct_info

    @ct_info.setter
    def ct_info(self, ct_info):
        """Sets the ct_info of this ProjectIdUuidDatasetBody.


        :param ct_info: The ct_info of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: DatasetCTInfo
        """

        self._ct_info = ct_info

    @property
    def skip_validation(self):
        """Gets the skip_validation of this ProjectIdUuidDatasetBody.  # noqa: E501

        The parameter is deprecated since 2.7, and does not have any effect. Will always validate the dataset you are registering. Validation ensures that the dataset is valid for Robust Intelligence's systems.  # noqa: E501

        :return: The skip_validation of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: bool
        """
        return self._skip_validation

    @skip_validation.setter
    def skip_validation(self, skip_validation):
        """Sets the skip_validation of this ProjectIdUuidDatasetBody.

        The parameter is deprecated since 2.7, and does not have any effect. Will always validate the dataset you are registering. Validation ensures that the dataset is valid for Robust Intelligence's systems.  # noqa: E501

        :param skip_validation: The skip_validation of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: bool
        """

        self._skip_validation = skip_validation

    @property
    def agent_id(self):
        """Gets the agent_id of this ProjectIdUuidDatasetBody.  # noqa: E501


        :return: The agent_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :rtype: RimeUUID
        """
        return self._agent_id

    @agent_id.setter
    def agent_id(self, agent_id):
        """Sets the agent_id of this ProjectIdUuidDatasetBody.


        :param agent_id: The agent_id of this ProjectIdUuidDatasetBody.  # noqa: E501
        :type: RimeUUID
        """

        self._agent_id = agent_id

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
        if issubclass(ProjectIdUuidDatasetBody, dict):
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
        if not isinstance(other, ProjectIdUuidDatasetBody):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
