function openPage() {
  browser.tabs.query({currentWindow: true, active: true})
    .then((tabs) => {
      browser.tabs.create({
	      url: 'https://demo.webis.de/police-pr?search=' + encodeURIComponent(tabs[0].url)
      });
  })
}

browser.browserAction.onClicked.addListener(openPage);
