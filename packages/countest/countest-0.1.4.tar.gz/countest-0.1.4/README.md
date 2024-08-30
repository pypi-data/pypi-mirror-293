# CountEst

CountEst is a Python module containing the implementation of count-based estimators, i.e., supervised learning algorithms that make predictions based on the frequency or count of specific events, categories, or values within a dataset. These estimators operate under the assumption that the distribution of counts or frequencies provides valuable information for making predictions or inferences. The classifier is inspired by "Vastu Moolak Ganit" as described in a recent Indian philosophy [Madhyasth Darshan](https://madhyasth-darshan.info) by Late Shri A Nagraj.

Currently, we have implemented count-based classifier for categorical data. It operates by learning the distribution of category counts (i.e. the number of occurrences or frequency of each distinct category within a specific feature) within each class during the training phase. It then predicts class probabilities for unseen data based on the observed counts of categories within each feature, employing a voting mechanism to handle ties. 

## Installation

The package can be installed using `pip`:

```
pip install countest
```

## Dependencies

The installation dependency requirements are:

- Python (>= 3.9)
- NumPy (>= 1.5)
- Pandas (>= 1.1.5)
- Scikit-Learn (>=0.20.0)

These dependencies are automatically installed using the pip commands above.

## Examples

Here we show an example using the CategoricalCBC (i.e. count-based classifier for categorical data):

```
from countest.classifiers import CategoricalCBC
import numpy as np

X = np.random.choice(range(0,10),(100,6))
y = np.random.choice([0, 1], size=100)

estimator = CategoricalCBC()
estimator.fit(X, y)

print(estimator.predict([3, 6, 7, 2, 3, 4]))
```

## Changelog

See the [changelog](https://github.com/sanskriti-02/CountEst/blob/master/CHANGELOG.md) for a history of notable changes to CountEst.

## Development

This project is currently in its early stages. We're actively building and shaping it, and we welcome contributions from everyone, regardless of experience level. If you're interested in getting involved, we encourage you to explore the project and see where you can contribute! For specific contribution guidelines, visit our [GitHub page](https://github.com/sanskriti-02/CountEst). 