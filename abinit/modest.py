from mpi4py import MPI
import sys
import os, sysconfig
libpy = sysconfig.get_config_var('LIBDIR') + '/'+ sysconfig.get_config_var('LDLIBRARY')

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    def mprint(text):
        if rank == 0:
            print(text)

    print(f"[Modest]: Started the MPI, rank %d" % rank)
    sys.stdout.flush()

    # Spawn a child for each parent rank
    # All ranks must call Spawn collectively
    mprint(f"[Modest]: Calling Spawn of DFT")
    intercomm = comm.Spawn("a.out", args=[libpy, "callback.py"], maxprocs=size)

    mprint(f"[Modest]: Started the intercomm")
    sys.stdout.flush()

    mprint(f"[Modest]: Waiting for DFT code")
    sys.stdout.flush()

    response = intercomm.recv(source=rank, tag=1)
    mprint(f"[Modest]: Got response from child: {response}")

    mprint(f"[Modest]: Three DFT+DMFT iterations")
    for it in range(3):

        mprint(f"[Modest]: Doing DMFT, done, now continue DFT")
        sys.stdout.flush()
        # P2P: talk to the matching child rank
        if it < 3-1:
            data = f"Continue DFT"
            intercomm.send(data, dest=rank, tag=0)
            intercomm.recv(source=rank, tag=1)
        else:
            data = f"Finish DFT"
            intercomm.send(data, dest=rank, tag=0)

    # (Optional) intra-Barrier among parents
    comm.Barrier()
    mprint(f"[Modest]: [Parent rank {rank}] entering intercomm barrier")
    sys.stdout.flush()

    # Intercomm collectives: both groups must participate
    intercomm.Barrier()
    intercomm.Disconnect()
    mprint(f"[Modest]: [Parent rank {rank}] dft_code has finished")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
