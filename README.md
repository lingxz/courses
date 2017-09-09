# Compare all the courses

Uses flask, numpy, pandas, bokeh, and opencv. 

## Run the thing

To run locally, clone this repo, install all the necessary modules by 

```
pip install -r requirements.txt
```

Then run the app by doing

```python
python main.py
```
and go to `localhost:5000` to see the app. This uses the scraped data saved in `alldata.csv`. 

For full dev (including scraping the data), install the things by 

```python
pip install -r requirements.dev.txt
```

`main.py`: runs the server

`digits_classifier.py`: uses opencv to recognize the digits, to run it locally you might need to change the font file path

`digitizer.py`: digitizes the graph by using a bunch of hard coded parameters and saves data into `alldata.csv`

`analyze.py`: analyzes the data from `alldata.csv`

## API

There is an API, you can get the data for each subject, in case you want to do something else with it:

```python
GET /api/module/<module>
```
where `<module>` is one of the keys of `SUBJECTS_LONG_TO_SHORT` in [this file](constants.py). 

