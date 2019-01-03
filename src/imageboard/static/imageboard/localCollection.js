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


    function concatLists(list) {
        if (Array.isArray(list)) {
            list.forEach(function(item) {
                var itemIndex = collection.indexOf(item);
                if (itemIndex === -1) {
                    collection.push(item);
                }
            });
            writeCollection();
        } else {
            throw 'Can only concat arrays';
        }

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
        clear: clearCollection,
        concat: concatLists
    };
};
