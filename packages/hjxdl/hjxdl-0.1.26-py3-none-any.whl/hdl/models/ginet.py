import torch
from torch import nn
import torch.nn.functional as F

# from torch_geometric.nn import MessagePassing
# from torch_geometric.utils import add_self_loops
from torch_geometric.nn import global_add_pool, global_mean_pool, global_max_pool

from hdl.layers.graph.gin import GINEConv
from hdl.layers.general.linear import (
    # BNReLULinear,
    BNReLULinearBlock,
)
from hdl.models.utils import load_model
from hdl.ops.utils import get_activation


__all__ = [
    "GINet",
    "GINMLPR",
]


num_atom_type = 119  # including the extra mask tokens
num_chirality_tag = 3

num_bond_type = 5  # including aromatic and self-loop edge
num_bond_direction = 3 


class GINet(nn.Module):
    """
    Args:
        num_layer (int): the number of GNN layers
        emb_dim (int): dimensionality of embeddings
        max_pool_layer (int): the layer from which we use max pool rather than add pool for neighbor aggregation
        drop_ratio (float): dropout rate
        gnn_type: gin, gcn, graphsage, gat
    Output:
        node representations
    """
    def __init__(
        self,
        num_layer=5,
        emb_dim=300,
        feat_dim=512,
        drop_ratio=0,
        pool='mean'
    ):
        super(GINet, self).__init__()
        self.init_args = {
            'num_layer': num_layer,
            'emb_dim': emb_dim,
            'feat_dim': feat_dim,
            'drop_ratio': drop_ratio,
            'pool': pool
        }
        self.num_layer = num_layer
        self.emb_dim = emb_dim
        self.feat_dim = feat_dim
        self.drop_ratio = drop_ratio

        self.x_embedding1 = nn.Embedding(num_atom_type, emb_dim)
        self.x_embedding2 = nn.Embedding(num_chirality_tag, emb_dim)
        nn.init.xavier_uniform_(self.x_embedding1.weight.data)
        nn.init.xavier_uniform_(self.x_embedding2.weight.data)

        # List of MLPs
        self.gnns = nn.ModuleList()
        for layer in range(num_layer):
            self.gnns.append(GINEConv(emb_dim))

        # List of batchnorms
        self.batch_norms = nn.ModuleList()
        for layer in range(num_layer):
            self.batch_norms.append(nn.BatchNorm1d(emb_dim))
        
        if pool == 'mean':
            self.pool = global_mean_pool
        elif pool == 'max':
            self.pool = global_max_pool
        elif pool == 'add':
            self.pool = global_add_pool
        
        self.feat_lin = nn.Linear(
            self.emb_dim,
            self.feat_dim
        )

        self.out_lin = nn.Sequential(
            nn.Linear(self.feat_dim, self.feat_dim), 
            nn.ReLU(inplace=True),
            nn.Linear(
                self.feat_dim,
                self.feat_dim // 2
            )
        )

    def forward(self, data):
        x = data.x
        edge_index = data.edge_index
        edge_attr = data.edge_attr

        h = self.x_embedding1(x[:,0]) + self.x_embedding2(x[:,1])

        for layer in range(self.num_layer):
            h = self.gnns[layer](h, edge_index, edge_attr)
            h = self.batch_norms[layer](h)
            if layer == self.num_layer - 1:
                h = F.dropout(h, self.drop_ratio, training=self.training)
            else:
                h = F.dropout(F.relu(h), self.drop_ratio, training=self.training)

        h = self.pool(h, data.batch)
        h = self.feat_lin(h)
        out = self.out_lin(h)
        
        return h, out


class GINMLPR(nn.Module):
    def __init__(
        self,
        num_layer=5,
        emb_dim=300,
        feat_dim=512,
        out_dim=1,
        drop_ratio=0,
        pool='mean',
        ckpt_file: str = None,
        num_smiles: int = 1,
    ) -> None:
        super().__init__()
        self.init_args = {
            "num_layer": num_layer,
            "emb_dim": emb_dim,
            "feat_dim": feat_dim,
            "out_dim": out_dim,
            "drop_ratio": drop_ratio,
            "pool": pool,
            "ckpt_file": ckpt_file,
            "num_smiles": num_smiles
        }
        self.gins = nn.ModuleList([])
        for _ in range(num_smiles):
            self.gins.append(
                GINet(
                    num_layer=num_layer,
                    emb_dim=emb_dim,
                    feat_dim=feat_dim,
                    drop_ratio=drop_ratio,
                    pool=pool,
                )
            )
        self.ckpt_file = ckpt_file
        self.num_smiles = num_smiles

        self.ffn = BNReLULinearBlock(
            in_features=feat_dim // 2 * num_smiles,
            out_features=out_dim,
            num_layers=num_layer,
            hidden_size=feat_dim // 2
        )
        self.out_act = get_activation('sigmoid')

        if ckpt_file is not None:
            self.load_ckpt()

    def load_ckpt(self):
        if self.ckpt_file is not None:
            for i in range(self.num_smiles):
                load_model(
                    self.ckpt_file,
                    model=self.gins[i]
                )
 
    def forward(
        self,
        data 
    ):
        out_list = []
        for data_i, gin in zip(data, self.gins):
            out_list.append(gin(data_i[0])[1])
        out = torch.hstack(out_list)  # (batch_size, feat_dim//2 * num_smiles)
        out = self.ffn(out)
        out = self.out_act(out)

        return out
            