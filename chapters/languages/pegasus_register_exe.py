e_findrange = Executable(namespace="diamond", name="findrange", version="4",
                    os="linux", arch="x86_64", installed=True)
e_findrange.addPFN(PFN("file://" + sys.argv[1] + "/bin/pegasus-keg",
                    "TestCluster"))
diamond.addExecutable(e_findrange)
