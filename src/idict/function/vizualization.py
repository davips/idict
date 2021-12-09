import numpy
import numpy as np
import pandas


def X2histogram(col=0, input="X", output="histogram", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, 2.1, 1.6], [3.2, 3, 2], [8, 7, 3]])
    >>> X2histogram(X=X, col=1)
    {'histogram': [{'x': '(1.1, 1.59]', 'count': 0}, {'x': '(1.59, 2.08]', 'count': 0}, {'x': '(2.08, 2.57]', 'count': 1}, {'x': '(2.57, 3.06]', 'count': 1}, {'x': '(3.06, 3.55]', 'count': 0}, {'x': '(3.55, 4.04]', 'count': 0}, {'x': '(4.04, 4.53]', 'count': 0}, {'x': '(4.53, 5.02]', 'count': 0}, {'x': '(5.02, 5.51]', 'count': 0}, {'x': '(5.51, 6.0]', 'count': 0}, {'x': '(6.0, 6.49]', 'count': 0}, {'x': '(6.49, 6.98]', 'count': 0}, {'x': '(6.98, 7.47]', 'count': 1}, {'x': '(7.47, 7.96]', 'count': 0}], '_history': Ellipsis}
    """
    X = kwargs[input]
    cut = list(map(float, X[:, col]))
    maximum = max(cut)
    minimum = min(cut)
    step = (maximum - minimum) / 10
    ranges = np.arange(minimum - 1, maximum + 1, step)

    df = pandas.DataFrame(cut)
    df2 = df.groupby(pandas.cut(cut, ranges)).count()
    result = [{"x": str(k), "count": v} for k, v in df2.to_dict()[0].items()]
    return {output: result, "_history": ...}


def Xy2scatterplot(colx=0, coly=1, Xin="X", yin="y", output="scatterplot", **kwargs):
    """
    >>> import numpy as np
    >>> X = np.array([[0, 2.1, 1.6], [3.2, 3, 2], [8, 7, 3]])
    >>> X2histogram(X=X, col=1)
    {'histogram': [{'x': '(1.1, 1.59]', 'count': 0}, {'x': '(1.59, 2.08]', 'count': 0}, {'x': '(2.08, 2.57]', 'count': 1}, {'x': '(2.57, 3.06]', 'count': 1}, {'x': '(3.06, 3.55]', 'count': 0}, {'x': '(3.55, 4.04]', 'count': 0}, {'x': '(4.04, 4.53]', 'count': 0}, {'x': '(4.53, 5.02]', 'count': 0}, {'x': '(5.02, 5.51]', 'count': 0}, {'x': '(5.51, 6.0]', 'count': 0}, {'x': '(6.0, 6.49]', 'count': 0}, {'x': '(6.49, 6.98]', 'count': 0}, {'x': '(6.98, 7.47]', 'count': 1}, {'x': '(7.47, 7.96]', 'count': 0}], '_history': Ellipsis}
    """
    X = kwargs[Xin]
    y = kwargs[yin]
    result = []
    for m in numpy.unique(y):
        inner = []
        for k in range(len(X)):
            left = m if isinstance(m, str) else str(float(m))
            if isinstance(y[k], str):
                right = y[k]
            else:
                right = str(float(y[k]))
            if left == right:
                inner.append(
                    {
                        "x": float(X[k, colx]),
                        "y": float(X[k, coly]),
                    }
                )
        result.append({"id": m, "data": inner})
    return {output: result, "_history": ...}


X2histogram.metadata = {
    "id": "-----------------------------X2histogram",
    "name": "X2histogram",
    "description": "Generate a histogram for the specified column of a field.",
    "parameters": ...,
    "code": ...,
}
Xy2scatterplot.metadata = {
    "id": "--------------------------Xy2scatterplot",
    "name": "Xy2scatterplot",
    "description": "Generate a scatterplot for the specified two columns of a field.",
    "parameters": ...,
    "code": ...,
}
