#include <cstdio>
#include <deque>
#include <cstdlib>
#include <ctime>
#include <conio.h>
#include <windows.h>
using namespace std;

#define WIDTH 29
#define HEIGHT 23
#define DELTAX 2
#define DELTAY 1

enum { SPACE, TUNNEL, WALL, BOX, FOOD, HIFOOD, BODY, HEAD, KEY, MAGIC };

const int SpeedTable[] = { 500, 350, 270, 200, 150, 120, 100, 85, 75, 70 };

const char *LevelTable[] =
{
    "无名小蛇", "蛇男爵　", "蛇子爵　", "蛇伯爵　", "蛇侯爵　", "蛇公爵　",
    "蛇王　　", "龙形蛇　", "无名小龙", "龙男爵　", "龙子爵　", "龙伯爵　",
    "龙侯爵　", "龙公爵　", "龙王　　", "四海龙王"
};

class Point
{
public:
    int x, y;
    Point(int xx = 0, int yy = 0) { x = xx; y = yy; }
};

class SnakeGame
{
public:
    SnakeGame();
    ~SnakeGame();
    void HideCursor();
    void GotoXY(int x, int y);
    void SetSpeed();
    void GameStart();
    void SnakeMove();
    void Changedirection();
    void SetThings(int things);
    void ClearThings();
    void OpenDoor(bool in);
    void PrintGame();
    void SetStage();
    void SetStage0();
    void SetStage1();
    void SetStage2();
    void SetStage3();
    void SetStage4();
    void SetStage5();
    void SetStage6();
    void SetStage7();
    void SetStage8();
    void SetStage9();
    void Run();
    bool Trade();

protected:
    HANDLE hout;
    deque<Point> body;
    int table[HEIGHT][WIDTH];
    Point food, hifood, magic, key, box, door1, door2;
    clock_t alive;
    int direction0, direction1;
    bool hashifood, pause, death, win;
    int score, level, count, speed, life, stage;
};

SnakeGame::SnakeGame()
{
    hout = GetStdHandle(STD_OUTPUT_HANDLE);
    speed = 0;
    score = 0;
    level = 0;
    life = 3;
    stage = 0;
    HideCursor();
}

SnakeGame::~SnakeGame()
{
    CloseHandle(hout);
}

void SnakeGame::HideCursor()
{
    CONSOLE_CURSOR_INFO cursor_info = {1, 0};
    SetConsoleCursorInfo(hout, &cursor_info);
}

void SnakeGame::GotoXY(int x, int y)
{
    COORD cod;
    cod.X = x;
    cod.Y = y;
    SetConsoleCursorPosition(hout, cod);
}

void SnakeGame::SetSpeed()
{
    int flag;
    GotoXY(DELTAX, 0);
    printf("请选择速度：1~10");
    GotoXY(DELTAX, 1);
    flag = scanf("%d*c", &speed);
    while (flag != 1 || speed < 1 || speed > 10)
    {
        system("cls");
        GotoXY(DELTAX, 0);
        printf("输入有误，请选择速度：1~10");
        if (flag == 1)
        {
            GotoXY(DELTAX, 1);
            printf("%30s", "");
        }
        else
        {
            scanf("%*[^0-9]");
            GotoXY(DELTAX, 1);
            printf("%30s", "");
        }
        GotoXY(DELTAX, 1);
        flag = scanf("%d*c", &speed);
    }
    --speed;
    GotoXY(DELTAX, 0);
    printf("%30s", "");
    system("cls");
}

