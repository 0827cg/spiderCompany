#!/usr/bin/python3 
"""
 Author: cg
 Date: 2020/12/16 17:55
"""
import json
from utils import com_util


class Schema:
    name = None

    age = None


dict_value = {
    "name": "cse",
    "age": 10
}

str_value = '{"name":"是gua些","age":22, "sex": 1}'

# json.loads(dict_value, Schema.__class__)

schema_a = Schema()
schema_a.name = "的人hi"
schema_a.age = 18

# 对象转字典
dict_schema = schema_a.__dict__
print(dict_schema)
print(type(dict_schema))

# 字典转json字符串
json_schema = com_util.parse_to_json(dict_schema)
print(json_schema)
print(type(json_schema))

# 字典转json字符串
pre_json_scheam = com_util.parse_to_json(dict_schema, True)
print(pre_json_scheam)
print(type(pre_json_scheam))

schema_b = Schema()
for key, value in dict_value.items():
    if not hasattr(schema_b, key):
        continue
    print(key, value)
    schema_b.__setattr__(key, value)

print(schema_b)
print(schema_b.name)
print(schema_b.age)
print(type(schema_b))

# json字符串到dict
print(str_value)
print(type(str_value))
json_value = json.loads(str_value)
print(json_value)
print(type(json_value))

pretty_value = com_util.parse_to_json(str_value, True)
print(pretty_value)
print(type(pretty_value))

# json字符串转对象
schema = com_util.parse_to_obj(str_value, Schema)
print("json字符串转对象")
print(schema.__dict__)
print(type(schema))
print(schema.age)

print(schema.__class__ is Schema)

