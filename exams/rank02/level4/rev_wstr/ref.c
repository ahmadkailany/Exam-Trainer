#include <unistd.h>
int main(int ac, char **av)
{
	if (ac == 2)
	{
		int end = 0, first = 1;
		while (av[1][end])
			end++;
		while (end > 0)
		{
			while (end > 0 && (av[1][end - 1] == ' ' || av[1][end - 1] == '\t'))
				end--;
			int start = end;
			while (start > 0 && av[1][start - 1] != ' ' && av[1][start - 1] != '\t')
				start--;
			if (start < end)
			{
				if (!first)
					write(1, " ", 1);
				first = 0;
				write(1, av[1] + start, end - start);
			}
			end = start;
		}
	}
	write(1, "\n", 1);
	return (0);
}
