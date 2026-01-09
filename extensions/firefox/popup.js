document.getElementById('capture').addEventListener('click', () => {
    chrome.storage.local.get(['endpoints'], (result) => {
        const endpoints = result.endpoints || [];
        document.getElementById('endpoints').innerHTML = 
            endpoints.map(e => `<div>${e}</div>`).join('');
    });
});

document.getElementById('export').addEventListener('click', () => {
    chrome.storage.local.get(['endpoints'], (result) => {
        const blob = new Blob([JSON.stringify(result.endpoints, null, 2)], 
                             {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        chrome.downloads.download({url, filename: 'xnlinkfinder-results.json'});
    });
});
