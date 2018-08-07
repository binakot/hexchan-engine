var LocalCollection = function(props) {
    var collection;

    function onStorageUpdate(ev){
        if (ev.key === props.key) {
            collection = JSON.parse(ev.newValue);
            if (typeof props.callback === 'function') {
                props.callback(collection);
            }
        }
    }

    function destroy() {
        window.removeEventListener('storage', onStorageUpdate);
    }

    function readCollection() {
        var collectionJSON = window.localStorage.getItem(props.key);
        if (collectionJSON) {
            collection = JSON.parse(collectionJSON);
        }
        else {
            collection = [];
        }
    }

    function writeCollection() {
        var collectionJSON = JSON.stringify(collection);
        window.localStorage.setItem(props.key, collectionJSON);
    }

    function clearCollection() {
        collection = [];
        writeCollection();
    }

    function print() {
        console.log(collection);
    }

    function pushItem(item) {
        var itemIndex = collection.indexOf(item);
        if (itemIndex === -1) {
            collection.push(item);
        }
        writeCollection();
    }

    function popItem(item) {
        var itemIndex = collection.indexOf(item);
        if (itemIndex !== -1) {
            collection.pop(itemIndex);
        }
        writeCollection();
    }

    function checkItem(item) {
        return collection.indexOf(item) !== -1;
    }

    function toggleItem(item) {
        var itemIndex = collection.indexOf(item);
        var status;
        if (itemIndex === -1) {
            collection.push(item);
            status = true;
        }
        else {
            collection.pop(itemIndex);
            status = false;
        }
        writeCollection();
        return status;
    }

    // Initialize
    readCollection();
    window.addEventListener('storage', onStorageUpdate);

    return {
        destroy: destroy,
        push: pushItem,
        pop: popItem,
        check: checkItem,
        toggle: toggleItem,
        print: print,
        clear: clearCollection
    };
};


var Hider = function(props) {
    var localCollection = new LocalCollection({
        key: props.storageKey,
        callback: function(collection){
            console.log(props.storageKey, collection);
            applyLocalCollectionState();
        }
    });

    function applyLocalCollectionState() {
        $(props.multiSelector).each(function(){
            var $item = $(this);
            var itemId = $item.attr('data-id');
            var isHidden = localCollection.check(itemId);

            $item.toggleClass(props.hiddenClass, isHidden);
        });
    }

    function destroy() {
        localCollection.destroy();
        $(document).off('.' + props.storageKey);
    }

    // Initialize
    applyLocalCollectionState();
    $(document).on('click.' + props.storageKey, props.toggleSelector, function(ev){
        var $item = $(ev.target).parents(props.multiSelector);
        var itemId = $item.attr('data-id');
        var isHidden = localCollection.toggle(itemId);

        $item.toggleClass(props.hiddenClass, isHidden);
    });

    return {
        destroy: destroy
    };
};


var threadHider = new Hider({
    storageKey: 'hiddenThreads',
    hiddenClass: 'thread--hidden',
    toggleSelector: '.js-toggle-thread',
    multiSelector: '.thread'
});


var postHider = new Hider({
    storageKey: 'hiddenPostss',
    hiddenClass: 'post--hidden',
    toggleSelector: '.js-toggle-post',
    multiSelector: '.post'
});
