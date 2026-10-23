import cv2
_sr=None
def upscale(f,w,h,sharp=0.6):
    """FSRCNN x2 super-resolution, area-downsample to (w,h), light unsharp mask."""
    global _sr
    if _sr is None:
        _sr=cv2.dnn_superres.DnnSuperResImpl_create();_sr.readModel("FSRCNN_x2.pb");_sr.setModel("fsrcnn",2)
    up=_sr.upsample(f)
    if (w,h)!=(up.shape[1],up.shape[0]): up=cv2.resize(up,(w,h),interpolation=cv2.INTER_AREA)
    return cv2.addWeighted(up,1+sharp,cv2.GaussianBlur(up,(0,0),1.2),-sharp,0) if sharp else up
