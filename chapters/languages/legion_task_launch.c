ArgumentMap arg_map;

IndexLauncher stencil_launcher(STENCIL_TASK_ID, color_is,
     TaskArgument(&num_elements, sizeof(num_elements)), arg_map);
stencil_launcher.add_region_requirement(
    RegionRequirement(ghost_lp, 0/*projection ID*/,
                      READ_ONLY, EXCLUSIVE, stencil_lr));
stencil_launcher.add_field(0, FID_VAL);
stencil_launcher.add_region_requirement(
    RegionRequirement(disjoint_lp, 0/*projection ID*/,
                      READ_WRITE, EXCLUSIVE, stencil_lr));
stencil_launcher.add_field(1, FID_DERIV);
runtime->execute_index_space(ctx, stencil_launcher);

runtime->destroy_logical_region(ctx, stencil_lr);
runtime->destroy_field_space(ctx, fs);
runtime->destroy_index_space(ctx, is);
