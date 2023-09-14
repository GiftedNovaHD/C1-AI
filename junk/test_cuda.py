# This additional script provides a helper function to test for the availability of a CUDA-compatible GPU. 
# Just a bunch of random benchmarks to ensure that my GPU is the main device running the inference operations. 

import torch
import torch.nn as nn


device = torch.device("CUDA-enabled GPU" if torch.cuda.is_available() else "CPU")
print(f"Using device: {device}")
print("Running tests...")

x = torch.randn(64, 64)
x = x.to(device)


class Net(nn.Module): 
  def __init__(self): 
    super(Net, self).__init__()
    self.fc1 = nn.Linear(10, 10)
    self.fc2 = nn.Linear(10, 1)

  def forward(self, x): 
    x = self.fc1(x) 
    x = self.fc2(x) 
    return x 
  
net = Net()
net = net.to(device) 
print(f"Sample neural network is loaded into {device}")
print("Performing matrix multiplication test...")

tensor1 = torch.randn(64, 64)
tensor2 = torch.randn(64, 64)
print(f"64 * 64 matmul experiment results performed on {device}: ")
torch.matmul(tensor1, tensor2)