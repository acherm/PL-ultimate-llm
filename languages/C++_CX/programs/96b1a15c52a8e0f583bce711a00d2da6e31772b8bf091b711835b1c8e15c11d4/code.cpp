// Hello World in C++/CX (Windows Runtime)
using namespace Platform;

[Platform::MTAThread]
int main(Platform::Array<Platform::String^>^ args)
{
    Platform::String^ message = "Hello, World from C++/CX!";
    // In a real WinRT app, you would use Windows APIs to display this
    // For console output in a minimal example:
    std::wstring ws(message->Begin(), message->End());
    wprintf(L"%s\n", ws.c_str());
    return 0;
}
