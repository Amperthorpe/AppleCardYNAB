from PIL import Image, ImageDraw
import pytesseract
import YNAB
import datetime, time
from classes import YNABTransaction
from edges import cropped_trans

PADDING = (
    30  # Distance between "Latest Card Transactions" text, and top of first transaction
)
TRANS_HEIGHT = 228  # Distance between transactions.

img_raw = Image.open("ac5.jpg")
box = (250, 0, img_raw.width - 150, img_raw.height)  # Remove distracting borders
img_full = img_raw.crop(box)

draw_crop = ImageDraw.ImageDraw(img_full)  # DEBUG


def draw_height(y):  # DEBUG
    draw_crop.line([(0, y), (img_full.width, y)], "Red")


transaction_list = []
for img in cropped_trans(img_full):
    # OCR each transaction seperately, to prevent errors.
    broken_trans_flag = False
    transaction = YNABTransaction()
    text: str = pytesseract.image_to_string(img)
    text: list = text.split("\n")
    for i, li in enumerate(text):
        if not li:
            text.pop(i)

    # First line, name + outflow
    split_li = text[0].split(" ")
    name = " ".join(split_li[:-1])
    transaction.memo = name
    outflow = split_li[-1]
    if not transaction.set_outflow(outflow):
        broken_trans_flag = True

    # Second line is not used.
    # Third line, date.
    # Date can be relative hours, "yesterday", a day of the week, or a date in m/d/yy format.

    weekdays_dict = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    now = datetime.datetime.now()  # TODO: this prob needs timezone info
    text_date = text[2]
    if text_date.endswith("hours ago"):
        hours = float(text_date.split(" ")[0])  # Get number at front of line.
        hours_delta = datetime.timedelta(hours=hours)
        date = now - hours_delta
        transaction.local_date = date

    elif text_date == "Yesterday":
        date = now - datetime.timedelta(days=1)
        transaction.local_date = date

    elif text_date in weekdays_dict.keys():
        days_since: int = (now.weekday() - weekdays_dict[text_date]) % 7
        date = now - datetime.timedelta(days=days_since)
        transaction.local_date = date

    elif "/" in text_date:
        date = datetime.datetime.strptime(text_date, r"%d/%m/%y")
        transaction.local_date = date
    else:
        print(f"Unable to parse date: \n{text}\n")
        broken_trans_flag = True

    if not broken_trans_flag:
        transaction_list.append(transaction)

print("################################")
if broken_trans_flag:
    print("##Unreadable Transaction Skipped##")

YNAB.YNAB_post(transaction_list)
