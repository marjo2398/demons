const { linkify } = require('../assets/js/chat_utils.js');

test('replaces http urls with a link', () => {
    expect(linkify('check out http://example.com')).toBe('check out <a href="http://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com</a>');
});

test('replaces https urls with a link', () => {
    expect(linkify('check out https://example.com')).toBe('check out <a href="https://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">https://example.com</a>');
});

test('does not match non-url content', () => {
    expect(linkify('hello world')).toBe('hello world');
});

test('handles multiple urls', () => {
    expect(linkify('http://example.com and https://example.org')).toBe('<a href="http://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com</a> and <a href="https://example.org" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">https://example.org</a>');
});

test('handles ftp urls', () => {
    expect(linkify('ftp://example.com')).toBe('<a href="ftp://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">ftp://example.com</a>');
});

test('handles file urls', () => {
    expect(linkify('file://path/to/file.txt')).toBe('<a href="file://path/to/file.txt" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">file://path/to/file.txt</a>');
});

test('ignores punctuation at the end of the url', () => {
    expect(linkify('check out http://example.com.')).toBe('check out <a href="http://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com</a>.');
    expect(linkify('is it http://example.com?')).toBe('is it <a href="http://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com</a>?');
});

test('handles complex urls with query parameters', () => {
    expect(linkify('http://example.com/path?query=1&param=2')).toBe('<a href="http://example.com/path?query=1&amp;param=2" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com/path?query=1&amp;param=2</a>');
});

test('handles urls with hashes', () => {
    expect(linkify('http://example.com/path#hash')).toBe('<a href="http://example.com/path#hash" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com/path#hash</a>');
});

test('handles urls without spaces before or after', () => {
    expect(linkify('(http://example.com)')).toBe('(<a href="http://example.com" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com</a>)');
});

test('escapes HTML entities in URL to prevent XSS in href', () => {
    expect(linkify('http://example.com/&quot;onmouseover=&quot;alert(1)')).toBe('<a href="http://example.com/&amp;quot;onmouseover=&amp;quot;alert" target="_blank" rel="noopener noreferrer" class="link-highlight break-all">http://example.com/&amp;quot;onmouseover=&amp;quot;alert</a>(1)');
});

test('handles urls with javascript: scheme correctly (does not match)', () => {
    expect(linkify('javascript:alert(1)')).toBe('javascript:alert(1)');
});
