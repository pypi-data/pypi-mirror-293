# algolearn - Custom Standard Library

Custom implementation of standard library to help learn Data Structures, Algorithms and Leetcode.

## Core Features

- Implement Array
- Implement LinkedList
- Implement HashMap
- Implement Heap
- Implement Stack
- Implement Tree

## Future Features

- Use a build tool instead of running setup.py directly because this method is deprecated

## Phases

## Milestones

## User stories

## System requirements

For manual publishing to PyPi: pip, wheel, twine, setuptools

## Installation

```bash
pip3 install algolearn
```

## Usage

```bash
python3 main.py
```

## Testing

```bash
python3 -m unittest -v tests/multiplication_tests.py
```

## Manually publishing to PyPi

```bash
pip install twine wheel setuptools
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```

## Contributing

## License
