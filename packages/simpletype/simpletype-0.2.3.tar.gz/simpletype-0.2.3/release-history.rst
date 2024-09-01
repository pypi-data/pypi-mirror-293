.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add support to convert to pyspark type.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.3 (2024-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Add ``precision`` parameter to ``Float`` and ``Double`` type.


0.2.2 (2024-08-31)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a bug that the ``Set`` type cannot handle ``TinyInt``, ``SmallInt``, ``BigInt`` and ``Double``, ``Decimal`` item types.


0.2.1 (2024-08-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add the following public APIs:
    - ``simpletype.api.AwsDynamoDBTypeEnum``
    - ``simpletype.api.AwsGlueTypeEnum``
    - ``simpletype.api.SparkTypeEnum``
    - ``simpletype.api.polars_type_to_simple_type``


0.1.1 (2024-08-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public APIs:
    - ``simpletype.api.T_SIMPLE_SCHEMA``
    - ``simpletype.api.T_POLARS_SCHEMA``
    - ``simpletype.api.T_SPARK_SCHEMA``
    - ``simpletype.api.TypeAttrEnum``
    - ``simpletype.api.TypeNameEnum``
    - ``simpletype.api.BaseType``
    - ``simpletype.api.DATA_TYPE``
    - ``simpletype.api.Integer``
    - ``simpletype.api.TinyInteger``
    - ``simpletype.api.SmallInteger``
    - ``simpletype.api.BigInteger``
    - ``simpletype.api.Float``
    - ``simpletype.api.Double``
    - ``simpletype.api.Decimal``
    - ``simpletype.api.String``
    - ``simpletype.api.Binary``
    - ``simpletype.api.Bool``
    - ``simpletype.api.Null``
    - ``simpletype.api.Datetime``
    - ``simpletype.api.Set``
    - ``simpletype.api.List``
    - ``simpletype.api.Struct``
    - ``simpletype.api.json_type_to_simple_type``
