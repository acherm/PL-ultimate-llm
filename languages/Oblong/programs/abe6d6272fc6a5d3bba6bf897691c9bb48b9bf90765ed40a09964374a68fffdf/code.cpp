#include <libLoam/c/ob-retorts.h>
#include <libLoam/c/ob-log.h>
#include <libPlasma/c++/Slaw.h>

using namespace oblong::loam;
using namespace oblong::plasma;

int main(int argc, char **argv)
{
  OB_DIE_ON_ERROR(OB_CHECK_ABI());

  Slaw s = Slaw::List(Slaw::String("hello"),
                      Slaw::String("world"),
                      Slaw::Number(42));

  OB_LOG_INFO("Created slaw: %s\n", s.toPrintableString().c_str());

  return EXIT_SUCCESS;
}
