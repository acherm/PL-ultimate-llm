[@react.component]
let make = (~message) => {
  let (count, setCount) = React.useState(() => 0);

  <div>
    <div> {React.string(message)} </div>
    <div> {React.string("Count: " ++ string_of_int(count))} </div>
    <button onClick={_event => setCount(_ => count + 1)}>
      {React.string("Click me")}
    </button>
  </div>;
};