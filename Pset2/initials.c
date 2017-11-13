#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)
{
    //prompt user
    printf("Enter your full name\n");
    string name = get_string();
    if (name != NULL)
    //print the first character in the string
    printf("%c", toupper(name[0]));
    {
        //initialize to 0, store length of name in variable n, iterate over i so long as less than lenght of name
        for (int i = 0, n = strlen(name); i < n; i++)

        {
            //if the i'th character in name equals white space
            if (isspace (name[i]))
            printf("%c", toupper(name[i + 1]));
        }

    }
printf("\n");
}
