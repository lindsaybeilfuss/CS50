#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change; //declare variable as float
    do
    {
        printf("enter the amount of change required:\n");
        change = get_float (); //prompt user and assign value to float
    }
    while (change < 0);

    int totalcoins = 0; //declare totalcoins as integer and assign value
    int cents = round(change * 100); //declare cents as integer and assign value

    //printf("%i\n", cents);

    totalcoins += cents/25; //increment variable on left by the value on the right, stores in totalcoins
    cents %= 25; //cents mod 25 gives remainder after dividing cents by 25, stores in cents
    totalcoins += cents/10;
    cents %= 10;
    totalcoins += cents/5;
    cents %= 5;
    totalcoins += cents/1;
    cents %= 1;

    printf("%i\n", totalcoins);
}
