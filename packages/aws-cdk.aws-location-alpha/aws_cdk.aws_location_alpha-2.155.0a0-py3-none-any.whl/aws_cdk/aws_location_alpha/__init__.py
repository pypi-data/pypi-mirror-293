r'''
# AWS::Location Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

Amazon Location Service lets you add location data and functionality to applications, which
includes capabilities such as maps, points of interest, geocoding, routing, geofences, and
tracking. Amazon Location provides location-based services (LBS) using high-quality data from
global, trusted providers Esri and HERE. With affordable data, tracking and geofencing
capabilities, and built-in metrics for health monitoring, you can build sophisticated
location-enabled applications.

## Place Index

A key function of Amazon Location Service is the ability to search the geolocation information.
Amazon Location provides this functionality via the Place index resource. The place index includes
which [data provider](https://docs.aws.amazon.com/location/latest/developerguide/what-is-data-provider.html)
to use for the search.

To create a place index, define a `PlaceIndex`:

```python
location.PlaceIndex(self, "PlaceIndex",
    place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
    data_source=location.DataSource.HERE
)
```

Use the `grant()` or `grantSearch()` method to grant the given identity permissions to perform actions
on the place index:

```python
# role: iam.Role


place_index = location.PlaceIndex(self, "PlaceIndex")
place_index.grant_search(role)
```

## Geofence Collection

Geofence collection resources allow you to store and manage geofences—virtual boundaries on a map.
You can evaluate locations against a geofence collection resource and get notifications when the location
update crosses the boundary of any of the geofences in the geofence collection.

```python
# key: kms.Key


location.GeofenceCollection(self, "GeofenceCollection",
    geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
    kms_key=key
)
```

Use the `grant()` or `grantRead()` method to grant the given identity permissions to perform actions
on the geofence collection:

```python
# role: iam.Role


geofence_collection = location.GeofenceCollection(self, "GeofenceCollection",
    geofence_collection_name="MyGeofenceCollection"
)

geofence_collection.grant_read(role)
```
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.DataSource")
class DataSource(enum.Enum):
    '''(experimental) Data source for a place index.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    ESRI = "ESRI"
    '''(experimental) Esri.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/esri.html
    :stability: experimental
    '''
    HERE = "HERE"
    '''(experimental) HERE.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/HERE.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.GeofenceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "geofence_collection_name": "geofenceCollectionName",
        "kms_key": "kmsKey",
    },
)
class GeofenceCollectionProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        geofence_collection_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) Properties for a geofence collection.

        :param description: (experimental) A description for the geofence collection. Default: - no description
        :param geofence_collection_name: (experimental) A name for the geofence collection. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param kms_key: (experimental) The customer managed to encrypt your data. Default: - Use an AWS managed key

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # key: kms.Key
            
            
            location.GeofenceCollection(self, "GeofenceCollection",
                geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
                kms_key=key
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdd3197c12b6d89ece6dfce72294a7f00d61e7a28da5918141a6d8e57c35fc5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument geofence_collection_name", value=geofence_collection_name, expected_type=type_hints["geofence_collection_name"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if geofence_collection_name is not None:
            self._values["geofence_collection_name"] = geofence_collection_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the geofence collection.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def geofence_collection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the geofence collection.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("geofence_collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The customer managed to encrypt your data.

        :default: - Use an AWS managed key

        :see: https://docs.aws.amazon.com/location/latest/developerguide/encryption-at-rest.html
        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GeofenceCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IGeofenceCollection")
class IGeofenceCollection(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Geofence Collection.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        :attribute: Arn, CollectionArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IGeofenceCollectionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Geofence Collection.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IGeofenceCollection"

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        :attribute: Arn, CollectionArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionArn"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGeofenceCollection).__jsii_proxy_class__ = lambda : _IGeofenceCollectionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-location-alpha.IPlaceIndex")
class IPlaceIndex(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPlaceIndexProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Place Index.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-location-alpha.IPlaceIndex"

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        :attribute: Arn,IndexArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPlaceIndex).__jsii_proxy_class__ = lambda : _IPlaceIndexProxy


@jsii.enum(jsii_type="@aws-cdk/aws-location-alpha.IntendedUse")
class IntendedUse(enum.Enum):
    '''(experimental) Intend use for the results of an operation.

    :stability: experimental
    '''

    SINGLE_USE = "SINGLE_USE"
    '''(experimental) The results won't be stored.

    :stability: experimental
    '''
    STORAGE = "STORAGE"
    '''(experimental) The result can be cached or stored in a database.

    :stability: experimental
    '''


@jsii.implements(IPlaceIndex)
class PlaceIndex(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndex",
):
    '''(experimental) A Place Index.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/places-concepts.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        location.PlaceIndex(self, "PlaceIndex",
            place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
            data_source=location.DataSource.HERE
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_source: typing.Optional[DataSource] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional[IntendedUse] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PlaceIndexProps(
            data_source=data_source,
            description=description,
            intended_use=intended_use,
            place_index_name=place_index_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPlaceIndexArn")
    @builtins.classmethod
    def from_place_index_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        place_index_arn: builtins.str,
    ) -> IPlaceIndex:
        '''(experimental) Use an existing place index by ARN.

        :param scope: -
        :param id: -
        :param place_index_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_arn", value=place_index_arn, expected_type=type_hints["place_index_arn"])
        return typing.cast(IPlaceIndex, jsii.sinvoke(cls, "fromPlaceIndexArn", [scope, id, place_index_arn]))

    @jsii.member(jsii_name="fromPlaceIndexName")
    @builtins.classmethod
    def from_place_index_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        place_index_name: builtins.str,
    ) -> IPlaceIndex:
        '''(experimental) Use an existing place index by name.

        :param scope: -
        :param id: -
        :param place_index_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        return typing.cast(IPlaceIndex, jsii.sinvoke(cls, "fromPlaceIndexName", [scope, id, place_index_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this place index.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantSearch")
    def grant_search(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to search using this index.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantSearch", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="placeIndexArn")
    def place_index_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the place index resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexArn"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexCreateTime")
    def place_index_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexName")
    def place_index_name(self) -> builtins.str:
        '''(experimental) The name of the place index.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexName"))

    @builtins.property
    @jsii.member(jsii_name="placeIndexUpdateTime")
    def place_index_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the place index resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "placeIndexUpdateTime"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-location-alpha.PlaceIndexProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_source": "dataSource",
        "description": "description",
        "intended_use": "intendedUse",
        "place_index_name": "placeIndexName",
    },
)
class PlaceIndexProps:
    def __init__(
        self,
        *,
        data_source: typing.Optional[DataSource] = None,
        description: typing.Optional[builtins.str] = None,
        intended_use: typing.Optional[IntendedUse] = None,
        place_index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a place index.

        :param data_source: (experimental) Data source for the place index. Default: DataSource.ESRI
        :param description: (experimental) A description for the place index. Default: - no description
        :param intended_use: (experimental) Intend use for the results of an operation. Default: IntendedUse.SINGLE_USE
        :param place_index_name: (experimental) A name for the place index. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            location.PlaceIndex(self, "PlaceIndex",
                place_index_name="MyPlaceIndex",  # optional, defaults to a generated name
                data_source=location.DataSource.HERE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae)
            check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument intended_use", value=intended_use, expected_type=type_hints["intended_use"])
            check_type(argname="argument place_index_name", value=place_index_name, expected_type=type_hints["place_index_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_source is not None:
            self._values["data_source"] = data_source
        if description is not None:
            self._values["description"] = description
        if intended_use is not None:
            self._values["intended_use"] = intended_use
        if place_index_name is not None:
            self._values["place_index_name"] = place_index_name

    @builtins.property
    def data_source(self) -> typing.Optional[DataSource]:
        '''(experimental) Data source for the place index.

        :default: DataSource.ESRI

        :stability: experimental
        '''
        result = self._values.get("data_source")
        return typing.cast(typing.Optional[DataSource], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the place index.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def intended_use(self) -> typing.Optional[IntendedUse]:
        '''(experimental) Intend use for the results of an operation.

        :default: IntendedUse.SINGLE_USE

        :stability: experimental
        '''
        result = self._values.get("intended_use")
        return typing.cast(typing.Optional[IntendedUse], result)

    @builtins.property
    def place_index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the place index.

        Must be between 1 and 100 characters and contain only alphanumeric characters,
        hyphens, periods and underscores.

        :default: - A name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("place_index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlaceIndexProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IGeofenceCollection)
class GeofenceCollection(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-location-alpha.GeofenceCollection",
):
    '''(experimental) A Geofence Collection.

    :see: https://docs.aws.amazon.com/location/latest/developerguide/geofence-tracker-concepts.html#geofence-overview
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # key: kms.Key
        
        
        location.GeofenceCollection(self, "GeofenceCollection",
            geofence_collection_name="MyGeofenceCollection",  # optional, defaults to a generated name
            kms_key=key
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        geofence_collection_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) A description for the geofence collection. Default: - no description
        :param geofence_collection_name: (experimental) A name for the geofence collection. Must be between 1 and 100 characters and contain only alphanumeric characters, hyphens, periods and underscores. Default: - A name is automatically generated
        :param kms_key: (experimental) The customer managed to encrypt your data. Default: - Use an AWS managed key

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46515b575b3aea76a1e7b6fb58cf0b2fb74b8eab224b06940310470f76183f7c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GeofenceCollectionProps(
            description=description,
            geofence_collection_name=geofence_collection_name,
            kms_key=kms_key,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGeofenceCollectionArn")
    @builtins.classmethod
    def from_geofence_collection_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        geofence_collection_arn: builtins.str,
    ) -> IGeofenceCollection:
        '''(experimental) Use an existing geofence collection by ARN.

        :param scope: -
        :param id: -
        :param geofence_collection_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb916f69d0fe4399d9278aecbd25559dc350b950a717f4bd2cbd4262712301a0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument geofence_collection_arn", value=geofence_collection_arn, expected_type=type_hints["geofence_collection_arn"])
        return typing.cast(IGeofenceCollection, jsii.sinvoke(cls, "fromGeofenceCollectionArn", [scope, id, geofence_collection_arn]))

    @jsii.member(jsii_name="fromGeofenceCollectionName")
    @builtins.classmethod
    def from_geofence_collection_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        geofence_collection_name: builtins.str,
    ) -> IGeofenceCollection:
        '''(experimental) Use an existing geofence collection by name.

        :param scope: -
        :param id: -
        :param geofence_collection_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96d0b73947b903aff64888db96cb07d68b0f8e10dea23e7b62d37c937970f738)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument geofence_collection_name", value=geofence_collection_name, expected_type=type_hints["geofence_collection_name"])
        return typing.cast(IGeofenceCollection, jsii.sinvoke(cls, "fromGeofenceCollectionName", [scope, id, geofence_collection_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given principal identity permissions to perform the actions on this geofence collection.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2b0b7d842c9c09abfd524da8f0b754d8bd5dac77b3ac3c48fa2e42486e2816)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity permissions to read this geofence collection.

        :param grantee: -

        :see: https://docs.aws.amazon.com/location/latest/developerguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-read-only-geofences
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a75e3f479665495211d879861c613331d0480d70c6adba492329ff9bc728ba0d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionArn")
    def geofence_collection_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the geofence collection resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionArn"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionCreateTime")
    def geofence_collection_create_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the geofence collection resource was created in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionCreateTime"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionName")
    def geofence_collection_name(self) -> builtins.str:
        '''(experimental) The name of the geofence collection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionName"))

    @builtins.property
    @jsii.member(jsii_name="geofenceCollectionUpdateTime")
    def geofence_collection_update_time(self) -> builtins.str:
        '''(experimental) The timestamp for when the geofence collection resource was last updated in ISO 8601 format.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "geofenceCollectionUpdateTime"))


__all__ = [
    "DataSource",
    "GeofenceCollection",
    "GeofenceCollectionProps",
    "IGeofenceCollection",
    "IPlaceIndex",
    "IntendedUse",
    "PlaceIndex",
    "PlaceIndexProps",
]

publication.publish()

def _typecheckingstub__bbdd3197c12b6d89ece6dfce72294a7f00d61e7a28da5918141a6d8e57c35fc5(
    *,
    description: typing.Optional[builtins.str] = None,
    geofence_collection_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45352af3f6c713374f537c829e98f8db51c9684d0ccc55eedcc24f34b4115a7d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248ee08bccad0771877a2fcc90a9b08d64668a1cf797c90deb8c53fec79af85d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8d45231ce3a808cab553413e12ee6462eb276374dc71795aae0d1b4cbc7651(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    place_index_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f4422a489b304c7bbc9bfabd28b7282eb0ff8e5a625351b01c27528783eef2(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d5a407a04ad6cfe5d7ad704c60c4485d954e37151f87d42b4a0f8aae3e8fcf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46e973a0eacea346fe0253fb892d398121998cd91fd16cfdf5bb8eef740a62ae(
    *,
    data_source: typing.Optional[DataSource] = None,
    description: typing.Optional[builtins.str] = None,
    intended_use: typing.Optional[IntendedUse] = None,
    place_index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46515b575b3aea76a1e7b6fb58cf0b2fb74b8eab224b06940310470f76183f7c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    geofence_collection_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb916f69d0fe4399d9278aecbd25559dc350b950a717f4bd2cbd4262712301a0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    geofence_collection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96d0b73947b903aff64888db96cb07d68b0f8e10dea23e7b62d37c937970f738(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    geofence_collection_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2b0b7d842c9c09abfd524da8f0b754d8bd5dac77b3ac3c48fa2e42486e2816(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75e3f479665495211d879861c613331d0480d70c6adba492329ff9bc728ba0d(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass
