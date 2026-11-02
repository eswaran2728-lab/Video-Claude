# Shared cut-out helper: BiRefNet mask (masks/NNNNN.png) cleaned for this statue. The PETG print is black + silver (almost no
# colour), so skin-coloured pixels (the holding hand/thumb) are removed from the mask; then the largest connected blob is kept
# (drops stray cable bits), edges eroded 1 px and feathered.
import cv2, numpy as np
def clean_mask(frame, m):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1].astype(int), hsv[..., 2].astype(int)
    skin = (((h <= 25) | (h >= 165)) & (s > 70) & (v > 45)).astype(np.uint8)
    skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(skin); H, W = skin.shape; hand = np.zeros_like(skin)
    for i in range(1, n):                                   # only big skin regions entering from the frame edge = the hand
        x, y, w, hh, a = st[i]
        if a > 1500 and (x <= 2 or y <= 2 or x + w >= W - 2 or y + hh >= H - 2): hand[lab == i] = 1
    skin = cv2.dilate(hand, np.ones((7, 7), np.uint8)).astype(bool)
    m = m.copy(); m[skin] = 0
    b = (m > 110).astype(np.uint8); n, lab, st, _ = cv2.connectedComponentsWithStats(b)
    if n > 1:
        keep = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        big = (lab == keep).astype(np.uint8); big = cv2.dilate(big, np.ones((9, 9), np.uint8))
        m = (m.astype(np.float32) * big).astype(np.uint8)
    m = cv2.erode(m, np.ones((3, 3), np.uint8)); return cv2.GaussianBlur(m, (0, 0), 1.0)
