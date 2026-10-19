# Knowledge check

Answer in full sentences, in your own words. These are the six questions at the end of `student_checklist.md`. This file is where your `SUBMISSION.md` section 6 lives.

**Q1.** Give two different causes of "containers healthy but `mpirun` hangs", and the output that tells them apart.

**Q2.** Why did the naive code pass on a small image and hang on a big one? Did the small run "prove" it correct?

**Q3.** When does "just raise the eager limit" stop working, and why is it not a fix?

**Q4.** Why can't `mpirun` just use `docker compose exec` instead of SSH?

**Q5.** Why does a 3x3 filter need exactly one halo row on each side? What changes for 5x5?

**Q6.** Why do we run MPI as `student` and not `root`?
