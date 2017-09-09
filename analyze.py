import numpy as np
import io
import csv
import os
import pandas as pd
from ast import literal_eval
from constants import SUBJECTS_LONG_TO_SHORT, SUBJECTS_SHORT_TO_LONG, THRESHOLDS, PASS_INDEX, YEARS
import shutil

class Analysis:

    def __init__(self):
        self.subjects = list(SUBJECTS_SHORT_TO_LONG.keys())
        self.years = YEARS
        self.load_data()

    def create_csv(self):
        import digitizer
        self.histograms = []
        for subject in self.subjects:
            hists = []
            print(subject)
            for year in self.years:
                print(year)
                s = self.convert_to_short(subject)
                hist = digitizer.ExamHistogram(s, year)
                hists.append(hist.data)
            self.histograms.append(hists)
        with open('alldata.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.years)
            writer.writerows(self.histograms)

    def get_images(self):
        import requests
        for subject in self.subjects:
            for year in self.years:
                s = subject
                print(s, year)
                if year >= 2015 and subject == 'astro':
                    s = 'asp'  # cos they changed the shortform for this year zzz 
                if year < 2015 and subject == 'proj3':
                    s = 'BPrj'
                if year < 2015 and subject == 'proj4':
                    s = 'MPrj'
                if year < 2015 and subject == 'plp':
                    s = 'Plasma'
                if year < 2015 and subject == 'msm2':
                    s = 'MSM'
                if year < 2015 and subject == 'sm':
                    s = 'StatMech'
                url = "https://www.imperial.ac.uk/physics/dugs/ExamStats/figures{}/{}.png".format(str(year)[-2:], s)
                print(url)
                response = requests.get(url, stream=True)
                filename = "{}-{}.png".format(s, year)
                print(response.status_code)
                if response.status_code == 200:
                    with open('images/' + filename, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)

    def load_data(self):
        try:
            with open('alldata.csv', 'r') as f:
                reader = csv.reader(f)
                unprocessed_data = list(reader)[1:]
            data = []
            for idx, row in enumerate(unprocessed_data):
                new_row = []
                for item in row:
                    if item == '':
                        new_row.append(np.NaN)
                    else:
                        new_row.append(literal_eval(item))
                data.append(new_row)
            self.histograms = data
        except FileNotFoundError:
            if not os.listdir('images'):
                self.get_images()
            self.create_csv()

    def display_all(self):
        for idx, s in enumerate(self.subjects):
            stats = self.display_subject(idx)
            print(stats)

    def convert_to_short(self, subject):
        if subject in SUBJECTS_LONG_TO_SHORT:
            return SUBJECTS_LONG_TO_SHORT[subject]
        elif subject in SUBJECTS_SHORT_TO_LONG:
            return subject
        else:
            raise ValueError('The subject {} does not exist!'.format(subject))

    def compare_subjects(self, subjects, threshold=70, after_scaling=True):
        processed_subjects = [self.convert_to_short(s) for s in subjects]
        indices = [self.subjects.index(s) for s in processed_subjects]
        for idx in indices:
            stats = self.display_subject(idx, threshold, after_scaling)
            print(stats)

    def display_subject(self, idx, threshold, after_scaling):
        hists = self.histograms[idx]
        subject_name = SUBJECTS_SHORT_TO_LONG[self.subjects[idx]]
        hcs = [HistogramContainer(h, threshold, after_scaling) for h in hists]
        sc = StatsContainer(threshold, hcs)
        rv = io.StringIO()
        rv.write("\n")
        rv.write("Displaying data for {}:\n".format(subject_name))
        rv.write("Average proportion of passes is {:.3f} with a standard deviation of {:.3f}.\n"
                 .format(np.nanmean(sc.pass_percentage), np.nanstd(sc.pass_percentage)))
        rv.write("Average proportion of {} and above is {:.3f} with a standard deviation of {:.3f}.\n"
                 .format(threshold, np.nanmean(sc.good_percentage), np.nanstd(sc.good_percentage)))
        rv.seek(0)
        return {
            'description': rv.read(),
            'df': sc.df,
        }


class HistogramContainer:

    def __init__(self, data, threshold, after_scaling):
        if threshold % 10 != 0:
            raise ValueError(
                "Threshold of {} is not allowed. Threshold must be a multiple of 10".format(threshold))
        if type(after_scaling) is not bool:
            raise ValueError('after_scaling variable should be a boolean')
        self.data = data
        self.threshold = threshold
        self.after_scaling = after_scaling

    def total(self):
        if not isinstance(self.data, list):
            return np.NaN
        return np.sum(self.data) // 2

    def num_above_threshold(self):
        if not isinstance(self.data, list):
            return np.NaN
        th = THRESHOLDS.index(self.threshold)
        i = 1 if self.after_scaling else 0
        a = [d[i] for d in self.data]
        return sum(a[th:])

    def num_pass(self):
        if not isinstance(self.data, list):
            return np.NaN
        i = 1 if self.after_scaling else 0
        a = [d[i] for d in self.data]
        return sum(a[PASS_INDEX:])

    def mode(self):
        if not isinstance(self.data, list):
            return np.NaN
        i = 1 if self.after_scaling else 0
        a = [d[i] for d in self.data]
        return np.argmax(np.array(a))

    def median(self):
        if not isinstance(self.data, list):
            return np.NaN
        i = 1 if self.after_scaling else 0
        a = np.array([d[i] for d in self.data])
        cumsum = np.cumsum(a)
        half = self.total() // 2
        return [n for n, i in enumerate(cumsum) if i >= half][0]


class StatsContainer:

    def __init__(self, threshold, histograms):
        self.histograms = histograms
        self.threshold = threshold

        self.passes = np.array([hist.num_pass() for hist in histograms])
        self.pass_percentage = np.array(
            [hist.num_pass() / hist.total() for hist in histograms])
        self.modes = np.array([hist.mode() for hist in histograms])
        self.mode_ranges = []
        for mode in self.modes:
            try:
                self.mode_ranges.append(THRESHOLDS[int(mode)])
            except:
                self.mode_ranges.append(np.NaN)

        self.medians = np.array([hist.mode() for hist in histograms])
        self.median_ranges = []
        for median in self.medians:
            try:
                self.median_ranges.append(THRESHOLDS[int(median)])
            except:
                self.median_ranges.append(np.NaN)
        self.totals = np.array([hist.total() for hist in histograms])
        self.good = np.array([hist.num_above_threshold()
                              for hist in histograms])
        self.good_percentage = np.array(
            [hist.num_above_threshold() / hist.total() for hist in histograms])
        self.get_stats_df()

    def get_stats_df(self):
        threshold_key = "Above {}".format(self.threshold)
        threshold_key_p = "Above {} percentage".format(self.threshold)
        d = {
            'Passes': self.passes,
            'Pass percentage': self.pass_percentage,
            'Modes': self.mode_ranges,
            'Medians': self.median_ranges,
            threshold_key: self.good,
            threshold_key_p: self.good_percentage,
            'Total students': self.totals,
        }
        self.df = pd.DataFrame(d, index=YEARS).dropna(how="all")
        print(self.df)


# a = Analysis()
# a.compare_subjects(['uni', 'gr'])
