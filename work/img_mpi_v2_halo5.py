#!/usr/bin/env python3
import socket
import sys
import numpy as np
from mpi4py import MPI

IN_PREFIX = "test_image"
OUT_PREFIX = "test_image_filtered_v2_5x5"
R = 2                                  # filter radius (5x5)
H = int(sys.argv[3]) if len(sys.argv) > 3 else 2   # halo rows (2 = correct, 1 = fails)


def box_blur_5x5(img: np.ndarray) -> np.ndarray:
    padded = np.pad(img.astype(np.float64), pad_width=R, mode="edge")
    acc = np.zeros_like(img, dtype=np.float64)
    h, w = img.shape
    for dy in range(-R, R + 1):
        for dx in range(-R, R + 1):
            acc += padded[R + dy: R + dy + h, R + dx: R + dx + w]
    acc /= 25.0
    return np.clip(acc, 0, 255).astype(np.uint8)


def split_rows(height, n):
    base, extra = height // n, height % n
    bounds, start = [], 0
    for i in range(n):
        rows = base + (1 if i < extra else 0)
        bounds.append((start, start + rows))
        start += rows
    return bounds


def halo_exchange(comm, rank, size, strip, width):
    top_halo = np.empty((H, width), dtype=np.uint8)
    bottom_halo = np.empty((H, width), dtype=np.uint8)

    if rank > 0:
        comm.Sendrecv(sendbuf=np.ascontiguousarray(strip[:H]), dest=rank - 1, sendtag=30,
                      recvbuf=top_halo, source=rank - 1, recvtag=31)
    else:
        top_halo = np.repeat(strip[0:1], H, axis=0)

    if rank < size - 1:
        comm.Sendrecv(sendbuf=np.ascontiguousarray(strip[-H:]), dest=rank + 1, sendtag=31,
                      recvbuf=bottom_halo, source=rank + 1, recvtag=30)
    else:
        bottom_halo = np.repeat(strip[-1:], H, axis=0)

    return top_halo, bottom_halo


def filter_with_halo(strip, top_halo, bottom_halo):
    extended = np.vstack([top_halo, strip, bottom_halo])
    filtered = box_blur_5x5(extended)
    return filtered[H:H + strip.shape[0], :]


def main():
    comm = MPI.COMM_WORLD
    rank, size = comm.Get_rank(), comm.Get_size()
    hostname = socket.gethostname()

    in_prefix = sys.argv[1] if len(sys.argv) > 1 else IN_PREFIX
    out_prefix = sys.argv[2] if len(sys.argv) > 2 else OUT_PREFIX

    if rank == 0:
        img = np.load(f"{in_prefix}.npy")
        height, width = img.shape
        bounds = split_rows(height, size)
        my_start, my_end = bounds[0]
        my_strip = img[my_start:my_end, :].copy()
        for worker in range(1, size):
            w_start, w_end = bounds[worker]
            strip = img[w_start:w_end, :].copy()
            comm.send(strip.shape, dest=worker, tag=10)
            comm.Send(strip, dest=worker, tag=11)
        width_for_halo = width
    else:
        shape = comm.recv(source=0, tag=10)
        my_strip = np.empty(shape, dtype=np.uint8)
        comm.Recv(my_strip, source=0, tag=11)
        width_for_halo = shape[1]

    top_halo, bottom_halo = halo_exchange(comm, rank, size, my_strip, width_for_halo)
    my_filtered = filter_with_halo(my_strip, top_halo, bottom_halo)

    if rank == 0:
        result = np.zeros_like(img)
        result[my_start:my_end, :] = my_filtered
        for worker in range(1, size):
            w_start, w_end = bounds[worker]
            shape = comm.recv(source=worker, tag=20)
            buf = np.empty(shape, dtype=np.uint8)
            comm.Recv(buf, source=worker, tag=21)
            result[w_start:w_end, :] = buf
        np.save(f"{out_prefix}.npy", result)
        print(f"[rank 0 on {hostname}] wrote {out_prefix}.npy (halo rows H={H}, filter 5x5)", flush=True)
    else:
        comm.send(my_filtered.shape, dest=0, tag=20)
        comm.Send(my_filtered, dest=0, tag=21)


if __name__ == "__main__":
    main()