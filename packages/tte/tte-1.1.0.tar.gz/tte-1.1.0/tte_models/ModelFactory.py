from tte_models.ratio import RATIO
from tte_models.my_model import MyModel

RATIO_NAME = "RATIO"
MyModel_NAME = "MyModel"


def get_model(model_name: str, input_size: int):
    # TODO: allow for kwargs and checkpoint_dir
    model = None
    if model_name == RATIO_NAME:
        model = RATIO(input_size=input_size)
    elif model_name == MyModel_NAME:
        model = MyModel(input_size=input_size)

    return model
