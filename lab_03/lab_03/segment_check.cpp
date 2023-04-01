#include "segment_check.h"

ret_code_t check_segment(const Point &a, const Point &b)
{
    if (a.x == b.x && a.y == b.y)
        return ERR_INCORRECT_DATA;
    return EXIT_OK;
}
