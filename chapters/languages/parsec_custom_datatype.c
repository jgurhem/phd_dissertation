parsec_ddesc_t *create_and_distribute_data(int rank, int world, int size,
                                           int seg) {
    my_datatype_t *m = (my_datatype_t*)calloc(1, sizeof(my_datatype_t));
    parsec_ddesc_t *d = &(m->super);

    d->myrank = rank;
    d->nodes  = world;
    d->rank_of     = rank_of;
    d->rank_of_key = rank_of_key;
    d->data_of     = data_of;
    d->data_of_key = data_of_key;
    d->vpid_of     = vpid_of;
    d->vpid_of_key = vpid_of_key;
    d->data_key    = data_key;

    m->size = size;
    m->data = NULL;
    m->ptr  = (uint8_t*)calloc(size, 1);
    return d;
}
