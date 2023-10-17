from PIL import Image
import io
import base64

image = Image.open("E:\Documents\eventschedule\static\img\logo.png")  

img_byte_array = io.BytesIO()
image.save(img_byte_array, format="png")  

img_base64 = base64.b64encode(img_byte_array.getvalue()).decode('utf-8')

img_data = base64.b64decode(img_base64)

img_byte_array = io.BytesIO(img_data)

image = Image.open(img_byte_array)

image.show()
