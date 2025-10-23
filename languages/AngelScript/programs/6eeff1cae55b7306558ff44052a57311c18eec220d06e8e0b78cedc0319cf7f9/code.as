// The function that will be executed as a coroutine
void MyCoroutine(array<string> &in args)
{
  // The coroutine will suspend its execution and return to the caller
  yield();

  // When the host application resumes the coroutine, it will
  // continue execution from here.
  for( uint n = 0; n < args.length(); n++ )
    print(args[n] + "\n");
}

// The main function that will start the coroutine
void main()
{
  // Create a new coroutine
  createCoroutine("MyCoroutine", {"hello", "world"});

  // The coroutine has been created, but not yet executed.
  // The host application can now resume the execution when it wants.
}