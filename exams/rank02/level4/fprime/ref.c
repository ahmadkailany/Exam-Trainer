#include <stdio.h>
#include <stdlib.h>
int main(int ac, char **av)
{
	if (ac == 2)
	{
		int n = atoi(av[1]), first = 1;
		if (n == 1)
			printf("1");
		for (int d = 2; n > 1; d++)
			while (n % d == 0)
			{
				printf(first ? "%d" : "*%d", d);
				first = 0;
				n /= d;
			}
	}
	printf("\n");
	return (0);
}
