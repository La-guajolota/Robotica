import cv2
import numpy as np

# Captura de video desde la cámara
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el frame.")
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Separar los canales de color RGB
    b, g, r = cv2.split(frame)
    blue_channel = cv2.merge([b, b, b])
    green_channel = cv2.merge([g, g, g])
    red_channel = cv2.merge([r, r, r])

    # Crear mosaico RGB
    rgb_top_row = np.hstack((frame, blue_channel))
    rgb_bottom_row = np.hstack((green_channel, red_channel))
    rgb_mosaic = np.vstack((rgb_top_row, rgb_bottom_row))

    # Convertir a HSV y separar canales
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    hue_channel = cv2.merge([h, h, h])
    saturation_channel = cv2.merge([s, s, s])
    value_channel = cv2.merge([v, v, v])

    # Crear mosaico HSV
    hsv_top_row = np.hstack((hue_channel, saturation_channel))
    hsv_bottom_row = np.hstack((value_channel, frame))
    hsv_mosaic = np.vstack((hsv_top_row, hsv_bottom_row))

    # Convertir a LAB y separar canales
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    luminance_channel = cv2.merge([l, l, l])
    a_channel = cv2.merge([a, a, a])
    b_channel = cv2.merge([b, b, b])

    # Crear mosaico LAB
    lab_top_row = np.hstack((luminance_channel, a_channel))
    lab_bottom_row = np.hstack((b_channel, frame))
    lab_mosaic = np.vstack((lab_top_row, lab_bottom_row))

    # Convertir a YCrCb y separar canales
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(ycrcb)
    y_channel = cv2.merge([y, y, y])
    cr_channel = cv2.merge([cr, cr, cr])
    cb_channel = cv2.merge([cb, cb, cb])

    # Crear mosaico YCrCb
    ycrcb_top_row = np.hstack((y_channel, cr_channel))
    ycrcb_bottom_row = np.hstack((cb_channel, frame))
    ycrcb_mosaic = np.vstack((ycrcb_top_row, ycrcb_bottom_row))

    # Crear mosaico Grayscale
    gray_channel = cv2.merge([gray, gray, gray])
    gray_mosaic = np.hstack((gray_channel, frame))

    # Mostrar los mosaicos
    cv2.imshow('Mosaico RGB', rgb_mosaic)
    cv2.imshow('Mosaico HSV', hsv_mosaic)
    cv2.imshow('Mosaico LAB', lab_mosaic)
    cv2.imshow('Mosaico YCrCb', ycrcb_mosaic)
    cv2.imshow('Mosaico Grayscale', gray_mosaic)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()