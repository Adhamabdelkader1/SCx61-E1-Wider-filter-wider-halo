# Extension tracks (optional, for bonus)

Pick **one** (two if you want). Each has a "Done when" condition, and you need evidence for it. All of them reuse what you already built. Nothing needs new software.

Put it in `EXTENSION.md` in your repo: which track, what you predicted **before** running, what you measured, what surprised you.

Run everything inside node0 as `student`, from the work folder, like the rest of the lab.

---

## E1. Wider filter, wider halo
**Idea:** a 5x5 box blur needs two rows from each neighbour, not one.
**Do:** write a serial 5x5 box blur (copy `filter_ref.py` and generalise it) and an MPI version whose halo exchange sends and receives **two** rows.
**Predict first:** if you keep a halo of one row for a 5x5 filter, which rows will differ from the serial result?
**Done when:** your two-row version gives 0 differing pixels against your 5x5 serial reference, and you also show the one-row version failing, with the differing row indices.

## E2. Find the hang boundary on your own machine
**Idea:** the width where the naive exchange starts to hang is a property of your Open MPI build and configuration, not a law of MPI.
**Do:** `break_deadlock.sh` always uses width 8192 (its argument is the timeout, not the width), so write your own loop. Each image row is `width` bytes (one byte per pixel):
```bash
for W in 256 1024 2048 4096 8192; do
  python3 make_test_image.py --width $W --height 300 --out-prefix sw_$W > /dev/null
  timeout 10 mpirun --hostfile hostfile -n 6 python3 img_mpi_v3_naive_halo.py sw_$W sw_${W}_out > /dev/null 2>&1
  echo "width=$W exit=$?"       # 0 = finished, 124 = killed by the timeout (hung)
done
```
Then narrow down between the last width that finished and the first that hung.
**Predict first:** which width will be the first to hang?
**Done when:** a table of widths with exit codes, the narrowest range you found, the exact command and timeout, a description of your machine, and one sentence on why a classmate's number may differ. Do **not** present your number as a constant of MPI.

## E3. Which programs does `Ssend` break?
**Idea:** `Ssend` completes only when the matching receive has started, so it exposes code that works only because the library buffers.
**Do:** you already ran the `Ssend` test on v3 at width 256. Now apply the same change (`comm.Send(` to `comm.Ssend(`) to copies of **v1** and **v2**.
**Predict first:** which of the two still finishes?
**Done when:** prediction, result for each, and an explanation of why v3 stalls under `Ssend` while v1 and v2 do not (look at the order of sends and receives).

## E4. What if the image is shorter than the number of ranks?
**Idea:** `split_rows` already handles heights that do not divide by 6 (try 301 and 302). The interesting question is the other end.
**Do:** run your finished v2 with `-n 6` on images of height 301, 302, 7, 6, 5 and 3 (use `--width 64` to keep it fast, and always wrap `mpirun` in `timeout 25`). Build a serial reference for each and compare.
**Predict first:** at what height does it stop working, and what exactly happens to the rank that gets no rows?
**Done when:** a table of heights with exit code and `compare.py` result, the first height that fails, the exact error line, an explanation of what happens to the **other** ranks, and a fix that makes the program refuse or adapt cleanly (for example, check before communicating) with proof.

## E5. Non-blocking exchange
**Idea:** `Isend` / `Irecv` with a wait removes the ordering problem in a different way from `Sendrecv`.
**Do:** copy `img_mpi_v3_naive_halo.py` and replace the blocking sends with non-blocking ones, then wait for them to finish before the program ends (`MPI.Request.Waitall`). Keep each send buffer alive and unchanged until its request completes.
**Done when:** it finishes on the 8192-wide image that hangs v3, matches the serial reference (0 differing pixels), and you explain in 3-4 lines why it no longer stalls and what must be true about the buffers until the wait returns.

## E6. Your own image
**Do:** convert a grayscale picture of your own to the format the lab uses, then run your v2 on it:
```bash
python3 -c "from PIL import Image; import numpy as np; np.save('myimg.npy', np.array(Image.open('photo.png').convert('L')))"
python3 -c "import numpy as np; from filter_ref import box_blur_3x3; np.save('myimg_serial.npy', box_blur_3x3(np.load('myimg.npy')))"
mpirun --hostfile hostfile -n 6 python3 img_mpi_v2_halo.py myimg myimg_v2
python3 compare.py --serial-prefix myimg_serial --candidate myimg_v2
```
**Done when:** before / after images in the README and 0 differing pixels. Do not use pictures of other people.

## E7. Show the incident in 60-90 seconds
**Do:** record a short screen capture or GIF: run, hang, one diagnosing command, fix, verify.
**Done when:** the file (under 10 MB) is in the repo and the README links it. No personal information on screen.

---

### How extensions are judged
Depth of evidence beats amount of code. A small extension with a real prediction, a real measurement and an honest note scores higher than a big one with no evidence.
