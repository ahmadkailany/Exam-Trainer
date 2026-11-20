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
#include "ft_list.h"
int ft_list_size(t_list *begin_list);
int main(int ac, char **av)
{
	t_list *head = NULL;
	for (int i = ac - 1; i >= 1; i--)
	{
		t_list *n = malloc(sizeof(t_list));
		n->data = av[i];
		n->next = head;
		head = n;
	}
	pn(ft_list_size(head)); pnl();
	return (0);
}
