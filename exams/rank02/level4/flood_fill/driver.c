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
#include "flood_fill.h"
int main(int ac, char **av)
{
	t_point begin = {atoi(av[1]), atoi(av[2])};
	t_point size = {(int)strlen(av[3]), ac - 3};
	char **tab = malloc(sizeof(char *) * size.y);
	for (int i = 0; i < size.y; i++)
		tab[i] = strdup(av[i + 3]);
	flood_fill(tab, size, begin);
	for (int i = 0; i < size.y; i++) { ps(tab[i]); pnl(); }
	return (0);
}
