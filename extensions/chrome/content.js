// Extract endpoints from page
const links = Array.from(document.querySelectorAll('a')).map(a => a.href);
chrome.runtime.sendMessage({type: 'endpoints', data: links});
