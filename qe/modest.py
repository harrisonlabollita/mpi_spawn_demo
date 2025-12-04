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
EXIT_CODE=$?

# Signal completion by creating a marker file
if [ $EXIT_CODE -eq 0 ]; then
    touch ./qe_is_done_${OMPI_COMM_WORLD_RANK:-0}
else
    touch ./qe_has_failed_${OMPI_COMM_WORLD_RANK:-0}
fi
        exit 0 #$EXIT_CODE
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
    lock_file_failed = f"./qe_has_failed_{rank}"
    while not os.path.exists(lock_file) and not os.path.exists(lock_file_failed):
        time.sleep(1)
    print("Rank= %s. before check file"%rank)
    if os.path.exists(lock_file_failed):
        print("DFT FAILED on rank %s!!!"%rank)
        os.remove(lock_file_failed)
    else:
        os.remove(lock_file)


    mprint(f"[Modest]: [Parent rank {rank}] dft_code has finished")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
