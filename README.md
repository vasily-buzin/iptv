# Russian IPTV playlist for CUB

1. Create a **public** GitHub repository, e.g. `iptv-russia`.
2. Upload `update.py` and `.github/workflows/update.yml` preserving the directory structure (GitHub web upload may not conveniently handle hidden folders; Git or GitHub's file creation interface works).
3. In **Actions → Update Russian IPTV playlist → Run workflow**, start the first run.
4. After it finishes, add this URL to CUB (replace USERNAME and REPO):

   `https://raw.githubusercontent.com/USERNAME/REPO/main/russia.m3u`

   If your default branch is `master`, replace `main` with `master`.

The workflow checks the source every day at approximately 04:17 UTC (GitHub schedules may be delayed). Only direct `.m3u8` streams are included; web pages, DASH `.mpd`, and invalid entries are excluded. This is not a stream availability test. GitHub may disable scheduled workflows in inactive public repositories.
