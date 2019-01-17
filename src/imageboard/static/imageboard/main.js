// Lightbox config
lightbox.option({
    resizeDuration: 300,
    fadeDuration: 300,
    imageFadeDuration: 300,
});


// Post and threads hiders
var threadHider = new Hider({
    type: 'thread',
    storageKey: 'hiddenThreads',
    placeholderLabel: 'Тред скрыт.'
});

var postHider = new Hider({
    type: 'post',
    storageKey: 'hiddenPosts',
    placeholderLabel: 'Пост скрыт.'
});


// Highlight user's posts and threads
function getCookieArray(key) {
    var cookieStr = Cookies.get(key);
    return cookieStr ? cookieStr.split('#') : [];
}

var userThreadsHighlighter = new Highlighter({
    cookieData: getCookieArray('user_threads'),
    storageKey: 'userThreads',
    selector: '.js-thread-hid'
});

var userPostsHighlighter = new Highlighter({
    cookieData: getCookieArray('user_posts'),
    storageKey: 'userPosts',
    selector: '.js-post-hid'
});


// Create popup for refs
var refPopup = new RefPopup();
