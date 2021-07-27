from PIL import Image
import pytesseract
import cv2
import os

class text_photo:

    async def image_txt(self, filename):
        text = pytesseract.image_to_string(Image.open(filename), lang='rus')
        os.remove(filename)
        return text


    async def run(self, image):
        # image = '5.jpg'

        preprocess = "thresh"

        # загрузить образ и преобразовать его в оттенки серого
        image = cv2.imread(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # проверьте, следует ли применять пороговое значение для предварительной обработки изображения

        if preprocess == "thresh":
            gray = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # если нужно медианное размытие, чтобы удалить шум
        elif preprocess == "blur":
            gray = cv2.medianBlur(gray, 3)

        # сохраним временную картинку в оттенках серого, чтобы можно было применить к ней OCR

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        # загрузка изображения в виде объекта image Pillow, применение OCR, а затем удаление временного файла
        #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        #"C:\Users\Zett\AppData\Local\Programs\Python\Python38 - 32\Scripts"
        #text = pytesseract.image_to_string(Image.open(filename), lang='rus')
        #os.remove(filename)
        text = await self.image_txt(filename)
        return text