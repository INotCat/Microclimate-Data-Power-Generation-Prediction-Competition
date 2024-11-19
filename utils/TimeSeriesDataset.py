import numpy as np
from torch.utils.data import Dataset

class TimeSeriesDataset(Dataset):
    """
    Customized dataset for LSTM network.
    """
    def __init__(self, X: np.ndarray, Y: np.ndarray):
        self.X = X
        self.Y = Y
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, i):
        return self.X[i], self.Y[i]