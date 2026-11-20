#include <unistd.h>
int main(int ac, char **av)
{
	if (ac == 3)
		for (int i = 0; av[1][i]; i++)
		{
			int seen = 0, j;
			for (j = 0; j < i; j++)
				if (av[1][j] == av[1][i])
					seen = 1;
			if (seen)
				continue ;
			for (j = 0; av[2][j]; j++)
				if (av[2][j] == av[1][i])
				{
					write(1, &av[1][i], 1);
					break ;
				}
		}
	write(1, "\n", 1);
	return (0);
}
