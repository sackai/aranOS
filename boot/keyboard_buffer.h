#ifndef KEYBOARD_BUFFER_H
#define KEYBOARD_BUFFER_H

int keyboard_buffer_empty(void);
void keyboard_buffer_push(char c);
char keyboard_buffer_pop(void);

#endif
