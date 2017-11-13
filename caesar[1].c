#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("missing command-line argument\n");
        return 1;
    }
    //convert string in argv to int key
    int key = atoi(argv[1]);


        {
            printf("plaintext: ");
            string s = get_string();
            printf("plaintext: %s\n", s);
            printf("ciphertext: ");

            //iterate over each character in string so long as less than length of string
            for (int i = 0, n = strlen(s); i < n; i++)

            //print ith character in string + key formula is ci = (pi +k) mod 26. mod 26 wraps around alphabet

                {
                    if (islower(s[i]))
                    printf("%c", (((s[i] + key) - 'a') % 26) + 'a');
                    else if (isupper(s[i]))
                    printf("%c", (((s[i] + key) - 'A') % 26) + 'A');
                }

            printf("\n");
        }
    return 0;
}


