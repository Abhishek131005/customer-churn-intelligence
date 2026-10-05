import pandas as pd

from src.models.predict import model


def get_feature_importance():
    preprocessor = model.named_steps["preprocessor"]
    classifier = model.named_steps["classifier"]

    feature_names = preprocessor.get_feature_names_out()
    coefficients = classifier.coef_[0]

    importance = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefficients
    })

    importance["importance"] = (
        importance["coefficient"].abs()
    )

    return importance.sort_values(
        "importance",
        ascending=False
    )