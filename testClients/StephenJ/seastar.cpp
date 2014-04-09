//This file is for any functions you want to write that aren't directly part of your AI
//This file is shared, meaning the Java and Python clients can access it too if you want C++ code for whatever reason
#include "seastar.h"

#include <vector>
#include <queue>
#include <set>
#include <map>
#include <stdlib.h> 
#include <iostream>

using namespace std;

/// This stores which cells are adjacent.
vector< vector< int > > ADJACENCY_LIST;

int MAP_HEIGHT;
int MAP_WIDTH;

int position_to_index(const int &x, const int &y)
{
    return x+y*MAP_WIDTH;
}

/// Check to see if a coordinate is valid.
bool check_coord(const int &x, const int &y, const int &max_x, const int &max_y)
{
    // We use pass by reference so we don't have to make copies.
    // The inline keyword hints to the compiler that this function is tiny and
    // it should try to insert it as though it isn't a function call,
    // but rather as a stream of code.
    if(x < 0) return false;
    if(x >= max_x) return false;
    if(y < 0) return false;
    if(y >= max_y) return false;
    return true;
}

int distance(const int &x1, const int &y1, const int &x2, const int &y2)
{
   return abs(x1-x2)+abs(y1-y2); 
}

int xoptimize(const int &x1, const int &y1, const int &x2, const int &y2)
{
   return abs(x1-x2); 
}
int indextox(const int &p)
{
    return p % MAP_WIDTH;
}

int indextoy(const int &p)
{
    return p / MAP_WIDTH;
}

int indexdistance(const int &p1, const int &p2)
{
    return distance( indextox(p1), indextoy(p1), indextox(p2), indextoy(p2) );
}

/// Create the adjacency list.
DLLEXPORT void init_astar(const int map_width, const int map_height)
{
    // We do this because generating the adjacencies can be expensive, and they
    // don't change. So instead of computing them every time we consider
    // something we'll just do it ahead of time and filter out obstacles.
    ADJACENCY_LIST.resize(map_height*map_width);
    MAP_WIDTH = map_width;
    MAP_HEIGHT = map_height;
    for(int x = 0; x < map_width; x++)
    {
        for(int y = 0; y < map_height; y++)
        {
            int pos = x + y*map_width;
            int tmpx, tmpy, tmp;
            // Initialize the sub list.
            ADJACENCY_LIST[pos] = vector<int>();
            // Generate the adjacent cells;
            // Right
            tmpx = x + 1; tmpy = y;
            tmp = position_to_index(tmpx,tmpy);
            if(check_coord(tmpx,tmpy,map_width,map_height))
                ADJACENCY_LIST[pos].push_back(tmp); 
            // Left
            tmpx = x - 1; tmpy = y;
            tmp = position_to_index(tmpx,tmpy);
            if(check_coord(tmpx,tmpy,map_width,map_height))
                ADJACENCY_LIST[pos].push_back(tmp); 
            // Up
            tmpx = x; tmpy = y + 1;
            tmp = position_to_index(tmpx,tmpy);
            if(check_coord(tmpx,tmpy,map_width,map_height))
                ADJACENCY_LIST[pos].push_back(tmp);
            // Down
            tmpx = x; tmpy = y - 1;
            tmp = position_to_index(tmpx,tmpy);
            if(check_coord(tmpx,tmpy,map_width,map_height))
                ADJACENCY_LIST[pos].push_back(tmp); 
            //End Adj Gen
        }
    }
}

bool operator<(const OpenPt &lhs, const OpenPt& rhs)
{
    if(lhs.est+lhs.sofar >= rhs.est+rhs.sofar)
        return true;
    return false;
}

