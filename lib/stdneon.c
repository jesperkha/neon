// neon stdlib
#include "neon.h"
#include <stdio.h>

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
