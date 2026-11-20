#include <unistd.h>
int main(int ac, char **av)
{
	if (ac == 3)
	{
		unsigned char seen[256] = {0};
		for (int k = 1; k <= 2; k++)
			for (int i = 0; av[k][i]; i++)
				if (!seen[(unsigned char)av[k][i]])
				{
					seen[(unsigned char)av[k][i]] = 1;
					write(1, &av[k][i], 1);
				}
	}
	write(1, "\n", 1);
	return (0);
}
