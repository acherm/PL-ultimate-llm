#include "generics.h"

defclass Point {
    int x;
    int y;
};

imeth int getX()
{
    return x;
}

imeth int getY()
{
    return y;
}

imeth void setX(int val)
{
    x = val;
}

imeth void setY(int val)
{
    y = val;
}