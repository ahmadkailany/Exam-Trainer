#include <unistd.h>
int main(int ac, char **av)
{
	if (ac == 2)
		for (int i = 0; av[1][i]; i++)
		{
			int n = 1;
			if (av[1][i] >= 'a' && av[1][i] <= 'z') n = av[1][i] - 'a' + 1;
			else if (av[1][i] >= 'A' && av[1][i] <= 'Z') n = av[1][i] - 'A' + 1;
			while (n--)
				write(1, &av[1][i], 1);
		}
	write(1, "\n", 1);
	return (0);
}
