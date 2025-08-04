#ifndef INTERFACE_H
#define INTERFACE_H

#include "vector2d.h"
#include <iostream>
#include <optional>

//Computes the refracted direction using Snell's law
//Returns std::nullopt if total internal refelction occurs

std::optional<Vec2> refract(
    const Vec2& incident,           // Incoming ray direction
    const Vec2& normal,             // Normal vector at the interaface, points out of the glass
    double n1,                      // Refractive index of medium 1
    double n2                       // Refraction index of medium 2
) {
    double cosTheta1 = -incident.dot(normal); //Cosine of angle between ray and normal
    // std::cout << "cosTheta1: " << cosTheta1 << std::endl;
    double eta=n1/n2;
    // std::cout << "eta: " << eta << std::endl;
    double sin2Theta2 = eta * eta * (1.0 - (cosTheta1 * cosTheta1));
    // std::cout << "sinT2: " << sin2Theta2 << std::endl;

    // Check for TIR
    if (sin2Theta2 > 1.0) {
        return std::nullopt;
    }



    // Compute refracted direction using vector Snell
    double cosTheta2 = std::sqrt(1 - ((eta * eta) * (1 - (cosTheta1 * cosTheta1))));
    std::cout << "cosTheta2: " << cosTheta2 << std::endl;
    Vec2 term1 = incident * eta;
    std::cout << "term1: " << term1.x << ", " << term1.y << std::endl;
    Vec2 term2 = normal * ((eta * cosTheta1) - cosTheta2);
    std::cout << "term2: " << term2.x << ", " << term2.y << std::endl;
    Vec2 refracted = term1 + term2;
    std::cout << "Unnormalized refracted: " << refracted.x << ", " << refracted.y << std::endl;
    Vec2 refractedNorm = refracted.normalize();
    std::cout << "normalized refracted: " << refractedNorm.x << ", " << refractedNorm.y << std::endl;
    return refractedNorm;
}

#endif