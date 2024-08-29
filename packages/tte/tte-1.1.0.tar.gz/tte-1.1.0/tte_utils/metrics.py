from lifelines.utils import concordance_index
import torch

from tte_utils.dataset import MyDataset


def calculate_ci(model, val_dataset) -> float:
    """
    Calculate the concordance index
    :param model: Subclass of AbstractNetwork
    :param val_dataset: Dataset
    :return:
    """
    model.network.eval()
    y_val = val_dataset.y.to(model.device)

    with torch.no_grad():
        event_times = y_val[:, 1].flatten().detach().cpu().numpy()

        output = model.predict(val_dataset.X)
        if isinstance(output, tuple):
            t_pred, p_pred = output
        else:
            t_pred = output

        preds = list(t_pred.flatten().detach().cpu().numpy())

        # get the uncensored and censored samples as a numpy array
        uncensored_idx = MyDataset.is_uncensored(val_dataset.y).flatten().detach().cpu().numpy()
        # get the event types
        event_indicators = list(uncensored_idx)

    return concordance_index(event_times, preds, event_indicators)
