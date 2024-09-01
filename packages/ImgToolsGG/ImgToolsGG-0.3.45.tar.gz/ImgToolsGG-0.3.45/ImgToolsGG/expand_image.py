
from PIL import Image
import os


# 对于一个  1365*2048 的图片，进行复制3次
def duplicate_and_combine_horizontally(image_path):
    # 打开原始图片
    original_image = Image.open(image_path)

    # 获取原始图片的尺寸
    width, height = original_image.size

    # 创建一个新图片，宽度是原始宽度的3倍，高度不变
    new_image_width = 3 * width
    new_image = Image.new('RGB', (new_image_width, height))

    # 将原始图片粘贴到新图片上，复制3次
    new_image.paste(original_image, (0, 0))
    new_image.paste(original_image, (width, 0))
    new_image.paste(original_image, (2 * width, 0))

    # 从输入文件名构造输出文件名
    base_name = os.path.splitext(os.path.basename(image_path))[0]  # 去除文件扩展名
    output_filename = f"{base_name}_combined.jpg"

    # 保存新图片
    new_image.save(output_filename)  # 保存图片到文件
    print(f"Image saved as {output_filename}")


# 使用函数，传入图片路径
duplicate_and_combine_horizontally('../imgs/2.jpg')
duplicate_and_combine_horizontally('y.jpg')

