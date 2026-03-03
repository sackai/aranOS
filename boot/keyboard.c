#include <stdint.h>
#include "irq.h"
#include "port_io.h"
#include "keyboard.h"

static int shift = 0;

static const char normal[128] = {
    0,27,'1','2','3','4','5','6','7','8','9','0','-','=', '\b',
    '\t','q','w','e','r','t','y','u','i','o','p','[',']','\n',
    0,'a','s','d','f','g','h','j','k','l',';','\'','`',0,'\\',
    'z','x','c','v','b','n','m',',','.','/',0,'*',0,' '
};

static const char shifted[128] = {
    0,27,'!','@','#','$','%','^','&','*','(',')','_','+', '\b',
    '\t','Q','W','E','R','T','Y','U','I','O','P','{','}','\n',
    0,'A','S','D','F','G','H','J','K','L',':','"','~',0,'|',
    'Z','X','C','V','B','N','M','<','>','?',0,'*',0,' '
};

extern void keyboard_buffer_push(char c);

static void keyboard_irq(void) {
    uint8_t sc = inb(0x60);

    if (sc == 0x2A || sc == 0x36) { shift = 1; goto end; }
    if (sc == 0xAA || sc == 0xB6) { shift = 0; goto end; }
    if (sc & 0x80) goto end;

    char c = shift ? shifted[sc] : normal[sc];
    if (c) keyboard_buffer_push(c);

end:
    outb(0x20, 0x20);
}

void keyboard_install(void) {
    irq_register_handler(1, keyboard_irq);
}
