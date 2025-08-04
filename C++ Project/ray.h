#ifndef RAY_H
#define RAY_H

#include "vector2d.h"

//Define Rays
struct Ray {
    Vec2 origin;        //Starting point vector
    Vec2 direction;     //Normalised direction vector

    //Constructor
    Ray(const Vec2& origin_, const Vec2& direction_)
        : origin(origin_), direction(direction_.normalize()) {}

    //Compute the point at distance t along the way
    Vec2 pointAt(double t) const {
        return origin + direction * t;
    }
};

#endif
