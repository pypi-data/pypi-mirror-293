import os
import torch
import torch.nn as nn
import torch.optim as optim

class CheckpointManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.best_loss = float('inf')

    def save_checkpoint(self, model, optimizer, epoch, loss):
        if loss < self.best_loss:
            self.best_loss = loss
            state = {
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'epoch': epoch,
                'loss': loss
            }
            torch.save(state, self.filepath)
            print(f"Checkpoint saved at epoch {epoch} with loss {loss}")
            

    def load_checkpoint(self, model, optimizer):
        checkpoint = torch.load(self.filepath)
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        epoch = checkpoint['epoch']
        loss = checkpoint['loss']
        print(f"Checkpoint loaded from epoch {epoch} with loss {loss}")
        return epoch, loss
      
      
      
# 示例训练循环
if __name__ == "__main__":
    model = nn.Linear(10, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()
    num_epochs = 10
    checkpoint_manager = CheckpointManager('best_checkpoint.pth')

    for epoch in range(num_epochs):
        # 假设有训练数据和标签
        inputs = torch.randn(32, 10)  # 示例输入
        targets = torch.randn(32, 1)  # 示例目标

        # 前向传播
        outputs = model(inputs)
        loss = criterion(outputs, targets)

        # 反向传播和优化
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # 保存检查点
        checkpoint_manager.save_checkpoint(model, optimizer, epoch, loss.item())