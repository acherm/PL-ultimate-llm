def proc diamond x,y,size,diff
    default diff=15
    plot x,y-size
    draw -size,size
    draw size,size
    draw size,-size
    draw -size,-size
    if size >4 then
        diamond x,y+size,size-diff
        diamond x,y-size,size-diff
        diamond x-size,y,size-diff
        diamond x+size,y,size-diff
end proc
