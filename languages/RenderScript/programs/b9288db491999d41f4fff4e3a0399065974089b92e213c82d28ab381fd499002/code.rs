#pragma version(1)
#pragma rs java_package_name(com.example.renderscript)

uchar4 RS_KERNEL grayscale(uchar4 in) {
    uchar gray = (uchar)((in.r * 0.299f) + (in.g * 0.587f) + (in.b * 0.114f));
    uchar4 out = in;
    out.r = gray;
    out.g = gray;
    out.b = gray;
    return out;
}
