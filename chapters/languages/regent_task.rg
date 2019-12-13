task pmm_d(A : region(ispace(int2d), double),
           B : region(ispace(int2d), double),
           C : region(ispace(int2d), double), n : int)
where reads(B), reads(C), reads writes(A) do
  for i = 0, n do
    for j = 0, n do
      for k = 0, n do
        A[int2d({i, j}) + A.bounds.lo] = A[int2d({i, j}) + A.bounds.lo]
             -B[int2d({i, k}) + B.bounds.lo] * C[int2d({k, j}) + C.bounds.lo]
      end
    end
  end
end
