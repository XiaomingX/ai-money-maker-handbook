// our unique ID, so we know which messages to pass back to content scripts
const ME = "background";

// what to do when someone clicks our menu item
const handleMenuClick = (event, tabId) => {
  chrome.tabs.sendMessage(tabId, {
    // send a command that will only be run by our logic script
    to: "logic",
    // logic will open an overlay
    cmd: "openOverlay",
    args: {
      // name of overlay
      overlay: "scrape",
      // should we keep it hidden
      hidden: true,
      // a unique id so we can close it later
      id: chrome.runtime.id + "_" + new Date().getTime(),
      // the URL of the image we're going to scrape
      oldImageSrc: event.srcUrl
    }
  });
};

// commands we are willing to execute on behalf of processes running outside this script
const cmd = {
  // inject our business logic (via content.js)
  runLogic: (request, sender) => {
    chrome.tabs.executeScript(sender.tab.id, {
      file: "js/logic.js"
    });
  },
  // add our context menu
  addMenu: () => {
    // don't try to duplicate this menu item
    chrome.contextMenus.removeAll();
    // create a menu
    chrome.contextMenus.create({
      id: "TestV3",
      title: "V3 Test",
      // show the menu over images
      contexts: ["image"]
    });
    // handle interactions with addListener
    chrome.contextMenus.onClicked.addListener(event => {
      // because the click came from a global UI element we need to figure out which tab it came from
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
        // pass the event AND the tab ID, which should be in tabs[0]
        handleMenuClick(event, tabs[0].id);
      });
    });
  },
  // handle scraped image data
  handleImageData: (request, sender) => {
    // send a message to the same tab that made the request
    chrome.tabs.sendMessage(sender.tab.id, {
      // send only to the logic process
      to: "logic",
      // logic.cmd.renderAlteredImage
      cmd: "renderAlteredImage",
      // args to render
      args: {
        // the old image URL, which we will need to seek out
        oldImageSrc: request.args.oldImageSrc,
        // the updated data:uri our overlay built and sent back
        newImageSrc: request.args.newImageSrc
      }
    });
  }
};

// listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender) => {
  // do we know what tab this request came from?
  if (sender.tab.id) {
    // is there a command?
    if (request.cmd) {
      // do we need to redirect to a content script?
      if (request.to && request.to !== ME) {
        // send it
        chrome.tabs.sendMessage(sender.tab.id, {
          to: request.to,
          cmd: request.cmd,
          args: request.args
        });
      } else {
        // can we carry out this command here?
        if (typeof cmd[request.cmd] === "function") {
          cmd[request.cmd](request, sender);
        }
      }
    }
  }
});
