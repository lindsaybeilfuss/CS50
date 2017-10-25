#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change; //declare variable as float
    do
    {
        printf("enter the amount of change required:\n");
        change = get_float (); //assign value to float
    }
    while (change < 0);

    int totalcoins = 0; //declare totalcoins as integer and assign value
    int cents = round(change * 100); //declare cents as integer and assign value

    //printf("%i\n", cents);

    totalcoins += cents/25; //increment variable on left by the value on the right
    cents %= 25;

    totalcoins += cents/10;
    cents %= 10;

    totalcoins += cents/5;
    cents %= 5;

    totalcoins += cents/1;
    cents %= 1;

    printf("%i\n", totalcoins);
}
