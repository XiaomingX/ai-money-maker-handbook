// let us know we're running
console.log("A script has run from chrome.tabs.executeScript via Manifest V3.");

// send a message to the background requesting that a context menu be attached
chrome.runtime.sendMessage({
  cmd: "addMenu"
});

// listen for messages from the background
chrome.runtime.onMessage.addListener(r => {
  console.log(r);
});
