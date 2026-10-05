from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def build_preprocessor(X):
    """
    Creates the preprocessing pipeline used before model training.

    Numerical features are standardized.
    Categorical features are one-hot encoded.
    """

    categorical_columns = X.select_dtypes(
        include="object"
    ).columns.tolist()

    numerical_columns = X.select_dtypes(
        exclude="object"
    ).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                StandardScaler(),
                numerical_columns
            ),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_columns
            )
        ]
    )

    return preprocessor