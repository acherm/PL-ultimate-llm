/* stack.v -- Vault typestate example
 * A fixed-size integer stack with compile-time state tracking.
 * Adapted from examples in DeLine & Fahndrich, PLDI 2002.
 */

#define MAXSTACK 64

typedef struct _Stack {
    int   data[MAXSTACK];
    int   top;
} Stack;

/* Track whether a stack slot holds a value */
trackattr_t StackState;

void stack_init(Stack *[StackState=empty] s) {
    s->top = 0;
}

int stack_empty(Stack *[StackState=empty|nonempty] s) {
    return (s->top == 0);
}

void stack_push(Stack *[StackState=empty|nonempty -> nonempty] s, int v) {
    s->data[s->top] = v;
    s->top = s->top + 1;
}

int stack_pop(Stack *[StackState=nonempty -> empty|nonempty] s) {
    s->top = s->top - 1;
    return s->data[s->top];
}

int main(void) {
    Stack st;
    int i;
    int v;

    adopt(&st) with StackState: empty;
    stack_init(&st);

    for (i = 1; i <= 10; i = i + 1) {
        stack_push(&st, i * i);
    }

    while (!stack_empty(&st)) {
        v = stack_pop(&st);
        printf("%d\n", v);
    }

    return 0;
}
