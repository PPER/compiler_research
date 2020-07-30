#include <stdio.h>
#include <stdlib.h>

int main()
{

  int in[1000]; 
  int i,j;
  FILE* myfile;
  int b =0;
  b+b;
  for (i = 0; i < 1000; i++)
  {
    in[i] = 0;
    in[i] -= 10;
  }   

  for (j = 100; j < 1000; j++)
  {
   in[j]+= 10;
   in[j] -= 30;
  }


  for (i = 0; i< 1000; i++){
	FILE *fp;
	fp = fopen("output", "w+");
    fprintf(fp,"%d\n", in[i]);
	fclose(fp);
  }
  return 1;
}

