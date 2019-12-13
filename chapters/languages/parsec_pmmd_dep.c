READ   Aik <- A PMM(i, k - 1)
RW     Aij <- (k == 1) ? dcA(i, j) : Aij PMM_D(i, j, k - 1)
           -> (i > k && j == k) ? A PMM(i, j)
           -> (i > k && j > k) ? Aij PMM_D(i, j, k + 1)
