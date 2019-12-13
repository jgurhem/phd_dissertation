#include <stdlib.h>
#include <stdbool.h>
#include <mpi.h>

typedef double XMP_Matrix;
typedef double* Matrix;

static MPI_Datatype Matrix_MPI_Type() { return MPI_DOUBLE;}

static bool Matrix_import(Matrix param, char* filename,
         const MPI_Datatype motif, const int size) {}
static bool Matrix_export(const Matrix param, char* filename,
         const MPI_Datatype motif, const int size, MPI_Comm Communicator) {}

