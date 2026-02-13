import "@typespec/http";
import "@typespec/rest";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
  title: "Pet Store API",
})
namespace PetStore;

model Pet {
  id: int32;
  name: string;
  age: int32;
  species: "dog" | "cat" | "bird";
}

model Error {
  code: int32;
  message: string;
}

@route("/pets")
interface Pets {
  @get list(): Pet[];
  @post create(@body pet: Pet): Pet | Error;
  @get read(@path petId: int32): Pet | Error;
}
