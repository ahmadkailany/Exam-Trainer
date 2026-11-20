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
#include "list.h"
t_list *sort_list(t_list *lst, int (*cmp)(int, int));
int ascending(int a, int b) { return (a <= b); }
int descending(int a, int b) { return (a >= b); }
int main(int ac, char **av)
{
	t_list *head = NULL;
	for (int i = ac - 1; i >= 2; i--)
	{
		t_list *n = malloc(sizeof(t_list));
		n->data = atoi(av[i]);
		n->next = head;
		head = n;
	}
	head = sort_list(head, av[1][0] == 'd' ? descending : ascending);
	for (t_list *c = head; c; c = c->next) { pn(c->data); if (c->next) ps(" "); }
	pnl();
	return (0);
}
