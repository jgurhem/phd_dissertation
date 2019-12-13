struct stepper
{
   typedef std::vector<partition> space;

   //C = C - A * B
   static partition_data pmm_d_core(
      partition_data const& A, partition_data const& B,
      partition_data const& C) {}

   static partition pmm_d_part(
      partition const& A_p, partition const& B_p, partition const& C_p)
   {
      using hpx::dataflow;
      using hpx::util::unwrapping;

      hpx::shared_future<partition_data> A_data = A_p.get_data();
      hpx::shared_future<partition_data> B_data = B_p.get_data();
      hpx::shared_future<partition_data> C_data = C_p.get_data();
      return dataflow(hpx::launch::async,
         unwrapping([C_p](partition_data const& A, partition_data const& B,
                      partition_data const& C) -> partition {
            partition_data r = stepper::pmm_d_core(A, B, C);
            return partition(C_p.get_id(), r);
         }),
         A_data, B_data, C_data);
   }

   space do_lu(std::size_t T, std::size_t N);
};

HPX_PLAIN_ACTION(stepper::pmm_d_part, pmm_d_part_action);

