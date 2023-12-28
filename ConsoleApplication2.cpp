#include <algorithm>
#include <fstream>
#include <iostream>
#include <vector>

using std::vector;
using std::cout;
using std::endl;
using std::ifstream;


typedef double coord_t;
typedef double coord2_t;

struct Point {
	coord_t x, y;

	bool operator <(const Point& p) const {
		return x < p.x || (x == p.x && y < p.y);
	}
};


coord2_t cross(const Point& O, const Point& A, const Point& B)
{
	return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
}


void convex_hull(vector<Point> P)
{
	size_t n = P.size(), k = 0;
	if (n <= 3) cout << "3 или мееньше точек";
	vector<Point> H(2 * n);


	sort(P.begin(), P.end());


	for (size_t i = 0; i < n; ++i) {
		while (k >= 2 && cross(H[k - 2], H[k - 1], P[i]) <= 0) k--;
		H[k++] = P[i];
	}


	for (size_t i = n - 1, t = k + 1; i > 0; --i) {
		while (k >= t && cross(H[k - 2], H[k - 1], P[i - 1]) <= 0) k--;
		H[k++] = P[i - 1];
	}

	H.resize(k - 1);
	std::cout << H.size() << endl;
	for (size_t i = 0; i < H.size(); ++i) {
		cout << "(" << H[i].x << ", " << H[i].y << ") " << endl;
	}
	cout << endl;
}

int main() {
	vector<Point> points;
	ifstream file("points.txt");
	double n;
	file >> n;
	for (int i = 0; i < n; i++) {
		double x, y;
		file >> x >> y;
		points.push_back({ x, y });
	}
	file.close();
	double start_time = clock();
	convex_hull(points);
	double end_time = clock();
	double search_time = (end_time - start_time);
	cout << "время выполнения" << search_time;
	return 0;
}
