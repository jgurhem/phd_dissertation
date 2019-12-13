struct partition_server : hpx::components::component_base<partition_server> {
   partition_server() {}

   partition_server(partition_data const& data)
     : data_(data) {}

   partition_server(std::size_t n,std::size_t t,std::size_t i,std::size_t j)
     : data_(n, t, i, j) {}

   partition_data get_data() const { return data_; }

   HPX_DEFINE_COMPONENT_DIRECT_ACTION(
      partition_server, get_data, get_data_action);

private:
   partition_data data_;
};

typedef hpx::components::component<partition_server> partition_server_type;
HPX_REGISTER_COMPONENT(partition_server_type, partition_server);

typedef partition_server::get_data_action get_data_action;
HPX_REGISTER_ACTION(get_data_action);
