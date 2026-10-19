# Incident report: <short title, e.g. "Halo exchange hangs on an 8192-wide image">

Blameless format: describe the system and the evidence, not who made the mistake. Every claim needs a command and its real output (or a screenshot). This file is also where your `SUBMISSION.md` sections 2 and 5 live: in `SUBMISSION.md` just write "see INCIDENT.md, section N".

## 1. Summary
Two sentences: what happened, and what the root cause was.

## 2. Symptoms
- What you ran: `bash break_deadlock.sh 20`. What you expected, and what you saw.
- Screenshot of the hang ending with `CONFIRMED HANG`: `evidence/hang.png`
- `docker compose ps` taken **while it hangs** (screenshot or pasted output): `evidence/ps_during_hang.png`. All nodes healthy. Why is that a problem for anyone who monitors only container health?
- Who emitted any error or warning line you quote? (your program, mpirun, Docker, the healthcheck?)

## 3. Timeline
| Step | Command | What I saw |
|---|---|---|
| 1 | | |

## 4. Investigation (three hypotheses, written before changing any code)
A hypothesis without a command and its output does not count.

| # | Hypothesis | Command that confirms or rejects it | Real output | Verdict |
|---|---|---|---|---|
| H1 | | | | |
| H2 | | | | |
| H3 | | | | |

Also report:
- `mpirun --hostfile hostfile -n 6 hostname`: output, and what it rules out.
- How far each rank got (`before Send` / `after Send` markers).
- Small image (`--width 256`) versus the 8192-wide image: what happened, and why a passing small run does not prove the program is correct.
- The `Ssend` test on a copy of v3 at width 256: what happened, and what it proves.

## 5. Root cause
In your own words, with the evidence that proves it:
- Which lines of `img_mpi_v3_naive_halo.py` are responsible? Quote them (only those lines).
- Which MPI behaviour is involved? Cite the Standard by **section title and version** (for example: MPI 4.1, "Communication Modes"). Open the page yourself before you cite it. Do not copy section numbers from anywhere.

## 6. The fix
- The smallest change that removes the cause: show the diff or the lines.
- Why does it remove the cause rather than only the symptom?

## 7. Verification
- `bash verify_fix.sh`, three runs in a row, each ending with 0 differing pixels (paste the outputs).
- `ssh node1 hostname` from node0 still works (Week 1 not broken).
- The width you verified at is above the width where the old code hung.

## 8. Prevention
What test or habit would catch this next time?
