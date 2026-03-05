<?hh
use namespace Facebook\XHP\HTML;

async function render_greeting(string $name): Awaitable<string> {
  $xhp = <div class="greeting">
    <h1>Hello, {$name}!</h1>
    <p>Welcome to XHP templating.</p>
  </div>;
  return await $xhp->toStringAsync();
}

<<__EntryPoint>>
async function main(): Awaitable<void> {
  echo await render_greeting('World');
}
