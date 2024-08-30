# Condy

Condy is a Python library that provides easy access to embeddings from a specific API.

## Installation

You can install Condy using pip:

```
pip install condy
```

## Usage

Here's a simple example of how to use Condy:

```python
from condy import get_embeddings

text = "Hello, world!"
embeddings = get_embeddings(text)
print(embeddings)
```