var registerForScript, loadScripts;
(function () {
  var scriptHooks = [];

  registerForScript = function (vdocId, moduleText) {
    scriptHooks.push([vdocId, moduleText]);
  }

  function go(caja) {
    for (var i = 0; i < scriptHooks.length; i++) {
      var id         = scriptHooks[i][0];
      var moduleText = scriptHooks[i][1];
      var sandbox = new caja.hostTools.Sandbox();
      sandbox.attach(document.getElementById(id));
      sandbox.runCajoledModuleString(moduleText);
    }
    scriptHooks = [];
  }

  loadScripts = function (server) {
    loadCaja(go, {
      debug: true,
      cajaServer: server
    });
  }
})();
