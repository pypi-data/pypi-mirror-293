import os
import random
import flgo.benchmark
import torch.nn as nn
import torch_geometric
from torch.nn import Linear
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool

path = os.path.join(flgo.benchmark.data_root, 'MUTAG')
all_data = torch_geometric.datasets.TUDataset(path, name='MUTAG', use_node_attr=True)
all_idxs = [i for i in range(len(all_data))]
random.shuffle(all_idxs)
num_samples = len(all_data)
train_idxs = all_idxs[:int(0.9*num_samples)]
test_idxs = all_idxs[int(0.9*num_samples):]
train_data = all_data[train_idxs]
test_data = all_data[test_idxs]


class GCN(nn.Module):
    def __init__(self, hidden_channels=64):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(7, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, hidden_channels)
        self.conv3 = GCNConv(hidden_channels, hidden_channels)
        self.lin = Linear(hidden_channels, 2)

    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        # 1. Obtain node embeddings
        x = self.conv1(x, edge_index)
        x = x.relu()
        x = self.conv2(x, edge_index)
        x = x.relu()
        x = self.conv3(x, edge_index)

        # 2. Readout layer
        x = global_mean_pool(x, batch)  # [batch_size, hidden_channels]

        # 3. Apply a final classifier
        x = F.dropout(x, p=0.5, training=self.training)
        x = self.lin(x)
        return x

def get_model():
    return GCN()