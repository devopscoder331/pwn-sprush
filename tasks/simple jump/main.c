#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void win() {
  char* flag = getenv("FLAG");
  puts(flag);
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
