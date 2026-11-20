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
void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)());
static t_list *build(int ac, char **av, int from)
{
	t_list *head = NULL;
	for (int i = ac - 1; i >= from; i--)
	{
		t_list *n = malloc(sizeof(t_list));
		n->data = strdup(av[i]);
		n->next = head;
		head = n;
	}
	return (head);
}
int main(int ac, char **av)
{
	t_list *l = build(ac, av, 2);
	ft_list_remove_if(&l, av[1], strcmp);
	if (!l) ps("(empty list)");
	for (t_list *c = l; c; c = c->next) { ps((char *)c->data); if (c->next) ps(" -> "); }
	pnl();
	return (0);
}
