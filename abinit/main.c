// -------------------------------------------------------
// a demo test with a simple mpi C & Python code.
// -------------------------------------------------------
// compile with
// clang execute_python.c main.c  -ldl -rdynamic -lmpi
//
#include "execute_python.h"
#include <mpi.h>
#include <stdio.h>

#include <unistd.h>

int main(int argc, char** argv) {

 sleep(2);

 if (argc != 3) {
  fprintf(stderr, "  [DFT]: Requires 2 args : Python shared lib location + script");
  return 1;
 }

 int ierr, num_procs, my_id;
 ierr = MPI_Init(&argc, &argv);

 // do somethign with mpi
 ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
 ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

 printf("  [DFT]: Code is starting, parallelized, this one on rank %i\n", my_id);

 int i;
 for (i=0; i < 3; i++) {

     if (!my_id) {
      printf("  [DFT]: DFT iteration %i, it is doing its thing until it needs to call the python script for DMFT\n", i);
     }
     sleep(2);

     // launch python
     if (!my_id) {
      printf("  [DFT]: Launch python interpreter: %s\n", argv[1]);
     }
     init_python_interpreter(argv[1]);

     if (!my_id) {
      printf("  [DFT]: execute python file: %s (callback to modest)\n", argv[2]);
     }
     execute_python_file(argv[2]);
 }


 // check it has not been finalized
 int final;
 MPI_Finalized(&final);
 if (final) {
  fprintf(stderr, "  [DFT]: MPI is finalized on node %i\n", my_id);
  return 1;
 }

 // wait for all python to conclude
 // and redo some mpi after closing python
 MPI_Barrier(MPI_COMM_WORLD);

 ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
 ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

 printf("  [DFT]: Closing interpreter on rank %i\n", my_id);
 close_python_interpreter();
 MPI_Finalize();
 printf("  [DFT]: Finished\n");
}
