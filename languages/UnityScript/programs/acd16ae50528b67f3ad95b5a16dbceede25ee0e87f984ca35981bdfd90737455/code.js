#pragma strict
public class MyGameClass extends MonoBehaviour {
	function MyGameMethod() {
		// Message with a link to an object.
		Debug.Log("Hello", gameObject);
		// Message using rich text.
		Debug.Log("<color=red>Fatal error:</color> AssetBundle not found");
	}
}