void SnakeGame::GameStart()
{
    int x, y;

    for (x = 0; x < WIDTH; ++x)
        table[0][x] = WALL;
    for (y = 1; y < HEIGHT - 1; ++y)
    {
        table[y][0] = WALL;
        for (x = 1; x < WIDTH - 1; ++x)
            table[y][x] = SPACE;
        table[y][WIDTH - 1] = WALL;
    }
    for (x = 0; x < WIDTH; ++x)
        table[HEIGHT - 1][x] = WALL;

    body.push_back(Point(8, 8));
    body.push_back(Point(8, 9));
    body.push_back(Point(8, 10));
    body.push_back(Point(8, 11));
    body.push_back(Point(8, 12));

    table[8][8] = BODY;
    table[8][9] = BODY;
    table[8][10] = BODY;
    table[8][11] = BODY;
    table[8][12] = HEAD;

    direction0 = 0;
    direction1 = 0;
    count = 0;
    hashifood = false;
    pause = false;
    death = false;
    win = false;
    hifood.x = 0;
    magic.x = 0;
    key.x = 0;
    SetStage();

    GotoXY(WIDTH * 2 + 6, 5);
    printf("等级：%s", LevelTable[level]);
    GotoXY(WIDTH * 2 + 6, 7);
    printf("得分：%d", score);
    GotoXY(WIDTH * 2 + 6, 9);
    printf("关卡：%d", stage + 1);
    GotoXY(WIDTH * 2 + 6, 11);
    printf("生命：%d",  life);
    GotoXY(WIDTH * 2 + 6, 13);
    printf("速度：%d", speed + 1);

    GotoXY(WIDTH * 2 + 4, 17);
    printf("按方向键控制移动");
    GotoXY(WIDTH * 2 + 4, 19);
    printf("按空格键暂停");
    GotoXY(WIDTH * 2 + 4, 21);
    printf("按任意键解除暂停");
    GotoXY(WIDTH * 2 + 4, 23);
    printf("by: wohaaitinciu");
}

void SnakeGame::SnakeMove()
{
    Point head = body.back();
    Point newhead, tail;

    if (direction1 != direction0)
        direction0 = direction1;

    switch (direction0)
    {
    case 0:
        newhead = Point(head.x, head.y + 1);
        break;
    case 1:
        newhead = Point(head.x + 1, head.y);
        break;
    case 2:
        newhead = Point(head.x, head.y - 1);
        break;
    case 3:
        newhead = Point(head.x - 1, head.y);
        break;
    default:
        return;
    }
    if (table[newhead.x][newhead.y] == WALL
        || table[newhead.x][newhead.y] == BODY)
    {
        death = true;
        return;
    }

    body.push_back(newhead);

    table[head.x][head.y] = BODY;
    GotoXY(DELTAX + 2 * head.y, DELTAY + head.x);
    printf("□");

    table[newhead.x][newhead.y] = HEAD;
    GotoXY(DELTAX + 2 * newhead.y, DELTAY + newhead.x);
    printf("■");

    if (newhead.x == food.x && newhead.y == food.y)
    {
        score += 30 + speed * 5;
        ++count;
        if (count < 20)
        {
            SetThings(FOOD);
            if (count % 5 == 0 && hifood.x == 0)
            {
                SetThings(HIFOOD);
                hashifood = true;
            }
            if (count == 12)
                OpenDoor(true);
        }
        else
        {
            if (count == 20)
                SetThings(MAGIC);
        }
        GotoXY(WIDTH * 2 + 6, 7);
        printf("得分：%d", score);
    }
    else
    {
        if (newhead.x == hifood.x && newhead.y == hifood.y)
        {
            hifood.x = 0;
            score += 100 + speed * 5;
            ClearThings();
            GotoXY(WIDTH * 2 + 6, 7);
            printf("得分：%d", score);

            hashifood = false;
        }
        else if (newhead.x == box.x && newhead.y == box.y)
        {
            box.x = 0;
            OpenDoor(false);
            SetThings(KEY);
        }
        else if (newhead.x == key.x && newhead.y == key.y)
        {
            win = true;
            score += 50;
            GotoXY(WIDTH * 2 + 6, 7);
            printf("得分：%d", score);
        }
        else if (newhead.x == magic.x && newhead.y == magic.y)
        {
            magic.x = 0;
            ClearThings();
            if (level < 15)
            {
                ++level;
                GotoXY(WIDTH * 2 + 6, 5);
                printf("等级：%s", LevelTable[level]);
            }
        }

        tail = body.front();
        body.pop_front();
        table[tail.x][tail.y] = SPACE;
        GotoXY(DELTAX + 2 * tail.y, DELTAY + tail.x);
        printf("　");
    }
}

