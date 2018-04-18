# github-MCMC
Using MCMC &amp; Page Rank to rank Github repositories and users.

## To use:

```
pip install requirements.txt
```

Add your API token to `specs.py`. Run,

```
python crawler.py
```

To get the top repos, run 
```
python store.py leader
```

## Results
Writeup is in `Github_MCMC.pdf`. Final results are in `results/repos.csv` and `results/users.csv`.