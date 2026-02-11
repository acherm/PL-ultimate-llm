<?hh

namespace HelloHackWorld\Controllers;

class BaseController {
  public static function getResponse(): array<string, mixed> {
    return array(
      'success' => true,
      'data' => array(
        'message' => 'Welcome to Hack!',
        'timestamp' => time(),
      ),
    );
  }

  public static function sendResponse(): void {
    $response = static::getResponse();
    header('Content-Type: application/json');
    print json_encode($response);
  }
}