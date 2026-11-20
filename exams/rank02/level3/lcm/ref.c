unsigned int lcm(unsigned int a, unsigned int b)
{
	unsigned int x = a, y = b, t;
	if (!a || !b)
		return (0);
	while (y)
	{
		t = x % y;
		x = y;
		y = t;
	}
	return (a / x * b);
}
