from mpi4py import MPI
import sys

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Spawn a child for each parent rank
    # All ranks must call Spawn collectively
    intercomm = comm.Spawn(sys.executable, args=["dft_code.py"], maxprocs=size)

    # P2P: talk to the matching child rank
    data = f"Hello from parent rank {rank}"
    intercomm.send(data, dest=rank, tag=0)
    response = intercomm.recv(source=rank, tag=1)
    print(f"[Parent rank {rank}] got response from child: {response}")

    # (Optional) intra-Barrier among parents
    comm.Barrier()
    print(f"[Parent rank {rank}] entering intercomm barrier")

    # Intercomm collectives: both groups must participate
    intercomm.Barrier()
    intercomm.Disconnect()
    print(f"[Parent rank {rank}] dft_code has finished.")

if __name__ == "__main__":
    main()
