PMM(i, k)

k = 0 .. bm - 2
i = k + 1 .. bm - 1

: dcA(i, k)

RW     A <- (k == 0) ? dcA(i, k) : Aij PMM_D(i, k, k)
         -> Aik PMM_D(i, k + 1 .. bm - 1, k + 1)
         -> dcA(i, k)
READ   Inv <- Inv Inv(k)

BODY
{
    double *Ap = (double *)A;
    double *Bp = (double *)Inv;
    pmm_core(Ap, Bp, dcA->super.mb);
}
END
