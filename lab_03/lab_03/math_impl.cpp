#include "math_impl.h"

#define DEG_TO_RAD(x) M_PI*x/180

double get_sin(double angle_degrees)
{
    return sin(DEG_TO_RAD(angle_degrees));
}

double get_cos(double angle_degrees)
{
    return cos(DEG_TO_RAD(angle_degrees));
}

int get_abs(int value)
{
    return abs(value);
}

short get_sign(int value)
{
    if (value < 0)
        return -1;
    return value > 0;
}

int get_integer_part(double value)
{
    return floor(value);
}

double get_fract_part(double value)
{
    return value - floor(value);
}

double get_right_fract_part(double value)
{
    return 1 - get_fract_part(value);
}
