#ifndef SEASTAR_H
#define SEASTAR_H

#ifdef _WIN32
#define DLLEXPORT extern "C" __declspec(dllexport)
#else
#define DLLEXPORT
#endif
struct OpenPt
{
    int est;
    int sofar;
    int index;
};
bool operator<(const OpenPt &lhs, const OpenPt& rhs);

int position_to_index(const int &x, const int &y);
bool check_coord(const int &x, const int &y, const int &max_x, const int &max_y);
int distance(const int &x1, const int &y1, const int &x2, const int &y2);
int indextox(const int &p);
int indextoy(const int &p);
int indexdistance(const int &p1, const int &p2);

#ifdef __cplusplus
extern "C"
{
#endif


/// Create the adjacency list.
DLLEXPORT void init_astar(const int map_width, const int map_height);
DLLEXPORT int* astar(int *startv, const int startc, int *endv, const int endc, int* obstaclev,
             const int obstaclec, const int blocking);

#ifdef __cplusplus
}
#endif

#endif
