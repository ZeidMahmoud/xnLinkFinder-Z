chrome.webRequest.onCompleted.addListener(
    (details) => {
        if (details.url) {
            chrome.storage.local.get(['endpoints'], (result) => {
                const endpoints = result.endpoints || [];
                if (!endpoints.includes(details.url)) {
                    endpoints.push(details.url);
                    chrome.storage.local.set({endpoints});
                }
            });
        }
    },
    {urls: ["<all_urls>"]}
);
