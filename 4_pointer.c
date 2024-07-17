
int main()
{
    int a = 41;
    int *b = &a;
    *b += 1;

    if (a > 42)
    {
        a += 42;
    } else {
        a -= 1;
    }
    return 0;
}