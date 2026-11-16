"""Statue cut-out from the hero frame: colour seeds + manual seeds (sword, base board) refined with OpenCV GrabCut."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage
img = cv2.imread('analysis/frames/a_005.png')               # 2160x3840 BGR
sc = 0.5; small = cv2.resize(img, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
col = cv2.imread('analysis/mask_colour.png', 0) > 0
col_s = cv2.resize(col.astype(np.uint8), (small.shape[1], small.shape[0]), interpolation=cv2.INTER_NEAREST) > 0
M = np.full(small.shape[:2], cv2.GC_BGD, np.uint8)
def S(p): return (np.array(p) * sc).astype(np.int32)
roi = S([[150, 1100], [1950, 1100], [1950, 3650], [150, 3650]])
cv2.fillPoly(M, [roi], cv2.GC_PR_BGD)
M[ndimage.binary_dilation(col_s, iterations=6) & (M == cv2.GC_PR_BGD)] = cv2.GC_PR_FGD
M[ndimage.binary_erosion(col_s, iterations=5)] = cv2.GC_FGD
board = S([[237, 3300], [1800, 3237], [1875, 3437], [325, 3575]])
cv2.fillPoly(M, [board], cv2.GC_PR_FGD)
cv2.fillPoly(M, [S([[280, 3360], [1700, 3300], [1740, 3400], [360, 3480]])], cv2.GC_FGD)
blade = S([[372, 1165], [402, 1160], [452, 1870], [420, 1875]])
cv2.fillPoly(M, [blade], cv2.GC_FGD)
cv2.fillPoly(M, [S([[750, 1000], [1550, 1000], [1550, 1640], [750, 1640]])], cv2.GC_BGD)   # maker's face
cv2.fillPoly(M, [S([[1650, 1700], [2160, 1700], [2160, 3150], [1650, 3150]])], cv2.GC_BGD)  # shirt right
cv2.fillPoly(M, [S([[640, 1600], [1150, 1600], [1150, 1735], [640, 1735]])], cv2.GC_BGD)                # above crown
cv2.fillPoly(M, [S([[565, 1760], [690, 1760], [690, 2040], [565, 2040]])], cv2.GC_BGD)                    # maker's fingers
cv2.fillPoly(M, [S([[715, 1790], [770, 1765], [900, 1760], [930, 1745], [955, 1760], [1000, 1800], [1040, 1840], [1040, 1950], [715, 1950]])], cv2.GC_FGD)  # crown
cv2.fillPoly(M, [S([[960, 2000], [1060, 2000], [1060, 2090], [960, 2090]])], cv2.GC_FGD)                  # moustache tip
cv2.fillPoly(M, [S([[150, 1830], [368, 1830], [368, 1985], [150, 1985]])], cv2.GC_BGD)                    # wall socket
cv2.fillPoly(M, [S([[150, 1985], [258, 1985], [258, 2125], [150, 2125]])], cv2.GC_BGD)
cv2.fillPoly(M, [S([[1145, 2550], [1225, 2525], [1262, 2675], [1300, 2800], [1200, 2850], [1150, 2775]])], cv2.GC_BGD)  # shirt print
bg = np.zeros((1, 65), np.float64); fg = np.zeros((1, 65), np.float64)
cv2.grabCut(small, M, None, bg, fg, 6, cv2.GC_INIT_WITH_MASK)
m = np.where((M == cv2.GC_FGD) | (M == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
lab, n = ndimage.label(m > 0); sizes = ndimage.sum(m > 0, lab, range(1, n + 1))
m = (np.isin(lab, np.argsort(sizes)[::-1][:1] + 1) * 255).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
mb = m > 0; holes = ndimage.binary_fill_holes(mb) & ~mb
hl, hn = ndimage.label(holes); hs = ndimage.sum(holes, hl, range(1, hn + 1))
mb |= np.isin(hl, [i + 1 for i, z in enumerate(hs) if z < 1500])   # fill specks only, keep real gaps (under the arm)
m = mb.astype(np.float32)
full = cv2.resize(m, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_LINEAR)
full = cv2.GaussianBlur(full, (0, 0), 2.2); full = np.clip((full - 0.5) * 2.2 + 0.5, 0, 1)
cv2.imwrite('analysis/statue_alpha.png', (full * 255).astype(np.uint8))
print('alpha bbox', np.argwhere(full > 0.5).min(0), np.argwhere(full > 0.5).max(0))
