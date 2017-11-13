#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("missing command-line argument, or ONLY enter one word\n");
        return 1;
    }
     for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        //check if each character is alphabetic. Isalpha function returns non-zero value if c is an alphabet, else it returns 0.
        if (isalpha(argv[1][i]) == 0)
        {
        printf("keyword must ONLY contain alphabetical characters \n");
        return 1;
        }
    }

    //assign value in string argv to string keyword used to encipher the plaintext
    string keyword = (argv[1]);

        {
            printf("enter plaintext to encipher: ");
            string plaintext = get_string();
            printf("plaintext: %s\n", plaintext);
            printf("ciphertext: ");

            //iterate over each character in plaintext so long as less than length of plaintext
            //declare variables i/j/n/m - could potentially do this at beginning instead of jsut within scope of for loop?
            for (int i = 0, j = 0, n = strlen(plaintext), m = strlen(keyword); i < n; i++, j++)

            //track position in keyword and iterate through jth character independently, reset to 0 if j >= length keyword to continue looping through
            {
                if (j >= m)
                    {
                        j = 0;
                    }
                        //jth character in keyword gets assigned 0,1,2 etc. by subtracting ASCII value of a/A
                        {
                            if (islower(plaintext[i]) && islower(keyword[j]))
                            printf("%c", (((plaintext[i] - 'a') + (keyword[j] - 'a')) % 26) + 'a');
                            else if (isupper(plaintext[i]) && isupper(keyword[j]))
                            printf("%c", (((plaintext[i] - 'A') + (keyword[j] - 'A')) % 26) + 'A');
                            else if (isupper(plaintext[i]) && islower(keyword[j]))
                            printf("%c", (((plaintext[i] - 'A') + (keyword[j] - 'a')) % 26) + 'A');
                            else if (islower(plaintext[i]) && isupper(keyword[j]))
                            printf("%c", (((plaintext[i] - 'a') + (keyword[j] - 'A')) % 26) + 'a');
                        }
            }
            printf("\n");
        }
    return 0;
}