///////////////////////////////////////////////////////////////////////////////
/// Given start points, endpoints, and obstacles between, finds the shortest
/// path between any of the provided start and endpoints.
///
/// @pre: call init_astar to setup the adjacency table which helps saves on
///     some valuable maths.
/// @post: returns the found path.
///
/// @param startv: Array of start points. Length should be even: even indexes
///     (0,2,...) contain the x coordinate of a start point; odd indexes
///     (0,1,...) contain the y coordinate of a start point.
/// @param startc: The length of the array (twice the length of the number of
///     points
/// @param: endv: Array of end points (see startv for packing info)
/// @param endc: length of the endpoints array (see startc)
/// @param obstaclev: An array, which is the size of the map, which contains
///     the obstacles as a bit field. For example, in your code, set cells
///     which contain a wall to have the 1's bit set to true for example.
/// @param obstaclec: The length of the obstaclev array. (Once again, should
///     be the same size as the map)
/// @param blocking: The mask that the obstacles will be compared to. You can
///     turn obstacles off for certain units for example without recomputing
///     the whole obstacle list.
/// @returns: A list of the path. Packed the same as starts and ends, but the
///     final entry in the list will be -1 to indicate the end has been
///     reached. Returns NULL if no path can be found.
///////////////////////////////////////////////////////////////////////////////
DLLEXPORT int* astar(int *startv, const int startc, int *endv, const int endc, int* obstaclev,
             const int obstaclec, const int blocking)
{
    priority_queue< OpenPt > openset; // Points you will investigate for your path.
    vector< bool > closedset; // Points you've already checked
    map< int, int> follow; // How you got to each point
    set< int > starts; // The places you want to start from
    set< int > ends; // The places you want to end from
    vector< int > path; // The resulting path
    vector< int > best_est; // The best score from this square so far (F score)
    vector<int>::iterator it; // General purpose iterator
    vector<int>::reverse_iterator rit; // GP reverse iterator
    bool endpoint = false; // If we've struck an endpoint
    int selectedend = -1; // The endpoint that was selected.
    int current;
    int traveled;
    int min;
    int tmp;

    // Start by making the best estimate the size of the map
    best_est.resize(obstaclec);
    closedset.resize(obstaclec);
    for(int i=0; i < obstaclec; i++)
    {
        best_est[i] = obstaclec; // The worst path must be < this
        closedset[i] = false;
    }
    // Convert the input arrays to index sets.
    for(int i=0; i < startc; i+=2)
    {   
        starts.insert( position_to_index(startv[i],startv[i+1]) );
    }
    for(int i=0; i < endc; i+=2)
    {
        ends.insert( position_to_index(endv[i],endv[i+1]) );
    }
    // For each starting point, estimate the best end point and seed the open
    // set with it.
    for(int i=0; i < startc; i+=2)
    {
        int min = obstaclec;
        for(int j=0; j < endc; j+=2)
        {
            if(startv[i] == endv[j] && startv[i+1] == endv[j+1])
            {
                cerr<<"Start point is in ends set"<<endl; 
                return NULL;
            }
            tmp = distance(startv[i],startv[i+1],endv[j],endv[j+1]);
            if(tmp < min) min = tmp;
        }
        // Make an open set entry for that estimate.
        OpenPt first;
        first.est = min;
        first.sofar = 0;
        first.index = position_to_index(startv[i],startv[i+1]);
        best_est[first.index] = min;
        openset.push( first );
    }

    while( openset.size() > 0 && endpoint == false )
    {
        //While there's still entries in the openset and we've not found
        //an endpoint.
        OpenPt consider = openset.top();
        current = consider.index; // The current position
        traveled = consider.sofar+1; //G score for all neighbors
        
        openset.pop();
        
        //If we've already considered this cell.
        //This check doesn't appear in wikipedia's psuedocode. I've added it because
        //we're using a priority queue for the openset: you cannot remove an item
        //from the queue unless it is at the top. Therefore, a position may be in
        //the openset twice if the oldest discovered path there is worse than a
        //newer one. If the algorithm lasts long enough for the old path to be
        //checked again, it will simply be discarded.
        if(closedset[current])
            continue;

        closedset[current] = true;
    
        for(it = ADJACENCY_LIST[current].begin(); it != ADJACENCY_LIST[current].end(); it++)
        {
            // For each adjacent position.
            endpoint = ends.count(*it);
            if(endpoint == true && selectedend == -1)
            {
                //If we've considered an endpoint, hurray! we're done. We can
                //do a little housekeeping and escape
                selectedend = *it;
                follow[*it] = current;
                break;
            }
            if( (obstaclev[*it] & blocking) == 0)
            {
                //Check to see if the cell is blocked by our mask
                min = obstaclec; // The estimated distance to the best goal.
                for(int j=0; j < endc; j+=2)
                {
                    tmp = distance(indextox(*it), indextoy(*it), endv[j], endv[j+1]);
                    if(tmp < min) min = tmp;
                }
                OpenPt next;
                next.est = min;
                next.sofar = traveled;
                next.index = *it;
                tmp = next.est+next.sofar; //Tenative f score
                if(closedset[*it] && tmp >= best_est[*it])
                {
                    // We've already found a better way here.
                    continue;
                }
                if(tmp < best_est[*it])
                {
                    // This is a pretty good looking path, put it in the queue
                    follow[*it] = current;
                    best_est[*it] = next.est+next.sofar;
                    openset.push( next );
                }
            } 
        }
    }

    if(endpoint == false)
    {
        // There wasn't a path to any endpoints. 
        return NULL;
    }

    int fp = selectedend;
    path.push_back(fp);
    while(starts.count(fp) == 0 && follow.count(fp) > 0)
    {
        //Trace a path back to a start
        fp = follow[fp];
        path.push_back(fp);
    }
    
    if(starts.count(fp) == 0)
    {
        //This detects a bug. If you get there the follow path is messed up.
        cerr<<"PATHING BUG: Could not trace follow path to start"<<endl;
        return NULL;
    }
    
    int length = path.size()*2+1;
    int *result = new int[length];
    int c = 0;
    for(rit = path.rbegin(); rit != path.rend(); rit++)
    {
        //Reverse the path and put it to the output array.
        result[c] = indextox(*rit);
        result[c+1] = indextoy(*rit);
        c += 2;
    }
    // Indicate the end of the result.
    result[length-1] = -1;
    return result;
}

