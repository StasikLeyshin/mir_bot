
from PIL import ImageDraw, ImageFont, Image
import textwrap
import os
import ujson
import json

class generating:

    def __init__(self, file, create_mongo):
        self.file = file
        self.create_mongo = create_mongo

    async def sp_vopr(self):
        f2 = open(f"{self.file}.txt", "r+", encoding="cp1251")
        s = f2.readlines()
        f2.seek(0)
        f2.close()
        vopr = {"nom": {}, "vopr": {}, "spis_vop": {}, "att": " "}
        vopr_new = []
        for i in s:
            pas = i[i.find(":") + 1:]
            logi = i[:i.find(":")]
            nom = pas[pas.find(":") + 1:].replace("\\v", "\n")
            vopr["nom"][logi] = nom
            vopr["vopr"][pas[:pas.find(":")]] = pas[pas.find(":") + 1:].replace("\\v", "\n")
            vopr["spis_vop"][logi] = pas[:pas.find(":")]
            vopr_new.append({"nom": logi, "vopr": pas[:pas.find(":")], "otvet": nom})
        MAX_W, MAX_H = 1080, 1920
        file_name = "generating_questions/img/1.jpg"
        im1 = Image.open(file_name)
        draw1 = ImageDraw.Draw(im1)
        im2 = Image.open(file_name)
        draw2 = ImageDraw.Draw(im2)
        im3 = Image.open(file_name)
        draw3 = ImageDraw.Draw(im3)
        im4 = Image.open(file_name)
        draw4 = ImageDraw.Draw(im3)
        if len(vopr["spis_vop"]) > 63:
            im4 = Image.open(file_name)
            draw4 = ImageDraw.Draw(im4)
        # font = ImageFont.truetype( "mira.ttf", 45)
        font = ImageFont.truetype("generating_questions/fonts/PFSquareSansPro-Medium.ttf", 45)
        font1 = ImageFont.truetype("generating_questions/fonts/PFSquareSansPro-Regular.ttf", 45)
        current_h, pad = 50, 10
        # para = astr.split(" ")
        margin = offset = 90
        nom2 = 0
        nom3 = 0
        nom4 = 0
        for i in vopr["spis_vop"].keys():
            if int(i) < 17:
                draw = draw1
            elif int(i) > 17 and nom2 == 0:
                draw = draw2
                margin = offset = 90
                nom2 = 1
            elif int(i) > 42 and nom3 == 0:
                draw = draw3
                margin = offset = 90
                nom3 = 1
            elif int(i) > 63 and nom4 == 0:
                draw = draw4
                margin = offset = 90
                nom4 = 1
            text = vopr["spis_vop"][i]
            no = str(i) + ". "
            if len(no) == 4:
                dob = 75
                margin = 77
            else:
                dob = 49
                margin = 100
            if len(text) >= 40 and len(text) < 60:
                peren = 28
            elif len(text) < 40:
                peren = 39
            elif len(text) >= 60:
                peren = 40
            f = 0
            for line in textwrap.wrap(text, width=peren):
                # print(line)
                if f == 0:
                    draw.text((margin, offset), no, font=font)
                    draw.text((margin + dob, offset), line, font=font1)
                    offset += font.getsize(line)[1] + 10
                    f = 1
                else:
                    # margin += dob
                    draw.text((margin + dob, offset), line, font=font1)
                    offset += font.getsize(line)[1] + 10
        im1.save('generating_questions/img/test1.png')
        im2.save('generating_questions/img/test2.png')
        if nom3:
            im3.save('generating_questions/img/test3.png')
        if nom4 == 1:
            im4.save('generating_questions/img/test4.png')
        #print(vopr)
        #json.dump(vopr, open("vopr.txt", "w", encoding="utf-8"))
        self.create_mongo.questions_update("bots", "questions", vopr_new)
        """att = str(await photo_uploader.upload_message_photo("test1.png")) + "," + str(
            await photo_uploader.upload_message_photo("test2.png")) + "," + str(
            await photo_uploader.upload_message_photo("test3.png"))
        os.remove("test1.png")
        os.remove("test2.png")
        os.remove("test3.png")
        if nom4 == 1:
            im4.save('test4.png')
            att = str(att) + "," + str(await photo_uploader.upload_message_photo("test4.png"))
            os.remove("test4.png")
        vopr["att"] = str(att)
        json.dump(vopr, open("vopr.txt", "w", encoding="utf-8"))"""
        return