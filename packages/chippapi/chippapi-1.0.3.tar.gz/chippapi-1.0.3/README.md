# ChippAPI
-> This is a simple python wrapper for [Chipp](https://chipp.ai/).

## Installation
```bash
pip install -i https://test.pypi.org/simple/ chippapi==1.0.3
```

## Usage
```python
import chippapi

chippapi.api_key = "YOUR_API_KEY"
chippapi.id = "YOUR_ID"

response = chippapi.chat(prompt="Hello, how are you?")
print(response)
```

## License
-> This project is licensed under the MIT license - see the [LICENSE](https://opensource.org/license/mit) for details.

