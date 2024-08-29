from PIL import Image, ImageEnhance
import os
import random

def rotate_and_adjust_properties(input_folder, output_folder, output_num):
    original_files = os.listdir(input_folder)

    for filename in original_files:
        if not filename.endswith(".jpg"):
            continue

        img = Image.open(os.path.join(input_folder, filename))

        # 生成随机属性图像
        for i in range(1, 11):
            # 随机亮度调整
            enhancer_brightness = ImageEnhance.Brightness(img)
            bright_img = enhancer_brightness.enhance(random.uniform(0.5, 1.5))

            # 随机对比度调整
            enhancer_contrast = ImageEnhance.Contrast(img)
            contrast_img = enhancer_contrast.enhance(random.uniform(0.5, 1.5))

            # 随机灰度调整
            enhancer_grayscale = ImageEnhance.Color(contrast_img)
            grayscale_img = enhancer_grayscale.enhance(random.uniform(0.2, 0.8))
            grayscale_img = grayscale_img.convert("L")  # 转换为灰度图像

            # 随机饱和度调整
            enhancer_saturation = ImageEnhance.Color(grayscale_img)
            saturated_img = enhancer_saturation.enhance(random.uniform(0.5, 1.5))

            new_name = f"properties_{i}_{filename}"
            saturated_img.save(os.path.join(input_folder, new_name))

        # 旋转和调整属性
        for i in range(1, output_num + 1):
            for j in range(1, 11):
                angle = 360 * i / output_num
                properties_filename = f"properties_{j}_{filename}"
                properties_img = Image.open(os.path.join(input_folder, properties_filename))
                rotated_properties_img = properties_img.rotate(angle)

                new_name = os.path.join(output_folder, f"{os.path.splitext(properties_filename)[0]}_{i}.jpg")
                rotated_properties_img.save(new_name)

        print(f"{filename} complete!")

    print("All complete!")

# 使用属性参数来控制是否生成属性变化图像
rotate_and_adjust_properties(input_folder="./raw/", output_folder="./out/", output_num=30)

remove_raw_file = input("Remove raw files? (y/n)").lower() == "y"

if remove_raw_file:
    # 使用列表推导式来移除raw文件夹中的文件
    [os.remove(os.path.join("./raw/", filename)) for filename in os.listdir("./raw/")]
    print("Raw files removed!")

rename_suffix = input("Suffix for renaming: ")
# 使用列表推导式来重命名out文件夹中的文件
[os.rename(os.path.join("./out/", filename), os.path.join("./out/", f"{rename_suffix} ({count}).jpg")) for count, filename in enumerate(os.listdir("./out/"))]
print("Files renamed!")
