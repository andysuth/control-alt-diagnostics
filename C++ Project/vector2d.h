#ifndef VECTOR2D_H
#define VECTOR2D_H
#define M_PI 3.14159265358979323846

#include <cmath>

struct Vec2 {
    double x,y;

    // Constructor 
    Vec2(double x_=0.0, double y_=0.0) : x(x_), y(y_) {}

    // Addition
    Vec2 operator+(const Vec2& other) const {
        return Vec2(x + other.x,y + other.y);
    }

    // Subtraction
    Vec2 operator-(const Vec2& other) const {
        return Vec2(x - other.x,y - other.y);
    }

    //Multiply
    // Vec2 * scalar
    Vec2 operator*(double scalar) const {
    return Vec2(x * scalar, y * scalar);
    }

    // scalar * Vec2
    friend Vec2 operator*(double scalar, const Vec2& vec) {
        return Vec2(vec.x * scalar, vec.y * scalar);
    }
    

    // Dot product
    double dot(const Vec2& other) const{
        return x * other.x + y * other.y;
    }

    // Magnitude
    double norm() const{
        return std::sqrt(x*x + y*y);
    }

    //Return unit vector
    Vec2 normalize() const{
        double n = norm();
        return Vec2(x/n, y/n);
    }

};

inline Vec2 angleToVec2(double degrees) {
    double radians = degrees * M_PI/180;
    return Vec2(std::cos(radians), std::sin(radians)).normalize();
}

#endif