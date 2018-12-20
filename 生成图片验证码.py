from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

# 生成随机字母
def rnd_char():
    return chr(random.randint(65, 90))

# 生成随机数字
def rnd_num():
    return random.randint(1, 9)

# 生成随机颜色
def rnd_color():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


def rnd_color_text():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


width = 60 * 4
height = 60
image = Image.new("RGB", (width, height), (255, 255, 255))
print(type(image))
myfont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=36)
draw = ImageDraw.Draw(image)
print(type(draw))
help(ImageDraw.Draw)

for x in range(width):
    for y in range(height):
        draw.point((x, y), rnd_color())

for t in range(4):
    draw.text((60 * t + 10, 10), rnd_char(), font=myfont, fill=rnd_color_text())


image = image.filter(ImageFilter.BLUR)
image.save('code.jpg', 'jpeg')


# help(Image.new)
# image1 = Image.new()
rndChar = random.randint(1, 2)
range(0, 1)
# print(rndChar)
print(range(0, 6, 3))
# help(random)