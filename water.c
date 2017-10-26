#include <stdio.h>
#include <cs50.h>

int main (void)
{
int minutes;
do
{
    printf("In minutes, how long do  your showers last?:\n");
    printf("Minutes: ");
    minutes = get_int();
}
while (minutes<0);
    printf("Bottles: %i\n", minutes*12);
    printf("You used this many bottles of water\n");
}

