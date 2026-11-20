#include <unistd.h>
static int blank(char c) { return (c == ' ' || c == '\t'); }
int main(int ac, char **av)
{
	for (int k = 1; k < ac; k++)
	{
		for (int i = 0; av[k][i]; i++)
		{
			char c = av[k][i];
			if (c >= 'A' && c <= 'Z')
				c += 32;
			if (c >= 'a' && c <= 'z' && (i == 0 || blank(av[k][i - 1])))
				c -= 32;
			write(1, &c, 1);
		}
		write(1, "\n", 1);
	}
	if (ac < 2)
		write(1, "\n", 1);
	return (0);
}
