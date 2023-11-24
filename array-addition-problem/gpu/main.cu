#include <stdio.h>

__global__ void vectorAdd(int* a, int* b, int* c) {
    int i = threadIdx.x;
    c[i] = a[i] + b[i];
    return;
}

int main() {
	int a[] = {1,2,3};
	int b[] = {4,5,6};
	int c[sizeof(a) / sizeof(int)] = {0};
	// Creating pointers into GPU
	int* cudaA = 0;
	int* cudaB = 0;
	int* cudaC = 0;
	// Allocate memory in the GPU
	cudaMalloc(&cudaA, sizeof(a));
	cudaMalloc(&cudaB, sizeof(b));
	cudaMalloc(&cudaC, sizeof(c));
	// Copy the vectors into the gpu
	cudaMemcpy(cudaA, a, sizeof(a), cudaMemcpyHostToDevice);
	cudaMemcpy(cudaB, b, sizeof(b), cudaMemcpyHostToDevice);
	// Launch the kernel with one block and a number of threads equal to the size of the vectors
	vectorAdd <<<1, sizeof(a) / sizeof(a[0])>>> (cudaA, cudaB, cudaC);
	// Copy the result vector back to the host
	cudaMemcpy(c, cudaC, sizeof(c), cudaMemcpyDeviceToHost);
	// Print the result
	for (int i = 0; i < sizeof(c) / sizeof(int); i++) {
		printf("c[%d] = %d\n", i, c[i]);
	}

	return 0;
}
