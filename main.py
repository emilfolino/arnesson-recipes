import csv
import cv2
import pytesseract

"""
https://www.opcito.com/blogs/extracting-text-from-images-with-tesseract-ocr-opencv-and-python
https://pyimagesearch.com/2021/11/15/tesseract-page-segmentation-modes-psms-explained-how-to-improve-your-ocr-accuracy/
https://medium.com/geekculture/tesseract-ocr-understanding-the-contents-of-documents-beyond-their-text-a98704b7c655

Använd nlkt och regexp för att plocka ut title och andra sektioner https://www.h2kinfosys.com/blog/nltk-regular-expressions/
https://www.nltk.org/api/nltk.parse.html
"""
UNICODE_1 = 49
UNICODE_2 = 50
CONFIG = r'--oem 3 --psm 3'

def run_img_through_tesseract(img):
    details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=CONFIG, lang="swe")
    # details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DATAFRAME, config=CONFIG, lang="swe")
    # details.to_csv("data.csv")
    # exit()
    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
        if int(details['conf'][sequence_number]) >30:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
            image = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return details, image

def parse_text(details):
    parsed_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word!='':
            word_list.append(word)
            last_word = word
        if (last_word!='' and word == '') or (word==details['text'][-1]):
            parsed_text.append(word_list)
            word_list = []
    return parsed_text



image = cv2.imread("recipe.jpeg")

#converting image into gray scale image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# converting it to binary image by Thresholding
# this step is require if you have colored image because if you skip this part
# then tesseract won't able to detect text correctly and this will give incorrect result
threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

data_orig = run_img_through_tesseract(image)
data_grey = run_img_through_tesseract(threshold_img)

# display image
cv2.imshow("original image - 1", data_orig[1])
cv2.imshow("greyd image - 2", data_grey[1])

unicode_key = cv2.waitKey(0)
cv2.destroyAllWindows()

if unicode_key == UNICODE_1:
    text = parse_text(data_orig[0])
elif unicode_key == UNICODE_2:
    text = parse_text(data_orig[1])
else:
    print("Unknown key. Exiting!")
    exit(1)

with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(text)
