import numpy as np
from scipy.ndimage import convolve, gaussian_filter
from PIL import Image
import argparse

# ---------- НАСТРАИВАЕМЫЕ ПАРАМЕТРЫ OPC ----------
# PSF (гауссово размытие в пикселях)
sigma = 1.5                  # сигма гауссова ядра (подбирается экспериментально)
kernel_size = int(6 * sigma) | 1  # размер ядра (нечётный)

# Процесс проявления
threshold = 0.7             # порог засветки резиста (0..1)
alpha = 30.0                 # крутизна сигмоиды (контраст)

# Оптимизация
learning_rate = 1.0          # темп обучения (может потребоваться подбор)
num_iterations = 200         # число итераций
beta = 0.001                 # коэффициент бинаризующего штрафа (чем выше, тем «бинарнее» маска)

# Порог финальной бинаризации маски (обычно 0.5)
final_threshold = 0.5

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def create_gaussian_kernel(sigma, size):
    """Создаёт нормированное 2D-гауссово ядро."""
    ax = np.arange(-size//2 + 1., size//2 + 1.)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
    return kernel / kernel.sum()

def apply_opc(target_image_path, output_image_path):
    # Загрузка таргета (PNG, ч/б или серый)
    img = Image.open(target_image_path).convert('L')   # 0..255
    target = (np.array(img, dtype=np.float32) > 128).astype(np.float32)  # 0/1

    # Создание PSF-ядра
    psf = create_gaussian_kernel(sigma, kernel_size)

    # Начальная маска = таргет (можно также размытый вариант)
    mask = target.copy()

    # Оптимизация градиентным спуском
    for it in range(num_iterations):
        # 1. Аэральное изображение: свёртка маски с PSF
        aerial = convolve(mask, psf, mode='constant', cval=0.0)

        # 2. Мягкий порог (предсказанный рисунок)
        p = sigmoid(alpha * (aerial - threshold))

        # 3. Функция потерь: MSE + бинарный штраф
        diff = p - target
        loss_mse = np.mean(diff ** 2)
        loss_bin = np.mean(mask * (1.0 - mask))
        loss = loss_mse + beta * loss_bin

        if it % 20 == 0:
            print(f"Итерация {it:3d}, loss = {loss:.6f} (mse={loss_mse:.6f}, bin={loss_bin:.6f})")

        # 4. Градиент dL/dI (производная MSE по I)
        # dL/dp = 2*(p - T)   ;   dp/dI = alpha * p * (1-p)
        dL_dI = 2.0 * diff * alpha * p * (1.0 - p)

        # 5. Градиент dL/dM = dL/dI ∗ flip(psf)  (свёртка с перевёрнутым ядром)
        flipped_psf = np.flip(psf)
        dL_dM = convolve(dL_dI, flipped_psf, mode='constant', cval=0.0)

        # 6. Добавляем градиент от бинарного штрафа: d/dM (M*(1-M)) = 1 - 2M
        dL_dM += beta * (1.0 - 2.0 * mask)

        # 7. Обновление маски (градиентный спуск)
        mask -= learning_rate * dL_dM

        # Ограничение диапазона [0, 1]
        mask = np.clip(mask, 0.0, 1.0)

    # Финальная бинаризация маски
    mask_binary = (mask > final_threshold).astype(np.uint8) * 255

    # Сохранение результата
    result = Image.fromarray(mask_binary, mode='L')
    result.save(output_image_path)
    print(f"Скорректированная маска сохранена в {output_image_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OPC корректор для безмасочной литографии")
    parser.add_argument("input", help="Путь к исходному PNG-шаблону (ч/б)")
    parser.add_argument("output", help="Путь для сохранения скорректированного PNG")
    args = parser.parse_args()

    apply_opc(args.input, args.output)