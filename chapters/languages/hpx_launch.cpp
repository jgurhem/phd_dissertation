int hpx_main(boost::program_options::variables_map& vm)
{
    std::uint64_t N = vm["N"].as<std::uint64_t>();
    std::uint64_t T = vm["T"].as<std::uint64_t>();

    // Create the stepper object
    stepper step;

    // Execute nt time steps on nx grid points and print the final solution.
    stepper::space solution = step.do_lu(T, N);
    for (std::size_t i = 0; i != T * T; ++i)
        solution[i].get_data().wait();

    return hpx::finalize();
}

int main(int argc, char* argv[])
{
    using namespace boost::program_options;

    options_description desc_commandline;
    desc_commandline.add_options()(
        ("N", value<std::uint64_t>()->default_value(10),
        "Dimension of the submatrices")
        ("T", value<std::uint64_t>()->default_value(10),
        "Number of subblocks in each dimension");

    // Initialize and run HPX
    return hpx::init(desc_commandline, argc, argv);
}
