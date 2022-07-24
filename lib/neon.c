// neon stdlib
#include "neon.h"
#include <stdio.h>
#include <string.h>

void neon_main();

int main(int argc, char** args)
{
	neon_main();
	return 0;
}

void println(char* msg)
{
	printf("%s\n", msg);
}

char* string_add(char* a, char* b)
{
	char* temp = a;
	strcat(temp, b);
	return temp;
}
