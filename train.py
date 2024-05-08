import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

# Define your custom dataset class (e.g., CustomDataset) and import it here
# from custom_dataset import CustomDataset

# Define your model (e.g., LSTMMLP) and import it here
# from my_model import LSTMMLP

# Define any necessary transforms for your dataset
# transform = transforms.Compose([...])

# Define data loaders for train, validation, and test sets
# train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
# val_loader = DataLoader(val_dataset, batch_size=batch_size)
# test_loader = DataLoader(test_dataset, batch_size=batch_size)

# Define the device (GPU if available, otherwise CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in tqdm(loader, desc='Training', leave=False):
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()

    train_loss = running_loss / len(loader)
    train_accuracy = correct / total
    return train_loss, train_accuracy

def validate_epoch(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in tqdm(loader, desc='Validation', leave=False):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    val_loss = running_loss / len(loader)
    val_accuracy = correct / total
    return val_loss, val_accuracy

def test_model(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in tqdm(loader, desc='Testing', leave=False):
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)

            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

    test_loss = running_loss / len(loader)
    test_accuracy = correct / total
    return test_loss, test_accuracy

def train_model(model, train_loader, val_loader, test_loader, criterion, optimizer, device, epochs):
    for epoch in range(epochs):
        print(f'Epoch {epoch + 1}/{epochs}')
        
        train_loss, train_accuracy = train_epoch(model, train_loader, criterion, optimizer, device)
        print(f'Train Loss: {train_loss:.4f}, Accuracy: {train_accuracy:.4f}')

        val_loss, val_accuracy = validate_epoch(model, val_loader, criterion, device)
        print(f'Validation Loss: {val_loss:.4f}, Accuracy: {val_accuracy:.4f}')

    test_loss, test_accuracy = test_model(model, test_loader, criterion, device)
    print(f'Test Loss: {test_loss:.4f}, Accuracy: {test_accuracy:.4f}')

# Usage example:

# Instantiate your custom dataset
# train_dataset = CustomDataset(train_data, train_targets, transform=transform)
# val_dataset = CustomDataset(val_data, val_targets, transform=transform)
# test_dataset = CustomDataset(test_data, test_targets, transform=transform)

# Instantiate your model
# model = LSTMMLP(input_size, hidden_size, num_layers, num_classes)

# Define criterion and optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
# train_model(model, train_loader, val_loader, test_loader, criterion, optimizer, device, epochs=num_epochs)
