#include <unistd.h>
static void hex(unsigned int n)
{
	if (n >= 16)
		hex(n / 16);
	write(1, &"0123456789abcdef"[n % 16], 1);
}
int main(int ac, char **av)
{
	if (ac == 2)
	{
		unsigned int n = 0;
		for (int i = 0; av[1][i] >= '0' && av[1][i] <= '9'; i++)
			n = n * 10 + av[1][i] - '0';
		hex(n);
	}
	write(1, "\n", 1);
	return (0);
}
