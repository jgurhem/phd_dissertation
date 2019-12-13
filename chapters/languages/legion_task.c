void stencil_task(const Task *task,
                  const std::vector<PhysicalRegion> &regions,
                  Context ctx, Runtime *runtime) {
  assert(regions.size() == 2);
  assert(task->regions.size() == 2);
  assert(task->regions[0].privilege_fields.size() == 1);
  assert(task->regions[1].privilege_fields.size() == 1);
  assert(task->arglen == sizeof(int));
  const int max_elements = *((const int*)task->args);
  const int point = task->index_point.point_data[0];

  FieldID r_fid = *(task->regions[0].privilege_fields.begin());
  FieldID w_fid = *(task->regions[1].privilege_fields.begin());

  const FieldAccessor<READ_ONLY,double,1> read_acc(regions[0], r_fid);
  const FieldAccessor<WRITE_DISCARD,double,1> write_acc(regions[1], w_fid);

  Rect<1> rect = runtime->get_index_space_domain(ctx,
                  task->regions[1].region.get_index_space());
    for (PointInRectIterator<1> pir(rect); pir(); pir++)
    {
      double l2, l1, r1, r2;
      double result = (-l2 + 8.0*l1 - 8.0*r1 + r2) / 12.0;
      write_acc[*pir] = result;
    }
}

int main(int argc, char **argv) {
  Runtime::set_top_level_task_id(TOP_LEVEL_TASK_ID);
  {
    TaskVariantRegistrar registrar(STENCIL_TASK_ID, "stencil");
    registrar.add_constraint(ProcessorConstraint(Processor::LOC_PROC));
    registrar.set_leaf();
    Runtime::preregister_task_variant<stencil_task>(registrar, "stencil");
  }
  return Runtime::start(argc, argv);
}
