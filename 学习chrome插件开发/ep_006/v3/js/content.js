// send a message to the background requesting our business logic
chrome.runtime.sendMessage({
  cmd: "runLogic"
});

// send a message to the background requesting that a context menu be attached
chrome.runtime.sendMessage({
  cmd: "addMenu"
});
