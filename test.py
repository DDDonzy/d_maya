from dataclasses import dataclass
import random

import yaml

import marshal
@dataclass
class Person:
    name: str
    age: int
    height: list


@dataclass
class Member:
    test: Person


# 示例对象
person = Person(name="Alice", age=30, height=list(random.random() for i in range(100_0000)))
m = Member(test=person)

import time
s = time.time()
# 序列化
# m_json = m.to_json()
# pickle.dumps(m)
# marshal.dumps(m)
# data = dill.dumps(m)
# print(dill.loads(data))
with open(r"t:/output.yaml", "w") as f:
    yaml.dump(m, f)
print(time.time() - s)

# # 反序列化
# m_loaded = Member.from_json(m_json)
