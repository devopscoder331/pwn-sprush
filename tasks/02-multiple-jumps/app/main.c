#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int first = 0;
int second = 0;

void win() {
  char* flag = getenv("FLAG");
  if (first && second)
    puts(flag);
}

void step1() {
  first = 1;
}

void step2() {
  second = 1;
}

void func() {
	char buffer[32];
	read(0, buffer, 128);
}

int main() {
	int a = 64;
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  func();
}
