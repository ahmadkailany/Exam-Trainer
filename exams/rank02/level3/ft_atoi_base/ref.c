static int val(char c)
{
	if (c >= '0' && c <= '9') return (c - '0');
	if (c >= 'a' && c <= 'f') return (c - 'a' + 10);
	if (c >= 'A' && c <= 'F') return (c - 'A' + 10);
	return (-1);
}
int ft_atoi_base(const char *str, int str_base)
{
	int s = 1, r = 0, v;
	if (*str == '-')
	{
		s = -1;
		str++;
	}
	while ((v = val(*str)) >= 0 && v < str_base)
	{
		r = r * str_base + v;
		str++;
	}
	return (r * s);
}
