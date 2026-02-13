let%server _ =
  Eliom_registration.Html.create
    ~path:(Eliom_service.Path ["hello"])
    ~meth:(Eliom_service.Get Eliom_parameter.unit)
    (fun () () ->
      Lwt.return
        Eliom_tools.F.(html ~title:"Hello"
          (body [h1 [txt "Hello World!"];
                 p [txt "Welcome to Eliom"]])))
