// let us know we're running
console.log("Background service worker has loaded via Manifest V3.");

// clear, add, and listen to new context menu
const handleContextMenus = () => {
  // don't try to duplicate this menu item
  chrome.contextMenus.removeAll();

  // create a menu
  chrome.contextMenus.create({
    title: "V3 Test",
    id: "TestV3",
    // show the menu over everything
    contexts: ["all"]
    // IMPORTANT: because we are no longer using a
    // persistent background script we will need to
    // add an event listener outside contextMenus.create.
  });

  // handle interactions
  chrome.contextMenus.onClicked.addListener(menu => {
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      chrome.tabs.sendMessage(tabs[0].id, {
        msg: "Greetings from your Test V3 context menu"
      });
    });
  });
};

// listen for messages
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  // log the message
  console.log("Message received!", request);

  // has the content script asked to us execute our business logic?
  if (request.cmd === "runLogic") {
    chrome.tabs.executeScript(sender.tab.id, {
      file: "js/logic.js"
    });
  }

  // has our business logic asked us to add a menu?
  if (request.cmd === "addMenu") {
    handleContextMenus();
  }
});
