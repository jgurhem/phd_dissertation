import tensorflow as tf
import sys

N = 4
matsize = 10
A = {}
inv = {}
sess = tf.Session()

for i in range(N):
    for j in range(N):
        A[i,j] = tf.Variable(tf.random_uniform([matsize, matsize],
                                      seed = i * N + j))

init = tf.global_variables_initializer()
sess.run(init)

for k in range(N):
    inv[k] = tf.matrix_inverse(A[k, k])
    for i in range(k + 1, N):
        A[i,k] = tf.matmul(A[i,k], inv[k])
        for j in range(k + 1, N):
            A[i,j] = A[i,j] - tf.matmul(A[i,k], A[k,j])

for i in range(N):
    for j in range(N):
       sess.run(A[i,j])
