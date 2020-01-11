#include <stdio.h>

void popularArray(int *a, int i, int n)
{
    if(i < n)
    {        
        scanf("%d", (a+i));
        popularArray(*&a, ++i, n);
    }
}

void printArray(int *a, int i, int n)
{
  if(i < n)
  {
    printf("%d, ", *(a + i));
    printArray(*&a, ++i, n);
  }
}

void jogo(int *tabuleiro, int *jogadores, int n, int m, int o, int rodada, int jogadores)
{
  if(rodada < o && jogadores < m  )
  {
    if(jogadores == m)
    {
      jogadores = 0;
      rodada = 
    }

    jogo(*&tabuleiro, *&jogadores, n, m, o, rodada, jogadores);
  }

}

int main()
{
    int n, m, o;
    scanf("%d%d%d", &n, &m, &o);
    int tabuleiro[n];
    int jogadores[1000] = {0};

    popularArray(tabuleiro, 0, n);
    printArray(tabuleiro, 0, n);
    printArray(jogadores, 0, m);

    return 0;
}