void SnakeGame::Changedirection()
{
    int ch = getch();

    switch (ch)
    {
    case 77:
        if (direction0 != 2)
            direction1 = 0;
        break;
    case 80:
        if (direction0 != 3)
            direction1 = 1;
        break;
    case 75:
        if (direction0 != 0)
            direction1 = 2;
        break;
    case 72:
        if (direction0 != 1)
            direction1 = 3;
        break;
    case ' ':
        getch();
        pause = !pause;
        break;
    default:
        break;
    }
}

void SnakeGame::SetThings(int things)
{
    int x, y;

    srand((unsigned)time(NULL));
    do
    {
        x = rand() % HEIGHT;
        y = rand() % WIDTH;
    } while (table[x][y] != SPACE);

    switch (things)
    {
    case FOOD:
        food.x = x;
        food.y = y;
        table[x][y] = FOOD;
        GotoXY(DELTAX + 2 * y, DELTAY + x);
        printf("☆");
        return;
    case HIFOOD:
        hifood.x = x;
        hifood.y = y;
        table[x][y] = HIFOOD;
        GotoXY(DELTAX + 2 * y, DELTAY + x);
        printf("★");
        GotoXY(WIDTH * 2 + 6, 3);
        printf("高分食物");
        alive = clock();
        return;
    case MAGIC:
        magic.x = x;
        magic.y = y;
        table[x][y] = MAGIC;
        GotoXY(DELTAX + 2 * y, DELTAY + x);
        printf("¤");
        GotoXY(WIDTH * 2 + 6, 3);
        printf("升级宝石");
        return;
    case KEY:
        key.x = x;
        key.y = y;
        table[x][y] = KEY;
        GotoXY(DELTAX + 2 * y, DELTAY + x);
        printf("※");
        GotoXY(WIDTH * 2 + 6, 3);
        printf("过关钥匙");
        return;
    default:
        return;
    }
}

void SnakeGame::ClearThings()
{
    GotoXY(WIDTH * 2 + 6, 3);
    if (key.x != 0)
        printf("过关钥匙");
    else if (magic.x != 0)
        printf("升级宝石");
    else if (count >= 12 && box.x != 0)
        printf("关卡打开");
    else if (hifood.x != 0)
        printf("高分食物");
    else
        printf("%8s", "");
}

void SnakeGame::OpenDoor(bool in)
{
    int x, y;
    if (in)
    {
        for (x = 0; x < HEIGHT; ++x)
        {
            for (y = 0; y < WIDTH; ++y)
            {
                if (table[x][y] == TUNNEL)
                {
                    table[x][y] = SPACE;
                    GotoXY(DELTAX + 2 * y, DELTAY + x);
                    printf("　");
                }
            }
        }
        GotoXY(WIDTH * 2 + 6, 3);
        printf("关卡打开");
        x = door1.x;
        y = door1.y;
    }
    else
    {
        x = door2.x;
        y = door2.y;
    }
    table[x][y] = SPACE;
    GotoXY(DELTAX + 2 * y, DELTAY + x);
    printf("　");
}

void SnakeGame::PrintGame()
{
    int x, y;

    for (x = 0; x < HEIGHT; ++x)
    {
        GotoXY(DELTAX, DELTAY + x);
        for (y = 0; y < WIDTH; ++y)
        {
            switch (table[x][y])
            {
            case SPACE: printf("　"); break;
            case HEAD:
            case WALL: printf("■"); break;
            case BODY:
            case TUNNEL: printf("□"); break;
            case BOX: printf("◎"); break;
            default: break;
            }
        }
    }
}
void SnakeGame::SetStage()
{
    switch (stage % 10)
    {
    case 0: SetStage0(); return;
    case 1: SetStage1(); return;
    case 2: SetStage2(); return;
    case 3: SetStage3(); return;
    case 4: SetStage4(); return;
    case 5: SetStage5(); return;
    case 6: SetStage6(); return;
    case 7: SetStage7(); return;
    case 8: SetStage8(); return;
    case 9: SetStage9(); return;
    default: return;
    }
}

