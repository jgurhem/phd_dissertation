stepper::space stepper::do_lu(std::size_t T, std::size_t N,
                              bool print_matrices) {
   using hpx::dataflow;

   std::vector<hpx::id_type> localities = hpx::find_all_localities();
   std::size_t nl = localities.size();    // Number of localities

   space tiles, invs;
   tiles.resize(T * T);
   invs.resize(T);

   for (std::size_t i = 0; i != T; ++i)
      for (std::size_t j = 0; j != T; ++j)
         tiles[idx(i, j, T)] =
             partition(localities[locidx(i, j, T, nl)], N, T, i, j);
   for (std::size_t i = 0; i != T; ++i)
      invs[i] = partition(localities[locidx(i, 0, T, nl)], N, T, i, 0);

   inv_part_action act_inv;
   pmm_part_action act_pmm;
   pmm_d_part_action act_pmm_d;
   using hpx::util::placeholders::_1;
   using hpx::util::placeholders::_2;
   using hpx::util::placeholders::_3;

   for (std::size_t k = 0; k < T - 1; ++k) {
      auto Op =
          hpx::util::bind(act_inv, localities[locidx(k, 0, T, nl)], _1, _2);
      invs[k] =
          dataflow(hpx::launch::async, Op, tiles[idx(k, k, T)], invs[k]);
      for (std::size_t i = k + 1; i < T; ++i) {
         auto Op = hpx::util::bind(
             act_pmm, localities[locidx(k, 0, T, nl)], _1, _2);
         tiles[idx(i, k, T)] =
             dataflow(hpx::launch::async, Op, tiles[idx(i, k, T)], invs[k]);
         for (std::size_t j = k + 1; j < T; ++j) {
            auto Op = hpx::util::bind(
                act_pmm_d, localities[locidx(i, j, T, nl)], _1, _2, _3);
            tiles[idx(i, j, T)] =
                dataflow(hpx::launch::async, Op, tiles[idx(i, k, T)],
                    tiles[idx(k, j, T)], tiles[idx(i, j, T)]);
         }
      }
   }

   // Return the LU factorization
   return tiles;
}
