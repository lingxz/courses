import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps


def createDigitsModel(fontfile, digitheight):
    # create training model based on the given TTF font file
    ttfont = ImageFont.truetype(fontfile, digitheight)
    samples = np.empty((0, digitheight * (digitheight // 2)))
    responses = []
    for n in range(10):
        pil_im = Image.new("RGB", (digitheight, digitheight * 2))
        ImageDraw.Draw(pil_im).text((0, 0), str(n), font=ttfont)
        pil_im = pil_im.crop(pil_im.getbbox())
        pil_im = ImageOps.invert(pil_im)
        #pil_im.save(str(n) + ".png")

        # convert to cv image
        cv_image = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGRA)
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

        roi = cv2.resize(thresh, (digitheight, digitheight // 2))
        responses.append(n)
        sample = roi.reshape((1, digitheight * (digitheight // 2)))
        samples = np.append(samples, sample, 0)

    samples = np.array(samples, np.float32)
    responses = np.array(responses, np.float32)

    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    return model


def findDigits(imagefile, fontfile="C:\\Windows\\Fonts\\Calibri.ttf"):
    # digit recognition part
    im = cv2.imread(imagefile)
    im = im[20:-20, 20:-20]
    out = np.zeros(im.shape, np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)
    _, contours, hierarchy = cv2.findContours(
        thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    digitheight = max([cv2.boundingRect(i)[3] for i in contours])
    model = createDigitsModel(fontfile, digitheight)
    numbers = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if h > w and h > (digitheight * 9) / 10 and h < (digitheight * 11) / 10:  # +/-20%
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 1)
            roi = thresh[y:y + h, x:x + w]  # crop
            roi = cv2.resize(roi, (digitheight, digitheight // 2))
            roi = roi.reshape((1, digitheight * (digitheight // 2)))
            roi = np.float32(roi)
            retval, results, neigh_resp, dists = model.findNearest(roi, k=1)
            res = int(results[0][0])
            numbers.append((x, res))
    numbers.sort(key=lambda x: x[0])
    value = int(''.join([str(x[1]) for x in numbers]))
    return value
