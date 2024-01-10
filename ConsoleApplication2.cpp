#include <algorithm>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iostream>
#include <vector>


struct Point {
	double x, y;
	double angle;

	bool operator<(const Point& p) const {
		return x < p.x || (x == p.x && y < p.y);
	}
};

bool compareByAngle(const Point& a, const Point& b) {
	return a.angle < b.angle;
}

double cross(const Point& O, const Point& A, const Point& B) {
	return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}

void quickHull(const std::vector<Point>& points, const Point& A, const Point& B, std::vector<Point>& result) {
	if (points.empty())
		return;

	int index = 0;
	double maxDistance = 0;

	for (int i = 0; i < points.size(); ++i) {
		double currentDistance = cross(A, B, points[i]);
		if (currentDistance > maxDistance) {
			index = i;
			maxDistance = currentDistance;
		}
	}

	if (maxDistance == 0)
		return;

	Point C = points[index];
	result.emplace_back(C);

	std::vector<Point> leftSet;
	std::vector<Point> rightSet;

	for (int i = 0; i < points.size(); ++i) {
		if (cross(A, C, points[i]) > 0)
			leftSet.emplace_back(points[i]);
		else if (cross(C, B, points[i]) > 0)
			rightSet.emplace_back(points[i]);
	}

	quickHull(leftSet, A, C, result);
	quickHull(rightSet, C, B, result);
}

void convex_hull(std::vector<Point> P) {
	int n = P.size();
	if (n <= 3) {
		std::cout << "Меньше или равно 3 точек." << std::endl;
		return;
	}

	std::vector<Point> result;
	std::sort(P.begin(), P.end());

	result.emplace_back(P[0]);
	result.emplace_back(P[n - 1]);

	std::vector<Point> leftSet;
	std::vector<Point> rightSet;

	for (int i = 1; i < n - 1; ++i) {
		if (cross(P[0], P[n - 1], P[i]) > 0)
			leftSet.emplace_back(P[i]);
		else if (cross(P[0], P[n - 1], P[i]) < 0)
			rightSet.emplace_back(P[i]);
	}

	quickHull(leftSet, P[0], P[n - 1], result);
	quickHull(rightSet, P[n - 1], P[0], result);

	std::sort(result.begin(), result.end(), compareByAngle);
	std::cout << result.size() << std::endl;
	for (const auto& point : result) {
		std::cout << "(" << point.x << ", " << point.y << ") " << std::endl;
	}
	std::cout << std::endl;
}

std::vector<Point> readPointsFromFile(const std::string& filename) {
	std::vector<Point> points;
	std::ifstream file(filename);
	if (!file.is_open()) {
		std::cout << "Ошибка открытия файла." << std::endl;
		exit(1);
	}

	int n;
	if (!(file >> n)) {
		std::cout << "Ошибка чтения числа точек." << std::endl;
		exit(1);
	}

	points.reserve(n);

	for (int i = 0; i < n; i++) {
		double x, y;
		if (!(file >> x >> y)) {
			std::cout << "Ошибка чтения координат точек." << std::endl;
			exit(1);
		}
		double angle = atan2(y, x);
		points.emplace_back(Point{ x, y, angle });
	}
	file.close();

	return points;
}

void executeConvexHull(const std::vector<Point>& points) {
	auto start_time = std::chrono::high_resolution_clock::now();
	convex_hull(points);
	auto end_time = std::chrono::high_resolution_clock::now();
	auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();
	std::cout << "время выполнения: " << duration << " миллисекунд" << std::endl;
}

int main() {
	setlocale(LC_ALL, "Russian");
	std::vector<Point> points = readPointsFromFile("points.txt");
	executeConvexHull(points);

	return 0;
}

