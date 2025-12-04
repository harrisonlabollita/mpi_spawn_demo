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

    # Wait for the child to disconnect ?
    #try:
    intercomm.Disconnect()
    #.Exception:
    #    print("ok, rank = %s, error mpi comm trapped. DFT ended uncleanly"%rank)

    mprint(f"[Modest]: [Parent rank {rank}] dft_code has finished")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
