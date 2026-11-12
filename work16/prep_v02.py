# v02 screenshots from the creator (src/v02/): personal data covered with grey "hidden" boxes (as the original deck did), cropped
# to the form card -> edit/assets/deck/v02_*.png. Coordinates below are in the CROPPED images.
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)


def hide(d, box, label=True):
    d.rectangle(box, fill=(214, 218, 225))
    if label: d.text(((box[0] + box[2]) / 2, (box[1] + box[3]) / 2), "hidden", fill=(120, 126, 138), font=F, anchor="mm")


im = Image.open("src/v02/designation_dropdown.png").convert("RGB"); d = ImageDraw.Draw(im)
hide(d, (398, 104, 584, 129)); im.crop((270, 10, 1050, 651)).save("edit/assets/deck/v02_designation.png")
im = Image.open("src/v02/team_radio.png").convert("RGB"); im.crop((85, 20, 851, 368)).save("edit/assets/deck/v02_team.png")
im = Image.open("src/v02/sheet_tabs.png").convert("RGB"); d = ImageDraw.Draw(im)
for y0, y1 in ((180, 210), (215, 246), (251, 282), (287, 318)):
    for x0, x1 in ((203, 380), (1108, 1285), (1290, 1465)): hide(d, (x0, y0, x1, y1))
im.crop((0, 30, 1874, 711)).save("edit/assets/deck/v02_sheet.png")
print("ok")
# date field only (the old image-5-1 also shows the old 4-team list below it)
Image.open("edit/assets/deck/image-5-1.png").convert("RGB").crop((0, 0, 646, 165)).save("edit/assets/deck/v02_date.png")
# compact Sheet strip: header + 4 rows, then the tab bar (with REDQ); from the masked sheet (cropped coords = original - 30 in y)
sh = Image.open("edit/assets/deck/v02_sheet.png"); top = sh.crop((0, 70, 1874, 295)); tabs = sh.crop((0, 635, 1874, 681))
strip = Image.new("RGB", (1874, top.height + tabs.height), (255, 255, 255)); strip.paste(top, (0, 0)); strip.paste(tabs, (0, top.height)); strip.save("edit/assets/deck/v02_sheet_strip.png")
print("strip", strip.size)
Image.open("edit/assets/deck/v02_team.png").crop((0, 0, 400, 348)).save("edit/assets/deck/v02_team_list.png")
# Check-out form (scene 09): keep the deck's top part (Email, Staff ID, Shift start date) and replace the old 4-option team card
# with the creator's new one (with REDQ), scaled to the same card width.
old = Image.open("edit/assets/deck/image-8-1.png").convert("RGB")                      # 525 x 560; team card starts at y ~352
team = Image.open("src/v02/checkout_team_radio.png").convert("RGB").crop((92, 6, 870, 364))
team = team.resize((511, round(team.height * 511 / team.width)), Image.LANCZOS)
out = Image.new("RGB", (525, 352 + team.height), old.getpixel((2, 345))); out.paste(old.crop((0, 0, 525, 352)), (0, 0)); out.paste(team, (7, 352))
out.save("edit/assets/deck/v02_checkout_form.png"); print("checkout", out.size)
