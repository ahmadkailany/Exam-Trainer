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
void sort_int_tab(int *tab, unsigned int size);
int main(int ac, char **av)
{
	int tab[600];
	for (int i = 1; i < ac; i++)
		tab[i - 1] = atoi(av[i]);
	sort_int_tab(tab, ac - 1);
	for (int i = 0; i < ac - 1; i++) { if (i) ps(" "); pn(tab[i]); }
	pnl();
	return (0);
}
