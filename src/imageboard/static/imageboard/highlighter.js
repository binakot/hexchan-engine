var Highlighter = function(props) {
    var localCollection = new LocalCollection({
        key: props.storageKey
    });

    function init() {
        // Write new items into collection
        localCollection.concat(props.cookieData);

        // Add attributes for styling marked elements
        var elements = document.querySelectorAll(props.selector);
        var element, elementId;

        for (var i = 0; i < elements.length; i++) {
            element = elements[i];
            elementId = element.getAttribute('data-id');
            if (localCollection.check(elementId)) {
                element.setAttribute('data-user', true);
                if (props.title) {
                    element.setAttribute('title', props.title);
                }
            }
        }
    }

    function destroy() {
        localCollection.destroy();
    }

    init();
    return {
        destroy: destroy
    };
};


// Parse cookies
var cookieData = {};
document.cookie.split('; ').forEach(function (cookieKeyValue) {
    var keyValueArray = cookieKeyValue.split('=');
    try {
        cookieData[keyValueArray[0]] = keyValueArray[1].split('#');
    } catch (err) {
        cookieData[keyValueArray[0]] = [];
    }
});

var userThreadsHighlighter = new Highlighter({
    cookieData: cookieData['user_threads'],
    storageKey: 'userThreads',
    selector: '.js-thread-hid',
    // title: 'Мой тред'
});

var userPostsHighlighter = new Highlighter({
    cookieData: cookieData['user_posts'],
    storageKey: 'userPosts',
    selector: '.js-post-hid',
    // title: 'Мой пост'
});
