# main.py
import cv2
import pytesseract
import matplotlib.pyplot as plt
import re
import os

# --- Укажи путь к tesseract, если он не в PATH (Windows пример):
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Буквы украинских номеров (КИРИЛЛИЦА, не латиница!)
CYR = "АВЕІКМНОРСТХ"
LAT = "ABEIKMHOPCTX"            # латинские "двойники"
DIG = "0123456789"

lat2cyr = str.maketrans({
    "A": "А", "B": "В", "E": "Е", "I": "І", "K": "К", "M": "М",
    "H": "Н", "O": "О", "P": "Р", "C": "С", "T": "Т", "X": "Х"
})

def ask_image_path() -> str:
    """
    Спросить путь в консоли. Если пусто — открыть диалог выбора файла (tkinter).
    """
    p = input("Введите путь к фото (или нажмите Enter, чтобы выбрать в окне): ").strip().strip('"')
    if p:
        return p
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk(); root.withdraw()
        p = filedialog.askopenfilename(title="Выберите фото номера",
                                       filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff"), ("All files", "*.*")])
        return p or ""
    except Exception:
        return ""

def open_img(img_path: str):
    if not img_path or not os.path.exists(img_path):
        raise FileNotFoundError(f"Файл не найден: {img_path or '(путь пуст)'}")
    img = cv2.imread(img_path)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {img_path}")
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb

def carplate_extract(image, cascade):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    rects = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 20))
    if len(rects) == 0:
        raise RuntimeError("Номер не найден на изображении (детектор ничего не дал).")
    # самый большой прямоугольник
    x, y, w, h = max(rects, key=lambda r: r[2] * r[3])
    pad = 5
    h_img, w_img = image.shape[:2]
    x1 = max(0, x + pad); y1 = max(0, y + pad)
    x2 = min(w_img, x + w - pad); y2 = min(h_img, y + h - pad)
    roi = image[y1:y2, x1:x2]
    if roi.size == 0:
        raise RuntimeError("ROI пустой после обрезки.")
    return roi

def enlarge_img(image, scale_percent=200):
    width = max(1, int(image.shape[1] * scale_percent / 100))
    height = max(1, int(image.shape[0] * scale_percent / 100))
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)

def preprocess_for_ocr(roi_rgb):
    gray = cv2.cvtColor(roi_rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.medianBlur(gray, 3)
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return bw

def normalize_plate(raw: str) -> str:
    s = raw.upper().strip().replace(" ", "").replace("\n", "")
    # латиницу → кириллицу
    s = s.translate(lat2cyr)

    # Исправить частые путаницы по позициям (LLNNNNLL)
    def fix_letter(ch): return {"0": "О", "1": "І"}.get(ch, ch)
    def fix_digit(ch):  return {"О": "0", "І": "1"}.get(ch, ch)

    if len(s) >= 8:
        lst = list(s)
        for i in (0, 1, 6, 7):   # буквы
            if lst[i] in "01":
                lst[i] = fix_letter(lst[i])
        for i in (2, 3, 4, 5):   # цифры
            if lst[i] in "ОІ":
                lst[i] = fix_digit(lst[i])
        s = "".join(lst)

    # оставить только кириллицу из набора + цифры
    s = "".join(ch for ch in s if (ch in CYR) or ch.isdigit())

    # Проверить шаблон LLNNNNLL (кириллица)
    if re.fullmatch(rf"[{CYR}]{2}\d{4}[{CYR}]{2}", s):
        return s
    return s  # если не идеально совпало — вернём как есть для просмотра

def main():
    try:
        img_path = ask_image_path()
        img = open_img(img_path)

        cascade_path = cv2.data.haarcascades + "haarcascade_russian_plate_number.xml"
        cascade = cv2.CascadeClassifier(cascade_path)
        if cascade.empty():
            raise RuntimeError(f"Не удалось загрузить каскад: {cascade_path}")

        roi = carplate_extract(img, cascade)
        roi_big = enlarge_img(roi, 200)
        roi_for_ocr = preprocess_for_ocr(roi_big)

        # Показать найденную область (слева — цвет, справа — бинаризация)
        plt.figure(figsize=(10, 4))
        plt.subplot(1, 2, 1); plt.axis('off'); plt.title("ROI (увеличено)"); plt.imshow(roi_big)
        plt.subplot(1, 2, 2); plt.axis('off'); plt.title("ROI для OCR"); plt.imshow(roi_for_ocr, cmap='gray')
        plt.tight_layout(); plt.show()

        # OCR: украинский + английский, белый список
        config = f"--psm 7 --oem 3 -l eng+ukr -c tessedit_char_whitelist={CYR+LAT+DIG}"
        raw_text = pytesseract.image_to_string(roi_for_ocr, config=config)
        plate = normalize_plate(raw_text)

        print("\n==== Результат OCR ====")
        print("Сырый вывод:", repr(raw_text))
        print("Нормализовано:", plate if plate else "(пусто)")
    except Exception as e:
        print(f"\n[Ошибка] {e}")

if __name__ == "__main__":
    main()
