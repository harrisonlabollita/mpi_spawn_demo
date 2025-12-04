from mpi4py import MPI

def main():
    # Check if we're a spawned process
    comm = MPI.COMM_WORLD
    parent = MPI.Comm.Get_parent()
    rank = comm.Get_rank()

    def mprint(text):
        if rank == 0:
            print(text)

    if parent == MPI.COMM_NULL:
        mprint("    [callback]: No parent communicator found. Exiting F.")
        return

    mprint(f"    [callback]: After running the DFT, we are now at the DMFT part, so we contact modest and wait")
    response = "Do DMFT"
    parent.send(response, dest=rank, tag=1)


    mprint(f"    [callback]: Waiting for signal from parent...")
    signal = parent.recv(source=rank, tag=0)
    mprint(f"    [callback]: Received signal: {signal}")


    if signal =="Finish DFT":
        parent.Barrier()
    # parent.Disconnect()

if __name__ == "__main__":
    main()
