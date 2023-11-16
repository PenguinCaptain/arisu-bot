from PIL import Image, ImageDraw, ImageFont

def b30single(data):
    color = {
        'Master': (187, 51, 238),
        'Expert': (238, 67, 102),
        'Advanced': (254, 170, 0),
        'Ultima': (0, 0, 0),
        'Basic': (102, 221, 17),
    }

    """
    "title": "Giselle",
    "score": 1007542,
    "difficulty": "Master",
    "id": "c893",
    "const": 14.9,
    "rating": 16.9,
    "token": "99c5e71073e0f616327cf3c490ba2a05",
    "isAllJustice": false,
    "isFullCombo": false
    """
    title = data["title"]
    score = data["score"]
    diff = data["difficulty"]
    rating = data["rating"]
    const = data["const"]
    id = data["id"]
    

    base = Image.new("RGB", (620, 240), (255, 255, 255))
    
    # jacket = Image.open(f'chunithm/jackets/{single_data["jacketFile"]}')
    # jacket = jacket.resize((186, 186))
    # pic.paste(jacket, (32, 28))

    # draw = ImageDraw.Draw(pic)
    # font = ImageFont.truetype('fonts/YuGothicUI-Semibold.ttf', 36)
    # size = font.getsize(musictitle)
    # if size[0] > 365:
    #     musictitle = musictitle[:int(len(musictitle)*(345/size[0]))] + '...'
    # draw.text((240, 27), musictitle, '#000000', font)

    # font = ImageFont.truetype('fonts/FOT-RodinNTLGPro-DB.ttf', 58)
    # draw.text((234, 87), str(single_data['score']), '#000000', font)

    # font = ImageFont.truetype('fonts/SourceHanSansCN-Bold.otf', 38)
    # draw.ellipse((242, 165, 286, 209), fill=color[single_data['musicDifficulty']])
    # draw.rectangle((262, 165, 334, 209), fill=color[single_data['musicDifficulty']])
    # draw.ellipse((312, 165, 356, 209), fill=color[single_data['musicDifficulty']])
    # draw.text((259, 157), str(single_data['playLevel']), (255, 255, 255), font)
    # draw.text((370, 157), '→ ' + str(truncate_two_decimal_places(single_data['rating'])), (0, 0, 0), font)

    # if 'isAllJustice' in single_data:
    #     font = ImageFont.truetype('fonts/FOT-RodinNTLGPro-DB.ttf', 35)
    #     if single_data['isAllJustice'] == 'true' or single_data['isAllJustice'] is True:
    #         draw.text((530, 105), "AJ", '#000000', font)
    #     elif single_data['isFullCombo'] == 'true' or single_data['isFullCombo'] is True:
    #         draw.text((530, 105), "FC", '#000000', font)
    # pic = pic.resize((280, 105))
    return base