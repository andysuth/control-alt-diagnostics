#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include "vector2d.h"
#include "ray.h"
#include "interface.h"

struct Layer {
    Vec2 incident;
    Vec2 normal;
    double n_1,n_2;
};

std::vector<Vec2> traceRay(const Vec2& start, Vec2 dir, const std::vector<Layer>& interfaces) {
    std::vector<Vec2> rayPath = { start };

    for (const auto& iface : interfaces) {
        // Compute refracted direction using Snell's law
        auto maybeRefracted = refract(dir, iface.normal, iface.n_1, iface.n_2);
        if (!maybeRefracted) {
            std::cerr << "Total internal reflection occurred\n";
            break;
        }

        Vec2 refracted = *maybeRefracted;

        // Travel the correct vertical distance to the next interface
        double travel = (iface.incident.y - rayPath.back().y) / dir.y;

        // Advance to the point of intersection on the interface
        Vec2 nextPos = rayPath.back() + dir * travel;
        rayPath.push_back(nextPos);

        // Update direction for next segment
        dir = refracted;
    }

    return rayPath;
}

int main() {

    double beamWidth = 6.0;
    double focalY = -5.0;
    int numRays = 10;


    std::vector<Layer> interfaces = {
        { Vec2(0.0, 0.0), Vec2(0.0, 1.0), 1.0, 1.5}, 
        { Vec2(0.0, -2.0), Vec2(0.0, 1.0), 1.5, 1.0 },
        { Vec2(0.0, -6.0), Vec2(0.0, 1.0), 1.0, 1.0}
    };
    
    

    std::ofstream fout("ray_bundle.txt");
    Vec2 start(0.0, 1.0);

    for (int i = 0; i < numRays; ++i) {
        // Spread rays evenly across the beam width
        double x0 = -beamWidth / 2.0 + i * (beamWidth / (numRays - 1));
        Vec2 start(x0, 1.0);  // All rays start at y = 1.0

        // Aim the ray at the fixed focal point
        Vec2 target(0.0, focalY);
        Vec2 dir = (target - start).normalize();

        auto path = traceRay(start, dir, interfaces);

        for (const auto& pt : path) {
            fout << i << " " << pt.x << " " << pt.y << "\n";  // Use ray index instead of angle
        }
        fout << "\n";  // Separate each ray in the file
    }

    fout.close();
}