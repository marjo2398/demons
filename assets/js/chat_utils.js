function linkify(text) {
    var urlRegex =/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig;
    return text.replace(urlRegex, function(url) {
        var escapeHTML = function(s) {
            return s.replace(/&/g, '&amp;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#39;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;');
        };
        var escapedUrl = escapeHTML(url);
        return '<a href="' + escapedUrl + '" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">' + escapedUrl + '</a>';
    });
}

// Export for CommonJS (Node.js/Jest environment)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { linkify };
}
