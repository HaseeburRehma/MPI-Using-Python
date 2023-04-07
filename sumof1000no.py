from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

start = 1 + rank * (1000 // size)
end = (rank + 1) * (1000 // size)

if rank == size - 1:
    end = 1000

local_sum = 0
for i in range(start, end + 1):
    local_sum += i

total_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

if rank == 0:
    print("The sum of the numbers from 1 to 1000 is:", total_sum)
