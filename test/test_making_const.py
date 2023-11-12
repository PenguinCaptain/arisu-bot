const = {'14': [('77bb3ca5929cb8f6.jpg', 'EXP'), ('545d27d38decbcd1.jpg', 'EXP'), ('ae12c105f6d70230.jpg', 'EXP')], 
        '14.1': [('f3f526bb5400bcb6.jpg', 'EXP')], 
        '14.2': [('6c682b055a448ee8.jpg', 'EXP'), ('bcc407345c4303e4.jpg', 'EXP'), ('e3ed79c8138e2ce2.jpg', 'EXP')], 
        '14.3': [('07c9d14609172cb8.jpg', 'EXP'), ('c08b3258022089a0.jpg', 'EXP'), ('6e46224559e92381.jpg', 'EXP'), ('84a431784a70c851.jpg', 'EXP')], 
        '14.4': [('a9b25545cd935cc9.jpg', 'EXP'), ('9b0555e529aef749.jpg', 'EXP'), ('6b34df2de18884b8.jpg', 'EXP'), ('f466786cc3deffca.jpg', 'EXP')]}
    
keys = const.keys()

height = 0

for key in keys:
    height += len(const[key]) // 10 + 1

width = 60 + 60 * 10

height = 140 + 60 * height

print(width, height)

from PIL import Image

img = Image.open("./src/chunithm/sp_bg.jpeg")

img = img.resize((width, height))

logo = Image.open("./src/chunithm/logo_sp.png")

img.paste(logo, (20, 20), logo)

img.show()
# for key in keys:
    