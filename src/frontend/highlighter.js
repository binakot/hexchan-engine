import LocalCollection from './localCollection';


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


export default Highlighter;
