#include <unistd.h>
static int blank(char c) { return (c == ' ' || c == '\t'); }
int main(int ac, char **av)
{
	if (ac >= 2)
	{
		char *s = av[1];
		int i = 0, fs, fe, printed = 0;
		while (s[i] && blank(s[i]))
			i++;
		fs = i;
		while (s[i] && !blank(s[i]))
			i++;
		fe = i;
		while (s[i])
		{
			while (s[i] && blank(s[i]))
				i++;
			int st = i;
			while (s[i] && !blank(s[i]))
				i++;
			if (i > st)
			{
				write(1, s + st, i - st);
				write(1, " ", 1);
				printed = 1;
			}
		}
		(void)printed;
		write(1, s + fs, fe - fs);
	}
	write(1, "\n", 1);
	return (0);
}
