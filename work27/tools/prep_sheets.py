"""Make 'before' bases and popup crops from the upscaled (2x, 1600x930) screenshots so typing and dropdowns can animate.
Boxes are in original 800x465 screenshot px (from pixel diffs between pairs)."""
from PIL import Image
S = 'video/assets/sheets/'; G = S + 'gen/'
def im(n): return Image.open(S + n + '.jpg').convert('RGB')
def patch(after, before, boxes, out):
    a = im(after).copy(); b = im(before)
    for x0, y0, x1, y1 in boxes:
        bx = (x0 * 2, y0 * 2, x1 * 2, y1 * 2); a.paste(b.crop(bx), bx[:2])
    a.save(G + out + '.jpg', quality=95)
def crop(n, box, out):
    x0, y0, x1, y1 = box; im(n).crop((x0 * 2, y0 * 2, x1 * 2, y1 * 2)).save(G + out + '.png')
# 02b: row 8 empty
patch('02b-belts-adding-new-belt', '02-belts', [(28, 306, 545, 336)], '02b_base')
# 04b: master list hidden (cell C4 stays selected)
patch('04b-classes-pick-master', '04-classes', [(158, 187, 292, 260)], '04b_base'); crop('04b-classes-pick-master', (158, 187, 292, 260), '04b_list')
# 05b: row 10 A-C empty and belt list hidden
patch('05b-students-new-student-pick-belt', '05-students', [(30, 259, 232, 281), (234, 280, 317, 446)], '05b_base'); crop('05b-students-new-student-pick-belt', (234, 280, 317, 446), '05b_list')
# 05c: fee + join date empty and Yes/No list hidden; second base with date but no list
patch('05c-students-active-yes', '05b-students-new-student-pick-belt', [(307, 259, 445, 281), (446, 280, 529, 353)], '05c_base')
patch('05c-students-active-yes', '05b-students-new-student-pick-belt', [(446, 280, 529, 353)], '05c_base2'); crop('05c-students-active-yes', (446, 280, 529, 353), '05c_list')
# 06b: A11 empty and suggestion hidden
patch('06b-enrolments-type-ic-to-search', '06-enrolments', [(27, 272, 126, 323)], '06b_base'); crop('06b-enrolments-type-ic-to-search', (27, 295, 126, 323), '06b_sug')
# 06c: class list hidden
patch('06c-enrolments-pick-class', '06-enrolments', [(109, 295, 200, 389)], '06c_base'); crop('06c-enrolments-pick-class', (109, 295, 200, 389), '06c_list')
# 08b: role list hidden
patch('08b-access-pick-role', '08-access', [(193, 233, 277, 347)], '08b_base'); crop('08b-access-pick-role', (193, 233, 277, 347), '08b_list')
# 08c: F7 empty (Yes appears)
patch('08c-access-parent-added', '08b-access-pick-role', [(394, 209, 476, 240)], '08c_base')
print('ok')
