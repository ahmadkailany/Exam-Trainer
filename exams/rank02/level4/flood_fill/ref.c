#include "flood_fill.h"
static void fill(char **tab, t_point size, int x, int y, char c)
{
	if (x < 0 || y < 0 || x >= size.x || y >= size.y || tab[y][x] != c)
		return ;
	tab[y][x] = 'F';
	fill(tab, size, x + 1, y, c);
	fill(tab, size, x - 1, y, c);
	fill(tab, size, x, y + 1, c);
	fill(tab, size, x, y - 1, c);
}
void flood_fill(char **tab, t_point size, t_point begin)
{
	fill(tab, size, begin.x, begin.y, tab[begin.y][begin.x]);
}
