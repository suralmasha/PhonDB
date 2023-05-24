# Phonetic Diversity Metric
This is metric of phonetic diversity and balance of textual data. 
It is supposed to be used while preparation or selection of training data for voice AI models. 
However other purposes are possible.

# Installation

```
pip install git+https://github.com/suralmasha/PhDB
```

# Usage

Define the path to your dataset. It can be a `txt` file or a folder with `txt` files 
(in the example - `data_path`). 
Pass it to the `get_window_coefficient()` function.

```
from phonetic_diversity import get_coefficient

data_path = r"C:\natasha_dataset\marks.txt"
res = get_window_coefficient(data_path)
print(res)
```

It will return a weighted coefficient 
of phonetic diversity and balance of your textual data counted by the floating window 
(size - **50 tokens**) in a `float` format. You can change the size of the window 
by using parameter `window_length`.

```
res = get_window_coefficient(data_path, window_length=20)
print(res)
```

You can also get a coefficient of phonetic diversity and balance for the full text 
by using `get_full_coefficient()` function.

```
from phonetic_diversity import get_coefficient

data_path = r"C:\natasha_dataset\marks.txt"
res = get_full_coefficient(data_path)
print(res)
```

You can also find an example of using the framework in `example.py`.
