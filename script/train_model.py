import sys
import os

# Add project root (two levels up) to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import torch
import torch.nn as nn
import torch.optim as optim
from home.utils.lstm import LSTMModel

def train_lstm_model():
    train_data = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3, 3, 3, 3, 3],
    ]
    labels = [1, 0, 1, 0]

    model = LSTMModel(input_size=9)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    x = torch.tensor(train_data, dtype=torch.float32).unsqueeze(1)  # [batch, seq, features]
    y = torch.tensor(labels, dtype=torch.float32)

    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        outputs = model(x).squeeze()
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()

    # Save model in 'home/models' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    models_dir = os.path.join(project_root, 'models')
    os.makedirs(models_dir, exist_ok=True)

    save_path = os.path.join(models_dir, 'lstm_model.pth')
    torch.save(model.state_dict(), save_path)
    print(f"Model trained and saved at {save_path}")

if __name__ == '__main__':
    train_lstm_model()
