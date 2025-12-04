#include <mpi.h>
#include <iostream>

int main(int argc, char* argv[]) {

    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Each rank contributes its own rank number to the sum
    int local_value = rank+1;
    std::cout << "I am rank= " << rank+1 << " with local_value = " << local_value << std::endl;

    int total_sum = 0;

    // Sum all ranks' contributions to the master rank (rank 0)
    MPI_Reduce(&local_value, &total_sum, 1, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    // Print result on master rank
    if (rank == 0) {
        std::cout << "Sum of all ranks: " << total_sum << std::endl;
    }

    // Disconnect
    MPI_Comm parent;
    MPI_Comm_get_parent(&parent);
    if (parent != MPI_COMM_NULL) {
         MPI_Comm_disconnect(&parent);
    }

    // Finalize MPI if we initialized it
   MPI_Finalize();

    return 0;
}
