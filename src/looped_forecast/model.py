"""Executive summary: compare one, tied three, and untied three-pass transformers."""
import torch
from torch import nn
from torch.nn import functional as F


class GaussianTransformer(nn.Module):
    def __init__(self, text_dim: int, depth: int, tied: bool, use_text: bool):
        super().__init__()
        self.use_text = use_text
        self.depth = depth
        self.numeric = nn.Linear(1, 32)
        self.text = nn.Linear(text_dim, 32, bias=False)
        self.positions = nn.Parameter(torch.zeros(1, 22, 32))
        def block():
            return nn.TransformerEncoderLayer(32, 4, 64, dropout=0.0, batch_first=True, norm_first=True)
        self.blocks = nn.ModuleList([block() for _ in range(1 if tied else depth)])
        self.norm = nn.LayerNorm(32)
        self.head = nn.Linear(32, 2)

    def forward(self, numeric, text):
        numeric_tokens = self.numeric(numeric.unsqueeze(-1))
        evidence = self.text(text if self.use_text else torch.zeros_like(text)).unsqueeze(1)
        state = torch.cat((numeric_tokens, evidence), dim=1) + self.positions
        for i in range(self.depth):
            state = self.blocks[0 if len(self.blocks) == 1 else i](state)
        mean, log_scale = self.head(self.norm(state[:, 0])).unbind(-1)
        return mean, F.softplus(log_scale) + 0.02
