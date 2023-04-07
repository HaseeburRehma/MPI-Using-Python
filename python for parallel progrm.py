from mpi4py import MPI

rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size

print(f"I am process {rank} of {size}")