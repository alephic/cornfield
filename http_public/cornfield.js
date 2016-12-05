
"use strict";

window.addEventListener('load', function(e) {
  var ws = new WebSocket('ws://'+window.location.hostname+':8765/');
  ws.addEventListener('open', function(e) {
    //ws.send("foo");
  });
  ws.addEventListener('message', function(e) {
    var logEntry = document.createElement('div');
    logEntry.appendChild(document.createTextNode(e.data));
    document.getElementById('log').appendChild(logEntry);
  });
  function submit() {
    var prompt = document.getElementById('prompt');
    ws.send(prompt.value);
    prompt.value = '';
  }
  document.getElementById('prompt').addEventListener('keydown', function(e) {
    if (e.key) {
      if (e.key == 'Enter') {
        submit();
      }
    } else if (e.which) {
      if (e.which == 13) {
        submit();
      }
    }
  });
  document.getElementById('prompt').focus();
  window.addEventListener('click', function(e) {
    document.getElementById('prompt').focus();
  })
});
