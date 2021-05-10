import os

from django.core.files.base import ContentFile
from django.core.files import File
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
from fpdf import FPDF

from .models import ScanFile


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect


def four_point_transform(img, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    max_width = max(int(width_a), int(width_b))
    height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    max_height = max(int(height_a), int(height_b))
    dst = np.array([[0, 0], [max_width - 1, 0], [max_width - 1, max_height - 1], [0, max_height - 1]], dtype="float32")
    m = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, m, (max_width, max_height))
    return warped


def scan_file(name):
    image_obj = ScanFile.objects.last()
    image = image_obj.photo

    image = np.asarray(bytearray(image.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    cnt = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnt = imutils.grab_contours(cnt)
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)[:5]

    for c in cnt:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            screen_cnt = approx
            break

    warped = four_point_transform(orig, screen_cnt.reshape(4, 2) * ratio)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    t = threshold_local(warped, 11, offset=10, method="gaussian")
    warped = (warped > t).astype("uint8") * 255

    ret, buf = cv2.imencode('.jpg', warped)
    content = ContentFile(buf.tobytes())

    image_obj.scanned_photo.save(f'scanned_{name}.jpg', content)


def convert_to_pdf(image_path, name, image):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(image_path, x=10, y=8, w=100)
    pdf_name = f'static/pdf_files/{name}.pdf'
    pdf.output(pdf_name)
    with open(pdf_name, 'rb') as fi:
        my_file = File(fi)
        image.pdf_file.save(f'{name}.pdf', my_file)
    os.remove(pdf_name)
