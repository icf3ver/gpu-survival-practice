CC = gcc
FLAGS = -O0

cpu: build/cpu

build/cpu: cpu/main.o
	$(CC) $< -o $@
cpu/main.o: cpu/main.c
	@echo $@
	$(CC) -c $< -o $@

NVCC = nvcc

gpu: build/gpu

build/gpu: gpu/main.cu
	nvcc $< -o $@
