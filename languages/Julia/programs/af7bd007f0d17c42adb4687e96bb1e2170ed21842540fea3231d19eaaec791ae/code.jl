function mandelbrot(c, max_iter)
    z = c
    for n = 1:max_iter
        if abs(z) > 2
            return n
        end
        z = z*z + c
    end
    return max_iter
end

function draw_mandelbrot(xmin,xmax,ymin,ymax,width,height,max_iter)
    r1 = range(xmin, stop=xmax, length=width)
    r2 = range(ymin, stop=ymax, length=height)
    return [mandelbrot(complex(r, i),max_iter) for r in r1, i in r2]
end

draw_mandelbrot(-2.0,1.0,-1.5,1.5,1000,1000,256)