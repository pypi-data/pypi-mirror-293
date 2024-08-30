# typed_singleton

A simple Python decorator library for creating singletons.

## Installation

```bash
pip install typed_singleton
```

## Usage

```python
from typed_singleton import Singleton


@Singleton
class SingletonClass:
    def __init__(self, my_value: int) -> None:
        self.my_value = my_value

    def get_my_awesome_value(self) -> int:
        return self.my_value

instance_1 = SingletonClass(1)
instance_2 = SingletonClass(2)
print(instance_1 is instance_2)  # True

print(instance_1.get_my_awesome_value())  # 1
print(instance_2.get_my_awesome_value())  # also 1
```
