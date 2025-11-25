chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Message received!");
  console.log("request: ", request);
  console.log("sender: ", sender);
  if (request.cmd === "runLogic") {
    chrome.tabs.executeScript(sender.tab.id, {
      file: "js/logic.js"
    });
  }
});
