#include "stdlib.h"

struct node {
    void *value;
    struct node *next;
};

struct stack {
    struct node *head;
};

/*@
predicate nodes(struct node *node, int count) =
    node == 0 ?
        count == 0
    :
        0 < count &*& node->value |-> _ &*& node->next |-> ?next &*& malloc_block_node(node) &*& nodes(next, count - 1);

predicate stack(struct stack *stack, int count) =
    stack->head |-> ?head &*& malloc_block_stack(stack) &*& 0 <= count &*& nodes(head, count);
@*/

struct stack *create_stack()
    //@ requires true;
    //@ ensures stack(result, 0);
{
    struct stack *stack = malloc(sizeof(struct stack));
    if (stack == 0) { abort(); }
    stack->head = 0;
    //@ close nodes(0, 0);
    //@ close stack(stack, 0);
    return stack;
}

void stack_push(struct stack *stack, void *value)
    //@ requires stack(stack, ?count);
    //@ ensures stack(stack, count + 1);
{
    //@ open stack(stack, count);
    struct node *n = malloc(sizeof(struct node));
    if (n == 0) { abort(); }
    n->next = stack->head;
    n->value = value;
    stack->head = n;
    //@ close nodes(n, count + 1);
    //@ close stack(stack, count + 1);
}

void *stack_pop(struct stack *stack)
    //@ requires stack(stack, ?count) &*& 0 < count;
    //@ ensures stack(stack, count - 1);
{
    //@ open stack(stack, count);
    struct node *head = stack->head;
    //@ open nodes(head, count);
    void *result = head->value;
    stack->head = head->next;
    free(head);
    //@ close stack(stack, count - 1);
    return result;
}