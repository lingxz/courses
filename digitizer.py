import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import digits_classifier
from constants import THRESHOLDS

GRAY = np.array([0.52549022, 0.52549022, 0.52549022, 1.])
BLUE = np.array([79., 129., 189., 255]) / 255
RED = np.array([192., 80., 77., 255.]) / 255


class ExamHistogram:

    def __init__(self, subject, year):
        self.year = year
        self.subject = subject
        if year >= 2015 and subject == 'astro':
            self.subject = 'asp'  # cos they changed the shortform for this year zzz 
        if year < 2015 and subject == 'proj3':
            self.subject = 'BPrj'
        if year < 2015 and subject == 'proj4':
            self.subject = 'MPrj'
        if year < 2015 and subject == 'plp':
            self.subject = 'Plasma'
        if year < 2015 and subject == 'msm2':
            self.subject = 'MSM'
        if year < 2015 and subject == 'sm':
            self.subject = 'StatMech'
        self.graph_top, self.graph_left, self.graph_right, self.graph_bottom = [None, None, None, None]
        self.data = []
        # url = "https://www.imperial.ac.uk/physics/dugs/ExamStats/figures{}/{}.png".format(str(year)[-2:], self.subject)
        # print(url)
        path = "images/{}-{}.png".format(self.subject, year)
        print(path)
        self.initialize(path)

    def initialize(self, url):
        try:
            self.img_data = img = mpimg.imread(url)
            print("img loaded")
        except:
            self.data = None
            return

        rows, columns, rgba = img.shape
        for index, row in enumerate(img):
            if np.isclose(1., row[rows // 2][0]):
                # border has ended
                self.border_end = border_end = index
                break
        for index, row in enumerate(img[border_end:]):
            if not np.isclose(1., row[rows // 2][0]):
                # graph starts here
                self.graph_top = border_end + index
                gray2 = np.array([0.624, 0.624, 0.624, 1.])
                for col, pixel in enumerate(row[border_end:]):
                    if np.allclose(pixel, GRAY, atol=0.01) or np.allclose(pixel, gray2, atol=0.01):
                        self.graph_left = border_end + col
                        break
                for col, pixel in enumerate(np.flipud(row)[border_end:]):
                    if np.allclose(pixel, GRAY, atol=0.2):
                        self.graph_right = columns - 1 - col - border_end
                        break
                break
        if not self.graph_left or self.graph_left < 30 or self.graph_left > 70:
            self.graph_left = 40
        if self.year == 2016 and self.subject in ['cos', 'cpp', 'essay3', 'fqm', 'lasers', 'sp']:
            # hotfix
            self.graph_left = 48
        if self.year == 2013 and self.subject in ['BPrj']:
            self.graph_left = 48
        if self.year == 2014 and self.subject in ['astro']:
            self.graph_left = 48
        if not self.graph_right or self.graph_right <= self.graph_left:
            self.graph_right = img.shape[1] - 22

        # print(self.graph_left, self.graph_right)
        for index, row in enumerate(np.flipud(img)[border_end:]):
            # find where the graph ends
            line = row[self.graph_left + 10:self.graph_right - 10]
            expected1 = np.array([GRAY for i in range(len(line))])
            expected2 = np.array([[0.76,0.76,0.76,1.] for i in range(len(line))])
            if np.allclose(line, expected1, atol=0.2) or np.allclose(line, expected2, atol=0.2):
                self.graph_bottom = rows - 1 - index - border_end
                break
        if not self.graph_bottom or self.graph_bottom <= self.graph_top:
            self.graph_bottom = len(img) - 74
        self.digitize_barchart()

    def digitize_barchart(self):
        img = self.img_data
        x_interval = (self.graph_right - self.graph_left) / 10.

        # find largest number
        if self.graph_left > 50:  # 3 digits
            left_slice = 50
        elif self.graph_left > 40:  # 2 digits
            left_slice = 40
        elif self.graph_left > 30:  # 1 digit
            left_slice = 30
        else:
            left_slice = self.graph_left - self.border_end
        number_img = img[self.graph_top - 10:self.graph_top + 10, self.graph_left - left_slice:self.graph_left - 5]
        fig = plt.imshow(number_img)
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        current_fig = plt.gcf()
        ax = current_fig.axes[0]
        ax.set_aspect('equal')
        size = current_fig.get_size_inches() * current_fig.dpi
        current_fig.set_size_inches(2 * size[0] / size[1], 2)
        plt.savefig("number.png", bbox_inches='tight')
        
        largest = digits_classifier.findDigits('number.png')
        # largest = 14

        def get_barchart_value(x, y, color):
            pixel = img[y, x]
            if not np.allclose(pixel, color, atol=0.01):
                return 0
            column = img[:, x][self.graph_top:self.graph_bottom - 5]
            total = self.graph_bottom - self.graph_top
            for index, p in enumerate(np.flipud(column)):
                if not np.allclose(p, color):
                    return int(round((index + 5) / total * largest))

        def get_unscaled_value(n):
            # the unscaled scores
            x = int(self.graph_left + n * x_interval + x_interval / 2 - 9)  # 9 is just agar agar
            y = self.graph_bottom - 5  # 5 is also agar agar
            return get_barchart_value(x, y, BLUE)

        def get_scaled_value(n):
            x = int(self.graph_left + n * x_interval + x_interval / 2 + 9)
            y = self.graph_bottom - 5
            return get_barchart_value(x, y, RED)

        self.data = []
        for markrange in range(10):  # there are 10 x intervals
            unscaled_value = get_unscaled_value(markrange)
            scaled_value = get_scaled_value(markrange)
            self.data.append((unscaled_value, scaled_value))
        print(self.data)
