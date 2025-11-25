// listen for extension install
chrome.runtime.onInstalled.addListener(() => {
  // only create our menu item once
  chrome.contextMenus.create({
    id: "TestV3",
    title: "V3 Test",
    // show the menu over everything
    contexts: ["all"]
  });
});

// listen for a browser session start
chrome.runtime.onStartup.addListener(() => {
  // initialize the click counter to zero
  chrome.storage.local.set({ clickCounter: 0 }, function() {
    // let us know it worked
    console.log("V3 Test: initialized test click counter to 0");
  });
});

// what to do when our menu is clicked
chrome.contextMenus.onClicked.addListener(event => {
  // get the current value
  chrome.storage.local.get("clickCounter", result => {
    // bump the count
    result.clickCounter = result.clickCounter + 1;
    // update local storage
    chrome.storage.local.set({ clickCounter: result.clickCounter }, function() {
      // let us know it worked
      console.log(
        "V3 Test: updated test click counter to " + result.clickCounter
      );
    });
  });
});
