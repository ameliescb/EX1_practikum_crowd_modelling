import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from torch.utils.data import DataLoader
from torchvision import datasets, transforms

import matplotlib.pyplot as plt

device = torch.device('cpu')

transforms = transforms.Compose([transforms.ToTensor()])
train_dataset = datasets.MNIST(
    './data',
    train=True,
    download=True,
    transform=transforms)

test_dataset = datasets.MNIST(
    './data',
    train=False,
    download=True,
    transform=transforms
)

BATCH_SIZE = 128        # number of data points in each batch
N_EPOCHS = 10           # times to run the model on complete data
INPUT_DIM = 28 * 28     # size of each input
HIDDEN_DIM = 256        # hidden dimension
LATENT_DIM = 2          # latent vector dimension
N_CLASSES = 10          # number of classes in the data
lr = 0.001              # learning rate

train_iterator = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
test_iterator = DataLoader(test_dataset, batch_size=BATCH_SIZE)

def idx2onehot(idx, n=N_CLASSES):

    assert idx.shape[1] == 1
    assert torch.max(idx).item() < n

    onehot = torch.zeros(idx.size(0), n)
    onehot.scatter_(1, idx.data, 1)

    return onehot

class Encoder(nn.Module):

    def __init__(self, input_dim, hidden_dim, latent_dim, n_classes):
        super().__init__()

        self.encode1 = nn.Linear(input_dim + n_classes, hidden_dim)
        self.encode2 = nn.Linear(hidden_dim, hidden_dim)

        self.mu = nn.Linear(hidden_dim, latent_dim)
        self.var = nn.Linear(hidden_dim, latent_dim)

    def forward(self, x):

        hidden1 = F.relu(self.encode1(x))
        hidden2 = F.relu(self.encode2(hidden1))

        mean = self.mu(hidden2)
        log_var = self.var(hidden2)

        return mean, log_var

class Decoder(nn.Module):

    def __init__(self, latent_dim, hidden_dim, output_dim, n_classes):
        super().__init__()

        self.decode1 = nn.Linear(latent_dim + n_classes, hidden_dim)
        self.decode2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):

        h = F.relu(self.decode1(x))
        output = torch.sigmoid(self.decode2(h))

        return output

class CVAE(nn.Module):

    def __init__(self, input_dim, hidden_dim, latent_dim, n_classes):
        super().__init__()

        self.encoder = Encoder(input_dim, hidden_dim, latent_dim, n_classes)
        self.decoder = Decoder(latent_dim, hidden_dim, input_dim, n_classes)

    def forward(self, x, y):

        x = torch.cat((x, y), dim=1)

        z_mu, z_var = self.encoder(x)

        std = torch.exp(z_var/2)
        eps = torch.randn_like(std)
        x_sample = eps.mul(std).add_(z_mu)

        z = torch.cat((x_sample, y), dim=1)

        output = self.decoder(z)

        return output, z_mu, z_var

model = CVAE(INPUT_DIM, HIDDEN_DIM, LATENT_DIM, N_CLASSES)
optimizer = optim.Adam(model.parameters(), lr=lr)

def calculate_loss(x, reconstructed_x, mean, log_var):
    # reconstruction loss
    RCL = F.binary_cross_entropy(reconstructed_x, x, size_average=False)
    # kl divergence loss
    KLD = -0.5 * torch.sum(1 + log_var - mean.pow(2) - log_var.exp())

    return RCL + KLD

def train():
    # set the train mode
    model.train()

    # loss of the epoch
    train_loss = 0

    for i, (x, y) in enumerate(train_iterator):
        # reshape the data into [batch_size, 784]
        x = x.view(-1, 28 * 28)
        x = x.to(device)

        # convert y into one-hot encoding
        y = idx2onehot(y.view(-1, 1))
        y = y.to(device)

        # update the gradients to zero
        optimizer.zero_grad()

        # forward pass
        reconstructed_x, z_mu, z_var = model(x, y)

        # loss
        loss = calculate_loss(x, reconstructed_x, z_mu, z_var)

        # backward pass
        loss.backward()
        train_loss += loss.item()

        # update the weights
        optimizer.step()

    return train_loss

def test():
    # set the evaluation mode
    model.eval()

    # test loss for the data
    test_loss = 0

    # we don't need to track the gradients, since we are not updating the parameters during evaluation / testing
    with torch.no_grad():
        for i, (x, y) in enumerate(test_iterator):
            # reshape the data
            x = x.view(-1, 28 * 28)
            x = x.to(device)

            # convert y into one-hot encoding
            y = idx2onehot(y.view(-1, 1))
            y = y.to(device)

            # forward pass
            reconstructed_x, z_mu, z_var = model(x, y)

            # loss
            loss = calculate_loss(x, reconstructed_x, z_mu, z_var)
            test_loss += loss.item()

    return test_loss

for e in range(N_EPOCHS):

    best_test_loss = 10000
    train_loss = train()
    test_loss = test()

    train_loss /= len(train_dataset)
    test_loss /= len(test_dataset)

    print(f'Epoch {e}, Train Loss: {train_loss:.2f}, Test Loss: {test_loss:.2f}')

    if best_test_loss > test_loss:
        best_test_loss = test_loss
        patience_counter = 1
    else:
        patience_counter += 1

    if patience_counter > 3:
        break

for i in range(10):
# create a random latent vector
    z = torch.randn(1, LATENT_DIM).to(device)

    # pick randomly 1 class, for which we want to generate the data
    y = torch.randint(0, N_CLASSES, (1, 1)).to(dtype=torch.long)
    print(f'Generating a {y.item()}')

    y = idx2onehot(y).to(device, dtype=z.dtype)
    z = torch.cat((z, y), dim=1)

    reconstructed_img = model.decoder(z)
    img = reconstructed_img.view(28, 28).data

    plt.figure()
    plt.imshow(img, cmap='gray')
    plt.show()