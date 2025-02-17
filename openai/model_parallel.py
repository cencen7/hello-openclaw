import os
import torch
import torch.nn as nn
import torch.distributed as dist
import torch.multiprocessing as mp


class Part1(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Part1, self).__init__()
        self.fc = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        x = self.fc(x)
        x = self.relu(x)
        return x
    

class Part2(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(Part2, self).__init__()
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = self.fc(x)
        return x
    
def run_model_parallel(rank, world_size):
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    
    dist.init_process_group(
        backend="gloo",
        rank=rank,
        world_size=world_size,
        init_method="tcp://localhost:12355"
    )
    
    print(f"[rank {rank}]: Process group initialized.")
    
    # hyperparameters
    input_size = 10
    hidden_size = 20
    output_size = 5
    batch_size = 64

    if rank == 0:
        model_part = Part1(input_size, hidden_size)
        optimizer = torch.optim.SGD(model_part.parameters(), lr=0.001)
    elif rank == 1:
        model_part = Part2(hidden_size, output_size)
        optimizer = torch.optim.SGD(model_part.parameters(), lr=0.001)

    if rank == 0:
        x = torch.randn(batch_size, input_size)
    if rank == 1:
        target = torch.randn(batch_size, output_size)

    for epoch in range(5):
        optimizer.zero_grad()
        if rank == 0:
            intermediate = model_part(x)
            # send the intermediate tensor to rank 1
            dist.send(tensor=intermediate, dst=1)
            # wait for the gradient of the intermediate tensor from rank 1
            grad_intermediate = torch.zeros_like(intermediate)
            dist.recv(tensor=grad_intermediate, src=1)
            # backward pass on part 1 using the received gradient
            intermediate.backward(grad_intermediate)
            optimizer.step()
            print(f"[Rank 0, Epoch {epoch}]: Part1 update complete.")
            
        elif rank == 1:
            # prepare tensor to receive the intermediate tensor from rank 0
            intermediate = torch.zeros(batch_size, hidden_size)
            dist.recv(tensor=intermediate, src=0)

            # Enable gradient tracking for the received intermediate tensor
            intermediate.requires_grad_()

            # Forward pass on part2 using the received intermediate tensor
            out = model_part(intermediate)
            loss = nn.MSELoss()(out, target)
            loss.backward()
            # send the gradient of the intermediate tensor to rank 0
            dist.send(tensor=intermediate.grad, dst=0)
            optimizer.step()
            print(f"[Rank 1, Epoch {epoch}]: Loss {loss.item():.4f}, Part2 update complete.")
        
        
    # Clean up
    dist.destroy_process_group()


# Define a simple model as a sequential module.
class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 20),
            nn.ReLU(),
            nn.Linear(20, 5)
        )

    def forward(self, x):
        return self.net(x)


def main():
    world_size = 2
    mp.spawn(run_model_parallel, args=(world_size,), nprocs=world_size, join=True)

if __name__ == "__main__":
    main()