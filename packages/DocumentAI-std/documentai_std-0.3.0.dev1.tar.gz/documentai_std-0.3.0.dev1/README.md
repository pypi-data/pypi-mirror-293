# DocumentAI-std

[//]: # ( TODO: Write a well presented documentation)
**DocumentAI-std** is a Python library designed to facilitate and standardize document analysis and processing tasks. It offers functionality for handling document elements, performing optical character recognition (OCR), and managing document datasets.

## Installation

To install **DocumentAI-std**, you can follow these steps:

1. Clone the repository from GitHub:

```sh
pip install DocumentAI-std
```


## Example of Usage

Here's an example demonstrating how to use the `Wildreceipt` dataset:

```python
from DocumentAI_std.datasets import Wildreceipt

# Define train and test sets
train_set = Wildreceipt(
    train=True,
    img_folder="/path/to/train/images/",
    label_path="/path/to/train/annotations.txt",
)
test_set = Wildreceipt(
    train=False,
    img_folder="/path/to/test/images/",
    label_path="/path/to/test/annotations.txt",
)

# Assert the number of data samples in train and test sets
assert len(train_set.data) == 1267
assert len(test_set.data) == 472
```

In the above example:
- We import the `Wildreceipt` dataset from the DocumentAI_std library.
- We create train and test dataset instances, specifying the paths to image folders and annotation files.
- We assert that the number of data samples in the train and test sets matches the expected counts.