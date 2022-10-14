#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
    // seed the rng
    srand(time(0));

    for (int i = 0; i < 10; i++)
    {
        // rand() % range + start_num
        int x = rand() % 6 + 1;

        printf("%i ", x);
    }
    printf("\n");
}