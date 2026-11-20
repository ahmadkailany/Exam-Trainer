#include <stdio.h>
#include <stdlib.h>
int main(int ac, char **av)
{
	if (ac == 3)
	{
		int a = atoi(av[1]), b = atoi(av[2]), t;
		while (b)
		{
			t = a % b;
			a = b;
			b = t;
		}
		printf("%d", a);
	}
	printf("\n");
	return (0);
}
