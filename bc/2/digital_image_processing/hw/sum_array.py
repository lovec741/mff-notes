# we have a kernel that is filled with ones
# we want to be able to precalculate something so we can use the kernel with O(1) speed for any kernel size

from typing import List
from PIL import Image


def generate_sum_array(img: Image.Image) -> List[List[List[float]]]:
    channels_count = len(img.getbands())
    empty_pixel_value = [0]*channels_count
    single_channel = channels_count == 1
    sum_array = [[None] * img.height for _ in range(img.width)]
    for x in range(img.width):
        for y in range(img.height):
            from_top = sum_array[x][y-1] if y != 0 else empty_pixel_value
            from_left = sum_array[x-1][y] if x != 0 else empty_pixel_value
            overlap = sum_array[x-1][y-1] if x != 0 and y != 0 else empty_pixel_value
            pixel_value = img.getpixel((x,y))
            if not single_channel:
                val = [0]*channels_count
                for i in range(channels_count):
                    val[i] = from_top[i] + from_left[i] + pixel_value[i] - overlap[i]
            else:
                val = from_top + from_left + pixel_value - overlap
            sum_array[x][y] = val
    return sum_array

def process_image(img: Image.Image, kernel_size: int, sum_array: List[List[List[float]]]):
    """kernel size has to be an odd number"""
    kernel_radius = kernel_size // 2
    channels_count = len(img.getbands())
    single_channel = channels_count == 1
    empty_pixel_value = [0]*channels_count
    for x in range(img.width):
        for y in range(img.height):
            # center at x, y
            left_x = x - kernel_radius if x - kernel_radius >= 0 else 0
            top_y = y - kernel_radius if y - kernel_radius >= 0 else 0
            right_x = x + kernel_radius if x + kernel_radius < img.width else img.width - 1
            bottom_y = y + kernel_radius if y + kernel_radius < img.height else img.height - 1

            pixel_count = (right_x - left_x + 1) * (bottom_y - top_y + 1)

            from_top_right = sum_array[right_x][top_y-1] if top_y != 0 else empty_pixel_value
            from_left_bottom = sum_array[left_x-1][bottom_y] if left_x != 0 else empty_pixel_value
            overlap = sum_array[left_x-1][top_y-1] if left_x != 0 and top_y != 0 else empty_pixel_value
            main = sum_array[right_x][bottom_y]
            if not single_channel:
                val = [0]*channels_count
                for i in range(channels_count):
                    val[i] = int((main[i] - from_left_bottom[i] - from_top_right[i] + overlap[i]) / pixel_count)
            else:
                val = int((main - from_left_bottom - from_top_right + overlap) / pixel_count)
            img.putpixel((x,y), tuple(val))

if __name__ == "__main__":
    img = Image.open("test.jpg")
    # img = img.crop((300,300,400,400))
    # img.show()
    sum_array = generate_sum_array(img)
    process_image(img, 3, sum_array)
    img.show()
    process_image(img, 7, sum_array)
    img.show()
    process_image(img, 21, sum_array)
    img.show()
