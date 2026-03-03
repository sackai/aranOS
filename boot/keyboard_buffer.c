#include "keyboard_buffer.h"

#define KB_BUF_SIZE 128

static char buffer[KB_BUF_SIZE];
static int head = 0;
static int tail = 0;

int keyboard_buffer_empty(void) {
    return head == tail;
}

void keyboard_buffer_push(char c) {
    int next = (head + 1) % KB_BUF_SIZE;
    if (next == tail) return; // buffer full → drop key
    buffer[head] = c;
    head = next;
}

char keyboard_buffer_pop(void) {
    if (head == tail) return 0;
    char c = buffer[tail];
    tail = (tail + 1) % KB_BUF_SIZE;
    return c;
}
