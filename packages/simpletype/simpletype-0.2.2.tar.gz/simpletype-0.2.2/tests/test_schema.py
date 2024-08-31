# -*- coding: utf-8 -*-

import pytest
import polars as pl
from simpletype.schema import (
    TypeNameEnum,
    AwsGlueTypeEnum,
    SparkTypeEnum,
    Integer,
    TinyInteger,
    SmallInteger,
    BigInteger,
    Float,
    Double,
    Decimal,
    String,
    Binary,
    Bool,
    Null,
    Datetime,
    Set,
    List,
    Struct,
    json_type_to_simple_type,
    polars_type_to_simple_type,
)


def test_integer():
    integer_type = json_type_to_simple_type({"type": TypeNameEnum.int})
    assert integer_type.to_polars() == pl.Int32()
    assert integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert integer_type.to_glue() == AwsGlueTypeEnum.bigint
    assert integer_type.to_spark_string() == AwsGlueTypeEnum.bigint


def test_tiny_integer():
    tiny_integer_type = json_type_to_simple_type({"type": TypeNameEnum.tinyint})
    assert tiny_integer_type.to_polars() == pl.Int8()
    assert tiny_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert tiny_integer_type.to_glue() == AwsGlueTypeEnum.tinyint
    assert tiny_integer_type.to_spark_string() == SparkTypeEnum.tinyint


def test_small_integer():
    small_integer_type = json_type_to_simple_type({"type": TypeNameEnum.smallint})
    assert small_integer_type.to_polars() == pl.Int16()
    assert small_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert small_integer_type.to_glue() == AwsGlueTypeEnum.smallint
    assert small_integer_type.to_spark_string() == SparkTypeEnum.smallint


def test_big_integer():
    big_integer_type = json_type_to_simple_type({"type": TypeNameEnum.bigint})
    assert big_integer_type.to_polars() == pl.Int64()
    assert big_integer_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert big_integer_type.to_glue() == AwsGlueTypeEnum.bigint
    assert big_integer_type.to_spark_string() == SparkTypeEnum.bigint


def test_float():
    float_type = json_type_to_simple_type({"type": TypeNameEnum.float})
    assert float_type.to_polars() == pl.Float32()
    assert float_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert float_type.to_glue() == AwsGlueTypeEnum.float
    assert float_type.to_spark_string() == SparkTypeEnum.float


def test_double():
    double_type = json_type_to_simple_type({"type": TypeNameEnum.double})
    assert double_type.to_polars() == pl.Float64()
    assert double_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert double_type.to_glue() == AwsGlueTypeEnum.double
    assert double_type.to_spark_string() == SparkTypeEnum.double


def test_decimal():
    decimal_type = json_type_to_simple_type({"type": TypeNameEnum.decimal})
    assert decimal_type.to_polars() == pl.Decimal()
    assert decimal_type.to_dynamodb_json_polars() == pl.Struct({"N": pl.Utf8()})
    assert decimal_type.to_glue() == AwsGlueTypeEnum.decimal
    assert decimal_type.to_spark_string() == SparkTypeEnum.decimal


def test_string():
    string_type = json_type_to_simple_type({"type": TypeNameEnum.str})
    assert string_type.to_polars() == pl.Utf8()
    assert string_type.to_dynamodb_json_polars() == pl.Struct({"S": pl.Utf8()})
    assert string_type.to_glue() == AwsGlueTypeEnum.string
    assert string_type.to_spark_string() == SparkTypeEnum.string
    assert string_type.default_for_null == ""


def test_binary():
    binary_type = json_type_to_simple_type({"type": TypeNameEnum.bin})
    assert binary_type.to_polars() == pl.Binary()
    assert binary_type.to_dynamodb_json_polars() == pl.Struct({"B": pl.Utf8()})
    assert binary_type.to_glue() == AwsGlueTypeEnum.binary
    assert binary_type.to_spark_string() == SparkTypeEnum.binary
    assert binary_type.default_for_null == b""


def test_bool():
    bool_type = json_type_to_simple_type({"type": TypeNameEnum.bool})
    assert bool_type.to_polars() == pl.Boolean()
    assert bool_type.to_dynamodb_json_polars() == pl.Struct({"BOOL": pl.Boolean()})
    assert bool_type.to_glue() == AwsGlueTypeEnum.boolean
    assert bool_type.to_spark_string() == SparkTypeEnum.boolean


def test_null():
    null_type = json_type_to_simple_type({"type": TypeNameEnum.null})
    assert null_type.to_polars() == pl.Null()
    assert null_type.to_dynamodb_json_polars() == pl.Struct({"NULL": pl.Boolean()})
    assert null_type.to_glue() == AwsGlueTypeEnum.string
    assert null_type.to_spark_string() == SparkTypeEnum.null
    assert null_type.default_for_null is None


def test_datetime():
    datetime_type = json_type_to_simple_type({"type": TypeNameEnum.datetime})
    assert datetime_type.to_polars() == pl.Datetime()
    assert datetime_type.to_dynamodb_json_polars() == pl.Struct({"S": pl.Utf8()})
    assert datetime_type.to_glue() == AwsGlueTypeEnum.timestamp
    assert datetime_type.to_spark_string() == SparkTypeEnum.timestamp