void SnakeGame::SetStage0()
{
    int x, y, mapx = 1, mapy = WIDTH - 6;
    int map[6][5] =
    {
        {2, 1, 1, 1, 3}, {2, 2, 2, 2, 1}, {0, 0, 0, 2, 1},
        {0, 0, 0, 2, 1}, {0, 0, 0, 2, 1}, {0, 0, 0, 2, 2}
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(1, WIDTH - 6);
    door2 = Point(6, WIDTH - 2);
    box = Point(1, WIDTH - 2);
}

void SnakeGame::SetStage1()
{
    int x, y, mapx = HEIGHT - 7, mapy = 1;
    int map[6][5] =
    {
        {2, 2, 0, 0, 0}, {1, 2, 2, 2, 2}, {1, 2, 1, 1, 2},
        {1, 2, 1, 2, 2}, {1, 2, 1, 2, 0}, {3, 1, 1, 2, 0}
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(HEIGHT - 5, 5);
    door2 = Point(HEIGHT - 7, 1);
    box = Point(HEIGHT - 2, 1);
}

void SnakeGame::SetStage2()
{
    int x, y, mapx = HEIGHT - 7, mapy = WIDTH - 6;
    int map[6][5] =
    {
        {2, 2, 2, 2, 2}, {2, 1, 1, 1, 1}, {2, 1, 2, 2, 2},
        {2, 1, 1, 1, 1}, {2, 2, 2, 2, 1}, {2, 1, 1, 1, 3}
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(HEIGHT - 7, WIDTH - 2);
    door2 = Point(HEIGHT - 2, WIDTH - 6);
    box = Point(HEIGHT - 2, WIDTH - 2);
}

void SnakeGame::SetStage3()
{
    int x, y, mapx = 1, mapy = 1;
    int map[6][5] =
    {
        {3, 1, 1, 2, 2}, {1, 2, 1, 1, 2}, {1, 1, 2, 2, 2},
        {2, 1, 2, 0, 0}, {2, 1, 2, 0, 0}, {2, 2, 2, 0, 0}
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(6, 2);
    door2 = Point(2, 5);
    box = Point(1, 1);
}

void SnakeGame::SetStage4()
{
    int x, y, mapx = 1, mapy = 1;
    int map[6][5] =
    {
        {3, 1, 2, 1, 2}, {1, 1, 2, 1, 2}, {1, 1, 1, 1, 2},
        {1, 2, 2, 2, 2}, {1, 2, 0, 0, 0}, {2, 2, 0, 0, 0},
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(1, 5);
    door2 = Point(6, 1);
    box = Point(1, 1);
}

void SnakeGame::SetStage5()
{
    int x, y, mapx = HEIGHT - 7, mapy = WIDTH - 6;
    int map[6][5] =
    {
        {0, 0, 2, 2, 2}, {0, 0, 2, 1, 1}, {0, 0, 2, 1, 2},
        {0, 0, 2, 1, 1}, {2, 2, 2, 2, 1}, {2, 1, 1, 1, 3}
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(HEIGHT - 7, WIDTH - 2);
    door2 = Point(HEIGHT - 2, WIDTH - 6);
    box = Point(HEIGHT - 2, WIDTH - 2);
}

void SnakeGame::SetStage6()
{
    int x, y, mapx = HEIGHT - 7, mapy = 1;
    int map[6][5] =
    {
        {2, 2, 2, 2, 2}, {2, 2, 1, 1, 2}, {2, 1, 1, 2, 2},
        {1, 1, 2, 2, 2}, {1, 2, 2, 2, 2}, {3, 1, 1, 1, 2},
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(HEIGHT - 7, 4);
    door2 = Point(HEIGHT - 2, 5);
    box = Point(HEIGHT - 2, 1);
}

void SnakeGame::SetStage7()
{
    int x, y, mapx = 1, mapy = WIDTH - 6;
    int map[6][5] =
    {
        {2, 1, 1, 1, 3}, {2, 1, 2, 2, 1}, {2, 1, 1, 1, 1},
        {2, 2, 1, 2, 2}, {0, 2, 1, 1, 1}, {0, 2, 2, 2, 2},
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(6, WIDTH - 2);
    door2 = Point(3, WIDTH - 6);
    box = Point(1, WIDTH - 2);
}

void SnakeGame::SetStage8()
{
    int x, y, mapx = 1, mapy = 1;
    int map[6][5] =
    {
        {3, 1, 1, 2, 2}, {1, 2, 1, 1, 2}, {1, 1, 2, 1, 2},
        {2, 1, 1, 2, 2}, {2, 2, 1, 1, 2}, {2, 2, 2, 2, 2},
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(6, 4);
    door2 = Point(3, 5);
    box = Point(1, 1);
}

void SnakeGame::SetStage9()
{
    int x, y, mapx = HEIGHT - 7, mapy = 1;
    int map[6][5] =
    {
        {2, 2, 2, 2, 2}, {1, 2, 2, 1, 2}, {1, 1, 1, 1, 2},
        {2, 1, 1, 2, 2}, {1, 1, 1, 2, 0}, {3, 1, 1, 2, 0},
    };
    for (x = 0; x < 6; ++x)
    {
        for (y = 0; y < 5; ++y)
            table[x + mapx][y + mapy] = map[x][y];
    }
    door1 = Point(HEIGHT - 7, 1);
    door2 = Point(HEIGHT - 7, 4);
    box = Point(HEIGHT - 2, 1);
}

bool SnakeGame::Trade()
{
    char c;
    do
    {
        GotoXY(WIDTH * 2 + 2, 0);
        printf("你是否愿意用15000分");
        GotoXY(WIDTH * 2 + 2, 1);
        printf("换一条命？Y/N");
        scanf("%c", &c);
        if (c == 'y' || c == 'Y')
            return true;
        else if (c == 'n' || c == 'N')
            return false;
    } while (1);
}

void SnakeGame::Run()
{
    while (1)
    {
        GameStart();
        PrintGame();
        SetThings(FOOD);
        GotoXY(WIDTH * 2 + 6, 3);
        printf("%8s", "");
        GotoXY(WIDTH * 2 + 4, 0);
        printf("按任意键开始游戏");
        getch();
        GotoXY(WIDTH * 2 + 4, 0);
        printf("%16s", "");

        while (!death && !win)
        {
            while (kbhit())
                Changedirection();
            SnakeMove();
            Sleep(SpeedTable[speed]);
            if (hashifood && clock() - alive >= 8000)
            {
                GotoXY(DELTAX + 2 * hifood.y, DELTAY + hifood.x);
                printf("　");
                hifood.x = 0;
                ClearThings();
                hashifood = false;
            }
        }

        if (death)
        {
            if (--life > 0)
            {
                GotoXY(WIDTH * 2 + 6, 3);
                printf("你死了！");
                GotoXY(WIDTH * 2 + 2, 0);
                system("pause");
                GotoXY(WIDTH * 2 + 2, 0);
                printf("%20s", "");
                body.clear();
            }
            else
            {
                GotoXY(WIDTH * 2 + 6, 3);
                printf("游戏结束");
                GotoXY(WIDTH * 2 + 2, 0);
                system("pause");
                if (score >= 15000 && Trade())
                {
                    GotoXY(WIDTH * 2 + 2, 0);
                    printf("%20s", "");
                    GotoXY(WIDTH * 2 + 2, 1);
                    printf("%20s", "");
                    ++life;
                    score -= 15000;
                    GotoXY(WIDTH * 2 + 6, 7);
                    printf("得分：%d%6s", score, "");
                    body.clear();
                    continue;
                }
                GotoXY(WIDTH * 2 + 2, 1);
                printf("%20s", "");
                GotoXY(WIDTH * 2 + 2, 0);
                return;
            }
        }
        else
        {
            GotoXY(WIDTH * 2 + 6, 3);
            printf("顺利过关");
            GotoXY(WIDTH * 2 + 2, 0);
            system("pause");
            GotoXY(WIDTH * 2 + 2, 0);
            printf("%20s", "");
            ++stage;
            if (stage % 10 == 0 && speed < 9)
                ++speed;
            body.clear();
        }
    }
}

int main()
{
    SnakeGame g;
    g.SetSpeed();
    g.Run();
    return 0;
}
