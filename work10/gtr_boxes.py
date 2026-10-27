# Where GTR branding sits in each photo (fractions of width/height, generous margins; read off gridded contact sheets).
# Every photo window, booth card and finale tile in v03 is checked against these before it is used.
GTR = {
    "2ee1beb9": [(0.70, 0.30, 0.84, 0.80)],                              # "DON'T LET CYBERCRIMINALS TAKE OFF" banner
    "38af901c": [(0.61, 0.25, 0.72, 0.60)],                              # same banner, background
    "912ed0e8": [(0.44, 0.25, 0.61, 0.52)],                              # same banner, middle of the portrait shot
    "ACAE9274": [(0.73, 0.00, 0.84, 0.80)],                              # STOP. THINK. VERIFY. banner
    "IMG_6433": [(0.83, 0.00, 1.00, 1.00)],
    "IMG_6423": [(0.82, 0.00, 1.00, 1.00)],
    "IMG_6437": [(0.85, 0.00, 1.00, 1.00)],
    "IMG_6438": [(0.88, 0.00, 1.00, 1.00)],
    "IMG_6439": [(0.88, 0.00, 1.00, 1.00)],
    "IMG_6440": [(0.89, 0.00, 1.00, 1.00)],
    "IMG_6435": [(0.68, 0.00, 0.79, 0.17), (0.84, 0.36, 0.99, 0.62)],    # GTR logo atop a plain banner; red GTR monitor
    # v04 added photos (booth_handover's logo + letter fragments behind the man are retouched out: retouch_added.py)
    "booth_visitors": [(0.655, 0.00, 0.71, 0.05), (0.77, 0.33, 0.94, 0.57), (0.91, 0.00, 1.00, 0.62)],  # logo, GTR monitor, banner
    "booth_handover": [(0.80, 0.60, 0.88, 0.70), (0.855, 0.15, 1.00, 0.78)],                            # GTR table card, banner
}
def hits(k, box):
    x0, y0, x1, y1 = box
    return [g for g in GTR.get(k, []) if x0 < g[2] and g[0] < x1 and y0 < g[3] and g[1] < y1]