def test_json_type_to_simple_type():
    # fmt: off
    assert json_type_to_simple_type({"type": "int"}) == Integer()
    assert json_type_to_simple_type({"type": "int", "default_for_null": -999}) == Integer(default_for_null=-999)
    assert json_type_to_simple_type({"type": "float"}) == Float()
    assert json_type_to_simple_type({"type": "float", "default_for_null": -3.14}) == Float(default_for_null=-3.14)
    assert json_type_to_simple_type({"type": "str"}) == String()
    assert json_type_to_simple_type({"type": "str", "default_for_null": "UNKNOWN"}) == String(default_for_null="UNKNOWN")
    assert json_type_to_simple_type({"type": "bin"}) == Binary()
    assert json_type_to_simple_type({"type": "bin", "default_for_null": b"hello"}) == Binary(default_for_null=b"hello")
    assert json_type_to_simple_type({"type": "bool"}) == Bool()
    assert json_type_to_simple_type({"type": "bool", "default_for_null": False}) == Bool(default_for_null=False)
    assert json_type_to_simple_type({"type": "null"}) == Null()
    assert json_type_to_simple_type({"type": "null", "default_for_null": None}) == Null(default_for_null=None)

    json_type = {"type": "set", "itype": {"type": "int"}}
    assert json_type_to_simple_type(json_type) == Set(Integer())
    json_type = {"type": "set", "itype": {"type": "int"}, "default_for_null": [1, 2, 3]}
    assert json_type_to_simple_type(json_type) == Set(Integer(), default_for_null=[1, 2, 3])

    json_type = {"type": "set", "itype": {"type": "float"}}
    assert json_type_to_simple_type(json_type) == Set(Float())

    json_type = {"type": "set", "itype": {"type": "str"}}
    assert json_type_to_simple_type(json_type) == Set(String())

    json_type = {"type": "set", "itype": {"type": "bin"}}
    assert json_type_to_simple_type(json_type) == Set(Binary())

    json_type = {"type": "list", "itype": {"type": "int"}}
    assert json_type_to_simple_type(json_type) == List(Integer())
    json_type = {"type": "list", "itype": {"type": "int"}, "default_for_null": [1, 2, 3]}
    assert json_type_to_simple_type(json_type) == List(Integer(), default_for_null=[1, 2, 3])

    json_type = {"type": "list", "itype": {"type": "float"}}
    assert json_type_to_simple_type(json_type) == List(Float())

    json_type = {"type": "list", "itype": {"type": "str"}}
    assert json_type_to_simple_type(json_type) == List(String())

    json_type = {"type": "list", "itype": {"type": "bin"}}
    assert json_type_to_simple_type(json_type) == List(Binary())

    json_type = {
        "type": "list",
        "itype": {"type": "struct", "fields": {"a_int": {"type": "int"}}},
    }
    assert json_type_to_simple_type(json_type) == List(Struct({"a_int": Integer()}))

    json_type = {
        "type": "struct",
        "fields": {
            "a_int": {"type": "int"},
            "a_str": {"type": "str"},
            "a_list_of_int": {"type": "list", "itype": {"type": "int"}},
            "a_set_of_str": {"type": "set", "itype": {"type": "str"}},
        },
    }
    assert json_type_to_simple_type(json_type) == Struct(
        {
            "a_int": Integer(),
            "a_str": String(),
            "a_list_of_int": List(Integer()),
            "a_set_of_str": Set(String()),
        }
    )
    # fmt: on


def test_polars_type_to_simple_type():
    # Test integer types
    assert isinstance(polars_type_to_simple_type(pl.Int32()), Integer)
    assert isinstance(polars_type_to_simple_type(pl.Int8()), TinyInteger)
    assert isinstance(polars_type_to_simple_type(pl.Int16()), SmallInteger)
    assert isinstance(polars_type_to_simple_type(pl.Int64()), BigInteger)

    # Test float types
    assert isinstance(polars_type_to_simple_type(pl.Float32()), Float)
    assert isinstance(polars_type_to_simple_type(pl.Float64()), Double)

    # Test Decimal
    assert isinstance(polars_type_to_simple_type(pl.Decimal()), Decimal)

    # Test String
    assert isinstance(polars_type_to_simple_type(pl.String()), String)

    # Test Binary
    assert isinstance(polars_type_to_simple_type(pl.Binary()), Binary)

    # Test Boolean
    assert isinstance(polars_type_to_simple_type(pl.Boolean()), Bool)

    # Test Null
    assert isinstance(polars_type_to_simple_type(pl.Null()), Null)

    # Test Datetime
    assert isinstance(polars_type_to_simple_type(pl.Datetime()), Datetime)

    # Test List
    list_type = polars_type_to_simple_type(pl.List(pl.Int32()))
    assert isinstance(list_type, List)
    assert isinstance(list_type.itype, Integer)

    # Test nested List
    nested_list_type = polars_type_to_simple_type(pl.List(pl.List(pl.String())))
    assert isinstance(nested_list_type, List)
    assert isinstance(nested_list_type.itype, List)
    assert isinstance(nested_list_type.itype.itype, String)

    # Test Struct
    struct_type = polars_type_to_simple_type(
        pl.Struct([pl.Field("a", pl.Int32()), pl.Field("b", pl.String())])
    )
    assert isinstance(struct_type, Struct)
    assert isinstance(struct_type.fields["a"], Integer)
    assert isinstance(struct_type.fields["b"], String)

    # Test nested Struct
    nested_struct_type = polars_type_to_simple_type(
        pl.Struct(
            [
                pl.Field("x", pl.Int32()),
                pl.Field("y", pl.Struct([pl.Field("z", pl.String())])),
            ]
        )
    )
    assert isinstance(nested_struct_type, Struct)
    assert isinstance(nested_struct_type.fields["x"], Integer)
    assert isinstance(nested_struct_type.fields["y"], Struct)
    assert isinstance(nested_struct_type.fields["y"].fields["z"], String)

    # Test unsupported type
    class UnsupportedType(pl.DataType):
        pass

    with pytest.raises(NotImplementedError):
        polars_type_to_simple_type(UnsupportedType)


if __name__ == "__main__":
    from simpletype.tests import run_cov_test

    run_cov_test(__file__, "simpletype.schema", preview=False)
