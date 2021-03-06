# BMW sale price project

The report is in `bmw_analysis.pdf`. The main source file is the
notebook `bmw_analysis.ipynb`.


## Prerequisites

The dataset can be downloaded using

```
mkdir datasets
wget -O datasets/bmw.csv https://raw.githubusercontent.com/datacamp/careerhub-data/master/BMW%20Used%20Car%20Sales/bmw.csv
```

Dependencies can be installed using (optionally making a new conda
environment first)

```
conda install numpy pandas matplotlib seaborn scikit-learn notebook
```

The project also depends on the local `multi_model.py` module.

For making the diagrams (optional), the `draw_diagrams.py` file should
be in the same directory as the notebook file, and graphviz is
needed. To install in e.g. Ubuntu use

```
pip install graphviz
sudo apt install graphviz # for Ubuntu
```


## Running the webserver (optional)

The flask and flask-restful packages are needed to run the webserver,
in addition to the dependencies mentioned above

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

An example front end is implemented in the `predict_price.html` and
`bmw_fetcher.js` files. The front end should work should work by
simply opening the html file in a browser, while the javascript script
is in the same directory. The response after the first query might
take around 10 seconds to load, but subsequent requests should be
faster.

The `bmw_fetcher.js` has the URL for a version
of the flask app deployed to Heroku hardcoded into it, as well as the
feature ranges from the `feature_ranges.json` output file from the
notebook. If you want to test against a locally run server, or retrain
the model with new features, the relevant variables in
`bmw_fetcher.js` should be adjusted correspondingly.

## Building the slides

The slides are based on the source file `slides.org`. This file is in
Emacs org-mode format, and should be exported to html using the
[ox-reveal](https://github.com/yjwen/org-reveal) exporter. The figures
can be generated by running the `bmw_analysis.ipynb` notebook.
