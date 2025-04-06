/**
 * Buffer Overflow (64-bit). Case 3: Static ROP
 * Compile: gcc main.c -o main -no-pie
 */


#include <stdio.h>
#include <unistd.h>

void ROP() {
  asm("pop %rdi\n\t"
      "ret");
}

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
