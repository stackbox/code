#include <iostream>
#include <cmath>
#include <cstdio>
using namespace std;

double getVal(double x1,double y1,double x2,double y2,double x3,double y3,double x) {
    double v1 = (y2 - y1)*(x-x1)*(x-x1)*(x-x1)/((x2-x1)*(x2-x1)*3);
    double v2 = (y1-y2)*x;
    double v3 = 0.5*(y3-y2)*(x-x2)*(x-x2)/(x3-x2);
    return v1 + v2 - v3;
    
}

int main() {
    int T;
    double x1,y1,x2,y2,x3,y3;
    cin >> T;
    while(T--) {
	cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3;
	double val = fabs(getVal(x1,y1,x2,y2,x3,y3,x3) - getVal(x1,y1,x2,y2,x3,y3,x2));
	printf("%.2lf\n",val);
    }
    return 0;
}

