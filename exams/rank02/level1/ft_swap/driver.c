#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static void ps(const char *s) { write(1, s, strlen(s)); }
static void pn(long long n)
{
	char b[32];
	int i = 31;
	unsigned long long u = n < 0 ? 0ULL - (unsigned long long)n : (unsigned long long)n;
	b[i] = 0;
	do { b[--i] = '0' + u % 10; u /= 10; } while (u);
	if (n < 0) b[--i] = '-';
	write(1, b + i, 31 - i);
}
static void pnl(void) { write(1, "\n", 1); }
void ft_swap(int *a, int *b);
int main(int ac, char **av)
{
	for (int i = 1; i + 1 < ac; i += 2)
	{
		int a = atoi(av[i]), b = atoi(av[i + 1]);
		ft_swap(&a, &b);
		pn(a); ps(" "); pn(b); pnl();
	}
	return (0);
}
