import copy
import random
import sys
from pathlib import Path

import numpy as np
import torch
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.transforms import functional as TF


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "AS2" / "datasets"
TRAIN_DATA_PATH = DATA_DIR / "train_data.npz"
PUBLIC_TEST_PATH = DATA_DIR / "test_data_public.npz"
MODEL_OUTPUT_PATH = PROJECT_ROOT / "task1_model.pkl"

BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 1e-3
VAL_SIZE = 0.2
SEED = 42


sys.path.insert(0, str(PROJECT_ROOT / "AS2"))
from submission_helper import save_task1_model


class MaskTopLeftCorner:
    def __init__(self, size=4):
        self.size = size

    def __call__(self, image):
        image = np.array(image).copy()
        s = self.size
        image[:s, :s, :] = 0
        return TF.to_pil_image(image)


class Task1Dataset(Dataset):
    def __init__(self, images, labels, transform):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        image = self.transform(image)
        return image, label


class KarimKhabibCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.layer2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 32),
            nn.ReLU(),
            nn.Linear(32, 2),
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.classifier(x)
        return x


def build_transforms():
    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        MaskTopLeftCorner(size=4),
        transforms.ToTensor(),  # normalizes uint8 [0, 255] to float [0, 1]
    ])

    eval_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor(),  # normalizes uint8 [0, 255] to float [0, 1]
    ])

    return train_transform, eval_transform


def load_data():
    train_data = np.load(TRAIN_DATA_PATH)
    public_test_data = np.load(PUBLIC_TEST_PATH)

    x = train_data["X"]
    y = train_data["y"]
    x_public = public_test_data["X"]
    y_public = public_test_data["y"]

    x_train, x_val, y_train, y_val = train_test_split(
        x,
        y,
        test_size=VAL_SIZE,
        random_state=SEED,
        stratify=y,
    )

    return x_train, x_val, y_train, y_val, x_public, y_public


def build_loaders():
    x_train, x_val, y_train, y_val, x_public, y_public = load_data()
    train_transform, eval_transform = build_transforms()

    train_dataset = Task1Dataset(x_train, y_train, train_transform)
    val_dataset = Task1Dataset(x_val, y_val, eval_transform)
    public_test_dataset = Task1Dataset(x_public, y_public, eval_transform)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)
    public_test_loader = DataLoader(public_test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    return train_loader, val_loader, public_test_loader


def run_epoch(model, loader, criterion, device, optimizer=None):
    if optimizer is None:
        model.eval()
    else:
        model.train()

    running_loss = 0.0
    running_correct = 0
    total = 0

    with torch.set_grad_enabled(optimizer is not None):
        for inputs, targets in loader:
            inputs = inputs.to(device)
            targets = targets.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, targets)

            if optimizer is not None:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            preds = outputs.argmax(dim=1)
            running_loss += loss.item() * inputs.size(0)
            running_correct += (preds == targets).sum().item()
            total += targets.size(0)

    epoch_loss = running_loss / total
    epoch_acc = running_correct / total
    return epoch_loss, epoch_acc


def train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs):
    model.to(device)

    history = {
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": [],
    }

    best_weights = copy.deepcopy(model.state_dict())
    best_val_loss = float("inf")

    for epoch in range(epochs):
        train_loss, train_acc = run_epoch(model, train_loader, criterion, device, optimizer)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, device)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["val_loss"].append(val_loss)
        history["val_acc"].append(val_acc)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_weights = copy.deepcopy(model.state_dict())

        print(
            f"Epoch {epoch + 1}/{epochs} | "
            f"train_loss: {train_loss:.4f} | train_acc: {train_acc:.4f} | "
            f"val_loss: {val_loss:.4f} | val_acc: {val_acc:.4f}"
        )

    model.load_state_dict(best_weights)
    return model, history


def evaluate_accuracy(model, loader, device):
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            preds = outputs.argmax(dim=1)
            total += labels.size(0)
            correct += (preds == labels).sum().item()

    return correct / total


def main():
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    random.seed(SEED)

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    train_loader, val_loader, public_test_loader = build_loaders()

    model = KarimKhabibCNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.CrossEntropyLoss()

    model, history = train_model(
        model,
        train_loader,
        val_loader,
        criterion,
        optimizer,
        device,
        EPOCHS,
    )

    val_acc = evaluate_accuracy(model, val_loader, device)
    public_test_acc = evaluate_accuracy(model, public_test_loader, device)

    print()
    print(f"Device: {device}")
    print(f"Validation accuracy: {val_acc:.4f}")
    print(f"Public test accuracy: {public_test_acc:.4f}")
    print(f"Best validation loss: {min(history['val_loss']):.4f}")

    model = model.to("cpu")
    save_task1_model(model, str(MODEL_OUTPUT_PATH))


if __name__ == "__main__":
    main()
