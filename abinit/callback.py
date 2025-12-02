from mpi4py import MPI

def main():
    # Check if we're a spawned process
    comm = MPI.COMM_WORLD
    parent = MPI.Comm.Get_parent()
    rank = comm.Get_rank()
    
    if parent == MPI.COMM_NULL:
        print("[DFT] No parent communicator found. Exiting F.")
        return

    print(f"[DFT rank {rank}] Waiting for signal from parent...")
    signal = parent.recv(source=rank, tag=0)
    print(f"[DFT rank {rank}] Received signal: {signal}")

   # Reply
    response = f"ACK from child {rank}"
    parent.send(response, dest=rank, tag=1)

    parent.Barrier()
    parent.Disconnect()

if __name__ == "__main__":
    main()
