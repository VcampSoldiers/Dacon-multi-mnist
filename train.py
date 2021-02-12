import torch
from torch.utils.data import DataLoader
from torch import nn
from dataset import MnistDataset
from preprocess import transforms_train, transforms_test
from model import MnistModel
from torchinfo import summary
import torch.optim as optim


trainset = MnistDataset(
    'data/train', 'data/dirty_mnist_2nd_answer.csv', transforms_train)
testset = MnistDataset(
    'data/test', 'data/sample_submission.csv', transforms_test)

train_loader = DataLoader(trainset, batch_size=256, num_workers=8)
test_loader = DataLoader(testset, batch_size=32, num_workers=4)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = MnistModel().to(device)
print(summary(model, input_size=(1, 3, 256, 256), verbose=0))

optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MultiLabelSoftMarginLoss()

num_epochs = 10
model.train()

for epoch in range(num_epochs):
    for i, (images, targets) in enumerate(train_loader):
        optimizer.zero_grad()

        images = images.to(device)
        targets = targets.to(device)

        outputs = model(images)
        loss = criterion(outputs, targets)

        loss.backward()
        optimizer.step()

        if (i+1) % 10 == 0:
            outputs = outputs > 0.5
            acc = (outputs == targets).float().mean()
            print(f'{epoch}: {loss.item():.5f}, {acc.item():.5f}')
