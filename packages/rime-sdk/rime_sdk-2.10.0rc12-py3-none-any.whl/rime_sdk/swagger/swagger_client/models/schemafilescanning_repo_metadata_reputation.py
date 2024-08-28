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

class SchemafilescanningRepoMetadataReputation(object):
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
        'downloads': 'str',
        'likes': 'str',
        'stars': 'str',
        'forks': 'str'
    }

    attribute_map = {
        'downloads': 'downloads',
        'likes': 'likes',
        'stars': 'stars',
        'forks': 'forks'
    }

    def __init__(self, downloads=None, likes=None, stars=None, forks=None):  # noqa: E501
        """SchemafilescanningRepoMetadataReputation - a model defined in Swagger"""  # noqa: E501
        self._downloads = None
        self._likes = None
        self._stars = None
        self._forks = None
        self.discriminator = None
        if downloads is not None:
            self.downloads = downloads
        if likes is not None:
            self.likes = likes
        if stars is not None:
            self.stars = stars
        if forks is not None:
            self.forks = forks

    @property
    def downloads(self):
        """Gets the downloads of this SchemafilescanningRepoMetadataReputation.  # noqa: E501

        The number of times the model repository has been downloaded.  # noqa: E501

        :return: The downloads of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :rtype: str
        """
        return self._downloads

    @downloads.setter
    def downloads(self, downloads):
        """Sets the downloads of this SchemafilescanningRepoMetadataReputation.

        The number of times the model repository has been downloaded.  # noqa: E501

        :param downloads: The downloads of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :type: str
        """

        self._downloads = downloads

    @property
    def likes(self):
        """Gets the likes of this SchemafilescanningRepoMetadataReputation.  # noqa: E501

        The number of times the model repository has been liked.  # noqa: E501

        :return: The likes of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :rtype: str
        """
        return self._likes

    @likes.setter
    def likes(self, likes):
        """Sets the likes of this SchemafilescanningRepoMetadataReputation.

        The number of times the model repository has been liked.  # noqa: E501

        :param likes: The likes of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :type: str
        """

        self._likes = likes

    @property
    def stars(self):
        """Gets the stars of this SchemafilescanningRepoMetadataReputation.  # noqa: E501

        The number of times the model repository has been starred.  # noqa: E501

        :return: The stars of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :rtype: str
        """
        return self._stars

    @stars.setter
    def stars(self, stars):
        """Sets the stars of this SchemafilescanningRepoMetadataReputation.

        The number of times the model repository has been starred.  # noqa: E501

        :param stars: The stars of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :type: str
        """

        self._stars = stars

    @property
    def forks(self):
        """Gets the forks of this SchemafilescanningRepoMetadataReputation.  # noqa: E501

        The number of times the model repository has been forked.  # noqa: E501

        :return: The forks of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :rtype: str
        """
        return self._forks

    @forks.setter
    def forks(self, forks):
        """Sets the forks of this SchemafilescanningRepoMetadataReputation.

        The number of times the model repository has been forked.  # noqa: E501

        :param forks: The forks of this SchemafilescanningRepoMetadataReputation.  # noqa: E501
        :type: str
        """

        self._forks = forks

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
        if issubclass(SchemafilescanningRepoMetadataReputation, dict):
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
        if not isinstance(other, SchemafilescanningRepoMetadataReputation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
