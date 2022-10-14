#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <time.h>
void shuffle();

int numbers[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
int n = 10;

int main(int argc, string argv[])
{
    srand(time(0));

    shuffle();

    for (int i = 0;  i < n; i++)
    {
        printf("%i ", numbers[i]);
    }
    printf("\n");
}

void shuffle()
{
    int tmp, j;
    for (int i = n - 1; i > 0; i--)
    {
        j = rand() % i;
        tmp = numbers[j];
        numbers[j] = numbers[i];
        numbers[i] = tmp;
    }
}