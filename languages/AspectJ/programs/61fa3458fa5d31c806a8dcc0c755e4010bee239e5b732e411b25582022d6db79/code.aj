aspect LoggingAspect {
    pointcut publicMethods(): execution(public * *(..));

    before(): publicMethods() {
        System.out.println("Entering: " + thisJoinPoint.getSignature());
    }

    after(): publicMethods() {
        System.out.println("Exiting: " + thisJoinPoint.getSignature());
    }
}

class Example {
    public void doSomething() {
        System.out.println("Doing something...");
    }

    public static void main(String[] args) {
        new Example().doSomething();
    }
}