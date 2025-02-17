"""
Potential Debugging Approaches

Minimal Reproducible Example
When issues arise in a multi-process or multi-machine environment, 
first isolate a minimal model (e.g., a one-layer MLP) and a small dataset to check if the distributed logic runs as expected.
If this minimal example also fails, it’s likely a fundamental environment/config issue. 
If the minimal example works but the large model fails, the problem might be scale or complexity related.

Forward/Backward Shape Checks
In model parallel scenarios, 
ensure that when you split a tensor in the forward pass, the shapes match what the downstream process expects, 
and that in the backward pass the gradient shapes match as well.
Print or log the shape of intermediate tensors on each rank to confirm they match your expectations.

Gradient Debugging
On a single machine, you might do a numerical gradient check (finite differences) to confirm correctness.
In a distributed setup:
Data parallel: Compare gradients across processes before and after synchronization to ensure they are consistent.
Model parallel: Make sure partial gradients are properly passed back to the corresponding model partitions.

Communication Libraries and Modes
In PyTorch, torch.distributed supports backends like Gloo, NCCL, and MPI. Ensure each process uses the same backend.
If you’re using lower-level Python multiprocessing or custom sockets, you must manually manage queues, pipes, locks, etc. This can be particularly tricky to debug.
Sync vs. Async

Some operations (e.g., NCCL all-reduce) can be asynchronous. You may need to explicitly call torch.cuda.synchronize() or .wait() to ensure certain operations complete before moving on.
Otherwise, you could experience partial updates, timing issues, or processes waiting for each other unpredictably.
Random Seeds and Initialization

If reproducibility is desired, each process should fix the random seed.
In data-parallel settings, 
be mindful that different ranks might handle different data shards or random augmentations, 
leading to subtle differences in the training outcome if not carefully controlled.

Logging & Visualization
It’s often helpful to log metrics (epoch, batch, loss, gradient norms, etc.) per rank to compare behaviors across processes.
Use distributed logging or visualization tools (like TensorBoard, MLFlow, or WandB) to monitor all ranks in one place.
Eliminate Hardware Faults

In multi-machine scenarios, networking inconsistencies or GPU driver mismatches can also lead to training failures that appear as code bugs


Backend	Best For	Pros	Cons
NCCL	Multi-GPU (NVIDIA)	- Highly optimized for GPU
- Good performance for large-scale GPU clusters	- Works only with NVIDIA GPUs
- Requires up-to-date CUDA drivers and matching versions
Gloo	CPU clusters or small GPU setups	- Works out of the box with CPU
- Built into PyTorch (no extra installation)	- Generally slower than NCCL for GPU
- Not as optimized for large-scale GPU training
MPI	HPC clusters with MPI	- Standard HPC communication
- Can leverage specialized HPC interconnects	- Must install and configure an MPI library
- Performance depends on MPI implementation

world_size = total number of distributed processes.
rank = ID for the current process.
In many cluster setups, environment variables (e.g., MASTER_ADDR, MASTER_PORT, RANK, WORLD_SIZE) are automatically set by a job scheduler or manually provided.
"""

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


import torch
import torch.nn as nn
import torch.optim as optim
import torch.distributed as dist
import torch.multiprocessing as mp


class SimpleMLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x
    
def train(rank, world_size, backend='gloo'):
    os.environ["MASTER_ADDR"] = "localhost"  # Replace with master node's IP if needed
    os.environ["MASTER_PORT"] = "12355" 

    dist.init_process_group(
    backend=backend,
    rank=rank,
    world_size=world_size,
    init_method="tcp://localhost:12355"
    )
    print(f"[rank {rank}]: Process group initialized.")

    model = SimpleMLP(input_size=10, hidden_size=20, output_size=5)
    model = model.to(rank)
    optimizer = optim.SGD(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()

    data = torch.randn(64, 10).to(rank)
    target = torch.randn(64, 5).to(rank)

    for epoch in range(5):
        optimizer.zero_grad()
        outputs = model(data)
        loss = criterion(outputs, target)
        loss.backward()

        for param in model.parameters():
            dist.all_reduce(param.grad,
                            op=dist.ReduceOp.SUM)
            param.grad /= world_size

        optimizer.step()
        
        if rank == 0:
            print(f"Rank {rank}, epoch {epoch}, loss {loss.item()}")

    dist.destroy_process_group()

def main():
    world_size = 2
    mp.spawn(train, args=(world_size,), nprocs=world_size, join=True)

if __name__ == "__main__":
    main()
