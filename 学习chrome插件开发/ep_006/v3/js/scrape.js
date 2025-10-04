// message.to must match this or messages from the background will be ignored
const ME = "scrape";

// transform an image into very large pixels
const deRezz = (img, canvas) => {
  // how big will our squares be?
  const chunkSize = 20;
  // a canvas has several possible contexts; this is the one that will let us draw an image
  let context = canvas.getContext("2d");
  // disable image smoothing, which may give us different results for different browsers
  context.imageSmoothingEnabled = false;
  // draw the image full-size, to exactly fill canvas
  context.drawImage(img, 0, 0, canvas.width, canvas.height);
  // convert what's on the canvas to an image data object
  let imageData = context.getImageData(0, 0, canvas.width, canvas.height).data;
  // for our demo: downsample into big blocks of color
  let row, column, pixel;
  for (row = 0; row < canvas.height; row = row + chunkSize) {
    for (col = 0; col < canvas.width; col = col + chunkSize) {
      pixel = (row * canvas.width + col) * 4;
      context.fillStyle =
        "#" +
        ("00" + imageData[pixel].toString(16)).substr(-2, 2) +
        ("00" + imageData[pixel + 1].toString(16)).substr(-2, 2) +
        ("00" + imageData[pixel + 2].toString(16)).substr(-2, 2);
      context.fillRect(col, row, chunkSize, chunkSize);
    }
  }
};

// a list of commands we are willing to carry out when the background process asks
const cmd = {
  // stand by to
  render: (message, sender) => {
    // burn after reading; this function may get called multiple times if there are iframes on the page
    delete cmd.render;
    // create an image tag
    let img = new Image();
    // on load, do stuff
    img.onload = () => {
      // make a canvas
      let canvas = document.createElement("CANVAS");
      // set canvas dimensions to the image's real dimensions
      canvas.height = img.naturalHeight;
      canvas.width = img.naturalWidth;
      // run the image through a transformation function
      deRezz(img, canvas);
      // throw it back to the background process, which will bounce the new image
      // to the content script, which will render it in place of the original
      chrome.runtime.sendMessage(
        {
          cmd: "handleImageData",
          args: {
            oldImageSrc: message.args.oldImageSrc,
            newImageSrc: canvas.toDataURL("image/png")
          }
        },
        // here we make use of the automatic response, which we get for free
        response => {
          // prevent message-port-closed warning from showing in console
          let lastErr = chrome.runtime.lastError;
          // ask the background to ask the business logic to close our host overlay
          chrome.runtime.sendMessage({
            to: "logic",
            cmd: "closeOverlay",
            args: {
              id: message.args.id
            }
          });
        }
      );
    };
    // set the image source
    img.src = message.args.oldImageSrc;
  }
};

// listen for messages from the background
chrome.runtime.onMessage.addListener((message, sender) => {
  // is the message for us?
  if (message.to && message.to === ME) {
    // do we have a valid command?
    if (message.cmd && typeof cmd[message.cmd] === "function") {
      // run it, passing the full message object
      cmd[message.cmd](message, sender);
    }
  }
});
