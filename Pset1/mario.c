#include <stdio.h>
#include <cs50.h>

int main(void)
{
int height; //int height must be declared outside of the do while loop
    do
    {
        printf("Enter the total number of stairs you want Mario to climb, no greater than 23\n");
        printf("Height: ");
        height = get_int();
    }
    while (height < 0 || height > 23);

//can declare variable in for loop within loop, but must redecalre if being used again
    for (int row = 0; row <height; row++) //initialize row to 0; condition to be checked; repeat until condition is false.
    {
        for (int space = 0; space < (height - row- 1); space++)
        {
            printf(" ");
        }
        for (int hash = 0; hash < (row + 1); hash++)
        {
            printf("#");
        }
        printf("  ");
        for (int hash = 0; hash < (row + 1); hash++)
        {
            printf("#");
        }
        printf("\n");
    }
}