import "regent"
local c = regentlib.c
local std = terralib.includec("stdlib.h")
require("bla_common")

task make_partition_mat(points : region(ispace(int2d), double),
                        tiles : ispace(int2d), np : int32)
  var coloring = c.legion_domain_point_coloring_create()
  for i in tiles do
    var lo = int2d { x = i.x * np, y = i.y * np }
    var hi = int2d { x = (i.x + 1) * np - 1, y = (i.y + 1) * np - 1 }
    var rect = rect2d { lo = lo, hi = hi }
    c.legion_domain_point_coloring_color_domain(coloring, i, rect)
  end
  var p = partition(disjoint, points, coloring, tiles)
  c.legion_domain_point_coloring_destroy(coloring)
  return p
end

task main()
  var nt : int32 = 4
  var np : int32 = 4

  var gridA = ispace(int2d, { x = nt * np, y = nt * np })
  var tilesA = ispace(int2d, { x = nt, y = nt })
  var A = region(gridA, double)
  var Ap = make_partition_mat(A, tilesA, np)

  var gridA_inv = ispace(int2d, { x = nt * np, y = np })
  var tilesA_inv = ispace(int2d, { x = nt, y = 1 })
  var A_inv = region(gridA_inv, double)
  var A_inv_p = make_partition_mat(A_inv, tilesA_inv, np)

  init_mat(A)
  for k = 0, nt-1 do
    inversion(Ap[int2d({k, k})], A_inv_p[int2d({k, 0})], np)
    for i = k + 1, nt do
      pmm(Ap[int2d({i, k})], A_inv_p[int2d({k, 0})], np)
      for j = k + 1, nt do
        pmm_d(Ap[int2d({i, j})], Ap[int2d({i, k})], Ap[int2d({k, j})], np)
      end
    end
  end
end

regentlib.start(main)

