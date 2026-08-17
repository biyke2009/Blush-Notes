import turtle

t = turtle.Turtle()
t.speed(0)

def tree(i):
    if i < 10:
        return

    t.forward(i)

    t.color("pink")
    t.circle(2)
    t.color("brown")

    t.left(20)
    tree(4 * i / 5)

    t.right(40)
    tree(4 * i / 5)

    t.left(20)
    t.backward(i)


tree(100)

turtle.done()