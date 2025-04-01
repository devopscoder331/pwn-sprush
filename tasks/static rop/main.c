#include <stdio.h>
#include <unistd.h>

void func() {
  char buffer[32];
  read(0, buffer, 256);
}

int main() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  puts("Hello dude!");
  func();
}
