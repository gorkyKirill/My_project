#include <iostream>
#include <fstream>
#include <vector>
#include <ctime>

using std::vector;
using std::cout;
using std::endl;
using std::ifstream;

struct Point { // представление точки с координатами 
    double x, y;
};

int orientation(Point p, Point q, Point r) {
    double val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
    if (val == 0) return 0;
    return (val > 0) ? 1 : 2;   // 0 если коллиниарны, 1 если поворот по часовой, 2 если против часовой
}

void findConvexHull(vector<Point>& points) {    // функция поиска выпуклой оболочки
    int n = points.size();  // принимает на выход массив данных точеек
    if (n < 3) return;  // если их колличество меньше 3 завершает работу

    vector<Point> hull;     // Создаем пустой множество для ответа - выпуклой оболочки hull

    double l = 0;
    for (int i = 1; i < n; i++)
        if (points[i].x < points[l].x)  // выбор самой левой точки l
            l = i;

    int p = l, q;
    do {    // поиск точек выпуклой оболочки
        hull.push_back(points[p]);
        q = (p + 1) % n;
        for (int i = 0; i < n; i++) {
            if (orientation(points[p], points[i], points[q]) == 2)
                q = i;
        }
        p = q;
    } while (p != l);

    for (Point p : hull) {
        cout << "(" << p.x << ", " << p.y << ") " << endl;;
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
    findConvexHull(points);
    double end_time = clock();
    double search_time = end_time - start_time;
    cout << search_time;
    return 0;
}
//1. Находим самую левую точку в множестве точек. Пусть эта точка называется l
//2. Создаем пустой множество для ответа - выпуклой оболочки hull
//3. Добавляем l в hull.
//4. Начиная с точки l строим выпуклую оболочку методом обхода "вправо" (по или против часовой стрелки).
// Для каждой точки p проверяем какие из остальных точек q расположены справа от вектора lp.
// Добавляем точку справа наиболее удаленную от прямой lp в hull
//5. Переходим к точке из предыдущего шага и повторяем шаг 4, пока не вернемся к начальной точке l