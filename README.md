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

For making the diagrams, graphviz is needed. To install in e.g. Ubuntu use
```
pip install graphviz
sudo apt install graphviz # for Ubuntu
```


## Running the webserver

The flask and flask-restful packages are needed to run the webserver
```
conda install flask flask-restful
```

Before running the server, the notebook needs to be run, to output the
`bmw_linreg_model.pckl` file which is needed by the webserver. The
server can then by run using
```
python flask_app.py
```

In production the server should be run through a WSGI layer, using
e.g. gunicorn (installable as `pip install gunicorn`) as
```
gunicorn flask_app:app
```
