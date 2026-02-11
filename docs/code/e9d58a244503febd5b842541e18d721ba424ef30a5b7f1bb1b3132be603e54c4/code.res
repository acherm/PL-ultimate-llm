type state = {count: int}

type action =
  | Click
  | Reset

let initialState = {count: 0}

let reducer = (state, action) =>
  switch action {
  | Click => {count: state.count + 1}
  | Reset => {count: 0}
  }

@react.component
let make = () => {
  let (state, dispatch) = React.useReducer(reducer, initialState)

  let message = "You've clicked " ++ state.count->Int.toString ++ " times"

  <div>
    <button onClick={_ => dispatch(Click)}> {React.string(message)} </button>
    <button onClick={_ => dispatch(Reset)}> {React.string("Reset")} </button>
  </div>
}