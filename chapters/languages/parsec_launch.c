parsec = parsec_init(cores, &argc, &argv);

two_dim_block_cyclic_init( &dcA, matrix_RealDouble, matrix_Tile,
                           world, rank, mb, mb, lm, lm, 0, 0, lm, lm,
                           1, 1, rows );
dcA.mat = parsec_data_allocate((size_t)dcA.super.nb_local_tiles *
                                 (size_t)dcA.super.bsiz *
                                 (size_t)parsec_datadist_getsizeoftype(
                                              dcA.super.mtype));

srand(rank + 1);
double * matp = (double *)dcA.mat;
for(int i = 0; i < dcA.super.nb_local_tiles * dcA.super.bsiz; i++) {
     matp[i] = (double)((rand() % 2000) - 1000) / 100;
}

tp = parsec_lu_new(&dcA, bm);
