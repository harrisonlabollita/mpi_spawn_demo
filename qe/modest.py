from mpi4py import MPI
import sys, time
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
    #intercomm = comm.Spawn("a.out", args=[libpy, "callback.py"], maxprocs=size)
    # Spawn the wrapper instead of the child directly
    if rank==0:
        open("./wrapper.sh", 'w').write("""#!/bin/bash
            # wrapper.sh
            # Run the actual MPI child program
            "$@"
            # Signal completion by creating a marker file
            touch ./qe_is_done_${OMPI_COMM_WORLD_RANK:-0}
         """)
    comm.Barrier()
    args = ["./a.out"]
    intercomm = comm.Spawn( "./wrapper.sh", args=args, maxprocs=size)

    mprint(f"[Modest]: Started the intercomm")
    sys.stdout.flush()

    mprint(f"[Modest]: Waiting for DFT code")
    sys.stdout.flush()

    # Poll for completion (wait for all ranks)
    lock_file = f"./qe_is_done_{rank}"
    while not os.path.exists(lock_file):
        time.sleep(1)
    os.remove(lock_file)

    # marker_files = [f"/tmp/child_done_{i}" for i in range(size)]

    # while True:
        # all_done = all(os.path.exists(f) for f in marker_files)
        # if all_done:
            # # Clean up marker files
            # for f in marker_files:
              # pass
              # os.remove(f)
            # break
        # time.sleep(1)

    #try:
    #    intercomm.Disconnect()
    #except MPI.Exception:
    #    print("ok, rank = %s, error mpi comm trapped. DFT ended uncleanly"%rank)

    mprint(f"[Modest]: [Parent rank {rank}] dft_code has finished")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
