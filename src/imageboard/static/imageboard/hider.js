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


    function removeItem(item) {
        var itemIndex = collection.indexOf(item);
        if (itemIndex !== -1) {
            collection.splice(itemIndex, 1);
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
            collection.splice(itemIndex, 1);
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
        remove: removeItem,
        check: checkItem,
        toggle: toggleItem,
        print: print,
        clear: clearCollection
    };
};


var Hider = function(props) {
    var hiddenClass = props.type + '--hidden';
    var toggleSelector = '.js-toggle-' + props.type;
    var multiSelector = '.' + props.type;

    var localCollection = new LocalCollection({
        key: props.storageKey,
        callback: function(collection){
            applyLocalCollectionState();
        }
    });

    var placeholderItemTemplate = _.template($('#placeholder-item-template').html());


    function setItemState(itemId, itemHid, isHidden) {
        var $item = $('#' + props.type + '-' + itemId);

        if ($item.hasClass(hiddenClass) === isHidden) {
            return;
        }

        $item.toggleClass(hiddenClass, isHidden);

        var $placeholderItem;
        if (isHidden) {
            $placeholderItem = $(placeholderItemTemplate({
                id: itemId,
                hid: itemHid,
                label: props.placeholderLabel,
                type: props.type
            }));
            $placeholderItem.insertAfter($item);
        }
        else {
            $placeholderItem = $('#placeholder-' + props.type + '-' + itemId);
            $placeholderItem.remove();
        }
    }


    function applyLocalCollectionState() {
        $(multiSelector).each(function(){
            var $item = $(this);
            var itemId = $item.attr('data-id');
            var itemHid = $item.attr('data-hid');
            var isHidden = localCollection.check(itemId);

            setItemState(itemId, itemHid, isHidden);
        });
    }


    function onToggleClick(ev) {
        var $toggler = $(ev.target);
        var itemId = $toggler.attr('data-id');
        var itemHid = $toggler.attr('data-hid');
        var isHidden = localCollection.toggle(itemId);

        setItemState(itemId, itemHid, isHidden);
    }


    function destroy() {
        localCollection.destroy();
        $(document).off('.' + props.storageKey);
    }


    // Initialize
    applyLocalCollectionState();
    $(document).on('click.' + props.storageKey, toggleSelector, onToggleClick);

    return {
        destroy: destroy
    };
};


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
