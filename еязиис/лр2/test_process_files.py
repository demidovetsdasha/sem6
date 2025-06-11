import os
import shutil
import time
import matplotlib.pyplot as plt
from data_extractor import DataExtractor, process_files

# Пути к папкам
input_dir = "test_input"
output_dir = "test_output"
output_xml = "xml_test_output"

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir, exist_ok=True)

data_extractor = DataExtractor()

all_files = sorted(os.listdir(input_dir))

times = []
num_files_list = []

for i, file_name in enumerate(all_files, start=1):
    file_path = os.path.join(input_dir, file_name)
    dest_path = os.path.join(output_dir, file_name)

    shutil.copy(file_path, dest_path)

    start_time = time.time()
    process_files(output_dir, output_xml, data_extractor)
    end_time = time.time()

    elapsed_time = end_time - start_time
    times.append(elapsed_time)
    num_files_list.append(i)

    print(f"Обработано {i} файлов за {elapsed_time:.4f} секунд")

plt.figure(figsize=(8, 5))
plt.plot(num_files_list, times, marker='o', linestyle='-')
plt.xlabel("Количество файлов")
plt.ylabel("Время обработки (сек)")
plt.title("Зависимость времени обработки от количества файлов")
plt.grid(True)
plt.show()
