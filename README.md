# BMW sale price project

The report is in `bmw_analysis.pdf`. The main source file is the
notebook `bmw_analysis.ipynb`. Functions for creating diagrams are
contained in the `draw_diagrams.py` file. This file should be in the
same directory as the notebook file when it is run.


## Prerequisites

The dataset can be downloaded using

```
mkdir datasets
wget -O datasets/bmw.csv https://raw.githubusercontent.com/datacamp/careerhub-data/master/BMW%20Used%20Car%20Sales/bmw.csv
```

Dependencies can be installed using (optionally making a new conda
environment first)

```
conda install numpy pandas matplotlib seaborn sklearn
```

For making the diagrams the following dependencies are needed
```
pip install diagrams
sudo apt install graphviz # for Ubuntu
```
